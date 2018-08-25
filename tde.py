from moviepy.editor import VideoFileClip
import numpy as np
import math

import cv2

class TDE():
    def __init__(self, stream_name='data/vlc-output_19.mp4'):
        self.t = 0
        self.video = VideoFileClip(stream_name)
        self.roi = np.array([(473, 203), (643, 200), (850, 500), (35, 500)])

    def setROI(self, topleft, topright, bottomright, bottomleft):
        self.roi = np.array([topleft, topright, bottomright, bottomleft])

    def order_points(self, pts):
        rect = np.zeros((4, 2), dtype="float32")

        # s = pts.sum(axis=1)
        # rect[0] = pts[np.argmin(s)]
        # rect[2] = pts[np.argmax(s)]

        # diff = np.diff(pts, axis=1)
        # rect[1] = pts[np.argmin(diff)]
        # rect[3] = pts[np.argmax(diff)]

        rect[0] = pts[0]
        rect[1] = pts[1]
        rect[2] = pts[2]
        rect[3] = pts[3]

        return rect

    def four_point_transform(self, image, pts):
        rect = self.order_points(pts)
        (tl, tr, br, bl) = rect

        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        # (h, w) = (image.shape[0], image.shape[1])
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        unwarp_matrix = cv2.getPerspectiveTransform(dst, rect)
        return warped, unwarp_matrix

    def get_next_frame(self):
        saliency = None
        image = self.video.get_frame(self.t)
        self.t+=1
        flatted = self.four_point_transform(image, self.roi)
        F_ROI = flatted[0]

        saliency = cv2.saliency.StaticSaliencyFineGrained_create()
        (success, saliencyMap) = saliency.computeSaliency(F_ROI)
        density = 0

        if success:
            threshMap = cv2.threshold(saliencyMap, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

            n_white_pix = np.sum(threshMap == 255)
            n_pix = threshMap.shape[0] * threshMap.shape[1]
            density = math.floor((n_white_pix/n_pix)*100)

            # cv2.putText(image,str(density)+'%', (100,100), cv2.FONT_HERSHEY_PLAIN, 4, 255, thickness=2)
        
        alpha = 0.7
        overlay = image.copy()
        # cv2.rectangle(overlay, (420, 205), (595, 385),
		# (0, 0, 255), -1)

        # contours = np.array( [ [50,50], [50,150], [150, 150], [150,50] ] )
        contours = self.roi
        
        cv2.fillPoly(image, pts =[contours], color=(255,255,0))

        cv2.addWeighted(overlay, alpha, image, 1 - alpha,
		0, image)
        cv2.imshow("Thresh", threshMap)
        key = cv2.waitKey(1)

        return image, density

    def run(self):
        saliency = None
        t = 0
        while True:
            image = self.video.get_frame(t)
            t+=1
            flatted = self.four_point_transform(image, self.roi)
            F_ROI = flatted[0]

            saliency = cv2.saliency.StaticSaliencyFineGrained_create()
            (success, saliencyMap) = saliency.computeSaliency(F_ROI)

            threshMap = cv2.threshold(saliencyMap, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

            _, contours, hierarchy = cv2.findContours(threshMap, 1, 2)

            for i in range(len(contours)):
                cnt = contours[i]
                hull = cv2.convexHull(cnt, returnPoints = False)
                defects = cv2.convexityDefects(cnt,hull)
                if defects is None:
                    continue
                for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    cv2.line(F_ROI,start,end,[0,255,0],2)
                    # cv2.circle(F_ROI,far,5,[0,0,255],-1)

            n_white_pix = np.sum(threshMap == 255)
            n_pix = threshMap.shape[0] * threshMap.shape[1]
            density = math.floor((n_white_pix/n_pix)*100)

            cv2.putText(image,str(density)+'%', (100,100), cv2.FONT_HERSHEY_PLAIN, 4, 255, thickness=2)

            cv2.imshow("Thresh", threshMap)
            cv2.imshow("Map", saliencyMap)
            cv2.imshow('ROI', cv2.cvtColor(F_ROI, cv2.COLOR_RGB2BGR))

            cv2.imshow('original', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

            key = cv2.waitKey(1)
    

if __name__ == '__main__':
    a = []
    def getxy(event, x, y, flags, param):
        global a
        if event == cv2.EVENT_LBUTTONDOWN :
                a.append([x, y])
                print ("(row, col) = ({},{})".format(x,y))

    video_name = 'data/vlc-output_19.mp4'
    video = VideoFileClip(video_name)
    t = 0
    image = video.get_frame(0)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', getxy)

    cv2.imshow('image', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    tde = TDE()
    tde.setROI(a[0], a[1], a[2], a[3])
    tde.run()