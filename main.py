import data_extraction as dx
import data_preparation as dp
import utils as ut
import numpy as np
import cv2 as cv

data = []
labels = []

video_width = 480
video_height = 640
width = 100
height = 200
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
    roi = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    smooth = dp.smooth(roi)
    acc = dp.accent(smooth)
    bin = dp.binarize(acc)
    edges = dp.edges(bin)
    rectangle = dp.findRectangle(edges, bin)
    if not rectangle is None:
        cv.imshow("plate", rectangle)
        
    # if cv.waitKey(1) == ord("c"):
        chars = dp.chars(rectangle, min_area=100, max_area=300)
        if len(chars) > 0 :
            for i, c in enumerate(chars):
                cv.imshow(f"char: {i}", c)
         
         
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()

# data = ut.loadData("binary_data")
# labels = ut.loadData("labels")


