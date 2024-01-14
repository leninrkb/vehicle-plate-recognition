import cv2 as cv
import numpy as np
from scipy.spatial import distance
import aspect_ratio as ar

kernel_smooth_size = 3
kernel_smooth = np.ones((kernel_smooth_size, kernel_smooth_size), np.float32) / (kernel_smooth_size * kernel_smooth_size)
kernel_accent = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])


def set_kernel_smooth_size(size):
    global kernel_smooth
    kernel_smooth = np.ones((size, size), np.float32) / (size * size)


def binarizeData(data: list):
    for i in range(len(data)):
        data[i] = binarize(data[i])


def resizeData(data: list, newsize: int):
    for i in range(len(data)):
        data[i] = cv.resize(data[i], (newsize, newsize))


def binarize(img):
    _, res = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    return res


def smooth(img):
    res = cv.filter2D(img, -1, kernel_smooth)
    return res


def edges(img):
    edges = cv.Canny(img, 100, 200)
    # edges = cv.dilate(edges, None, iterations=1)
    return edges


def accent(img):
    img = cv.filter2D(img, -1, kernel_accent)
    return img


def findRectangle(img, roi_bin, roi):
    contours, _ = cv.findContours(img, cv.RETR_TREE, cv.RETR_CCOMP)
    plate = None
    for contour in contours:
        epsilon = 0.08 * cv.arcLength(contour, True) # establece el umbral par que un poligono sea tomando en cuenta como cuadrangular
        apx = cv.approxPolyDP(contour, epsilon, True)
        if len(apx) == 4:
            area = cv.contourArea(contour)
            if 1500 < area < 40000:
                x, y, w, h = cv.boundingRect(contour) # retorna los puntos del objeto
                aspect_ratio = w / h
                if aspect_ratio >= 1 or ar.threshold(aspect_ratio) or w > h:
                    plate = roi_bin[y : y + h, x : x + w]
                    roi = cv.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return plate, roi


def sortChars(chars):
    sorted_chars = sorted(chars, key=lambda x: x[1])
    sorted_chars = [c[0] for c in sorted_chars]
    return sorted_chars


def chars(img):
    contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    characters = []
    areas = []
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 7:
            x, y, w, h = cv.boundingRect(contour)
            if w < h :
                area =  h
                areas.append(area)
                ch = img[y : y + h, x : x + w]
                characters.append((ch, x, area))
    avg = np.average(areas)
    selected_chars = []
    for char in characters:
        if char[2] >= avg:
            selected_chars.append(char)
    return sortChars(selected_chars)


def hamming_distance(x, y):
    return distance.hamming(x, y)


def flattenData(data):
    data = np.array(data)
    data = data.reshape(data.shape[0], -1)
    return data


def transformRect2Sqr(img, pad=10):
    height, width = img.shape
    diff = abs(height - width)
    if height > width:
        padding = ((0, 0), (diff // 2, diff - diff // 2))
    else:
        padding = ((diff // 2, diff - diff // 2), (0, 0))
    img = np.pad(img, padding, mode="constant", constant_values=0)
    top, bottom, left, right = [pad] * 4
    img = cv.copyMakeBorder(img, top, bottom, left, right, cv.BORDER_CONSTANT, value=0)
    return img


def prepare_img(mat, dim=28):
    mat = transformRect2Sqr(mat, pad=1)
    mat = cv.resize(mat, (dim, dim))
    mat = mat / 255
    mat = np.array([mat], dtype=np.uint8)
    return mat
