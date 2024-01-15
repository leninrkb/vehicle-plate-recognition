import data_preparation as dp
import cv2 as cv
import post_processing
import time
import asyncio

auto = False
capture = False
end = False
dp.set_kernel_smooth_size(5)
video_width = 480 # original
video_height = 640 # original
width = 150 # roi
height = 250 # roi
top_left = (video_height//2 - height, video_width//2 - width)
bottom_right = ( video_height//2 + height, video_width//2 + width)
padd = 10

def set_auto():
    global auto
    auto = not auto

def capture_frame():
    global capture
    capture = True
    
def end_recognition():
    global end
    end = True
    
async def count():
    for i in range(5):
        print(i)
        time.sleep(1)
    
def recognition(predict_mode, find_method=None):
    global capture
    global end
    global auto
    capture = False
    end = False
    cap = cv.VideoCapture(0)
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv.resize(frame, (video_height, video_width))
        cv.rectangle(frame, top_left, bottom_right, (0,255,0), 1)
        cv.imshow("frame",frame)
        # 
        roi = frame[top_left[1]+padd:bottom_right[1]-padd, top_left[0]+padd:bottom_right[0]-padd]
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
        
        edges = dp.edges(bin)
        cv.imshow("5 roi edges", edges)
        
        rect, roi = dp.findRectangle(bin, bin, roi)
        if not rect is None:
            rect = dp.smooth(rect)
            # rect = dp.smooth(rect)
            # rect = dp.accent(rect)
            rect = dp.binarize(rect)
            rect = dp.binarize(rect)
            # rect = dp.accent(rect)
            cv.imshow("6 plate", rect)
            # cv.imshow("7 roi", roi)
            chars = dp.chars(rect)
            if cv.waitKey(1) == ord("c") or cv.waitKey(1) == ord("C") or capture or auto:
                print("chars...")
                capture = False
                if not chars == None and len(chars) > 0:
                    start = time.time()
                    plate = predict_mode(chars)
                    find_method(plate)
                    print(f"time: {time.time() - start}", end="\n ------------ \n")
        if cv.waitKey(1) == ord('q') or end:
            end = False
            set_auto()
            break
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    recognition(post_processing.nn)
