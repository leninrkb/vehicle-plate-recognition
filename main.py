import data_extraction as dx
import data_preparation as dp
import utils as ut
import numpy as np
import cv2 as cv
import post_processing as pp
import time

capture = False
end = False
cap = cv.VideoCapture(0)
dp.set_kernel_smooth_size(5)

def capture_frame():
    global capture
    capture = True
    
def end_recognition():
    global end
    end = True
    
def main():
    global capture
    global end
    capture = False
    end = False
    video_width = 480
    video_height = 640
    width = 150
    height = 250
    top_left = (video_height//2 - height, video_width//2 - width)
    bottom_right = ( video_height//2 + height, video_width//2 + width)

    cap.open(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
        
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        cv.rectangle(frame, top_left, bottom_right, (0,255,0), 1)
        cv.imshow("frame",frame)
        # 
        s = 10
        roi = frame[top_left[1]+s:bottom_right[1]-s, top_left[0]+s:bottom_right[0]-s]
        # cv.imshow("roi", roi)
        
        gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
        gray = cv.convertScaleAbs(gray, alpha=1.8, beta=0)
        # cv.imshow("1 roi gray", gray)
        
        # smooth = dp.smooth(gray)
        # cv.imshow("2 roi smooth", smooth)
        
        # acc = dp.accent(smooth)
        # cv.imshow("3 roi accent", acc)
        
        bin = dp.binarize(gray)
        # cv.imshow("4 roi bin", bin)
        
        # edges = dp.edges(bin)
        # cv.imshow("5 roi edges", edges)
        
        rect, roi = dp.findRectangle(bin, bin, roi)
        if not rect is None:
            cv.imshow("6 plate", rect)
            cv.imshow("7 roi", roi)
            chars = dp.chars(rect)
            if cv.waitKey(1) == ord("c") or capture:
                print("chars...")
                capture = False
                if not chars == None and len(chars) > 0:
                    start = time.time()
                    pp.ann_predict(chars)
                    print(f"time: {time.time() - start}", end="\n ------------ \n")
            del chars
        if cv.waitKey(1) == ord('q') or end:
            break
    cap.release()
    cv.destroyAllWindows()
    end = False

main()
# main()
