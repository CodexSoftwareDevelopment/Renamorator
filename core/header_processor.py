import cv2
import numpy as np

def preprocess_header(img: np.ndarray) -> np.ndarray:
    h, w = img.shape[:2]
    header = img[0:int(h * 0.25), :]
    gray = cv2.cvtColor(header, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    th = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    coords = np.column_stack(np.where(opening > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    M = cv2.getRotationMatrix2D((w / 2, h * 0.125), angle, 1.0)
    deskewed = cv2.warpAffine(
        opening, M, (w, int(h * 0.25)),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
    return cv2.bitwise_not(deskewed)