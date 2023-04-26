import cv2
import numpy as np

# Read input
img = cv2.imread('tes.png', cv2.IMREAD_GRAYSCALE)

# Generate intermediate image; use morphological closing to keep parts of the brain together
inter = cv2.morphologyEx(img, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

# Find largest contour in intermediate image
cnts, _ = cv2.findContours(inter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnt = max(cnts, key=cv2.contourArea)

# Output
out = np.zeros(img.shape, np.uint8)
cv2.drawContours(out, [cnt], -1, 255, cv2.FILLED)
out = cv2.bitwise_and(img, out)

cv2.imshow('img', img)
cv2.imshow('inter', inter)
cv2.imshow('out', out)
cv2.waitKey(0)
cv2.destroyAllWindows()
