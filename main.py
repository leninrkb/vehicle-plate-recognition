import data_extraction as dx
import data_preparation as dp
import utils as ut
import numpy as np
import cv2 as cv
import post_processing as pp
import time

data = []
labels = []

video_width = 480
video_height = 640
width = 150
height = 250
top_left = (video_height//2 - height, video_width//2 - width)
bottom_right = ( video_height//2 + height, video_width//2 + width)

cap = cv.VideoCapture(0)
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
    # cv.imshow("roi gray", gray)
    
    # smooth = dp.smooth(gray)
    # cv.imshow("roi smooth", smooth)
    
    # acc = dp.accent(gray)
    # cv.imshow("roi accent", acc)
    
    bin = dp.binarize(gray)
    # cv.imshow("roi bin", bin)
    
    edges = dp.edges(bin)
    # cv.imshow("roi edges", edges)
    
    rect, roi = dp.findRectangle(edges, bin, roi)
    if not rect is None:
        cv.imshow("plate", rect)
        cv.imshow("roi", roi)
        chars = dp.chars(rect)
        if cv.waitKey(1) == ord("c") or True:
            if len(chars) > 0:
                start = time.time()
                pp.main(chars)
                print(f"time: {time.time() - start}", end="\n ------------ \n")
        del chars
        # del chars, rect
    # del roi, gray, acc, bin, edges, smooth
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()

# data = ut.loadData("binary_data")
# labels = ut.loadData("labels")


