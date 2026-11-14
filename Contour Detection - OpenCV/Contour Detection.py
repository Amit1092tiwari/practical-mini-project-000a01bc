"""
Contour Detection using OpenCV
Requires: opencv-python (pip install opencv-python)
"""

from pathlib import Path
import cv2

# Determine image path relative to script directory
BASE_DIR = Path(__file__).resolve().parent
image_path = BASE_DIR / 'test1.jpg'

# Load the image
image = cv2.imread(str(image_path))
if image is None:
    raise FileNotFoundError(
        f"Unable to read image at '{image_path}'. "
        "Please verify that 'test1.jpg' exists in the script directory."
    )

# Resize the image for consistent display
image = cv2.resize(image, (350, 350))

# Display the original image
cv2.imshow('1 - Original Image', image)
cv2.waitKey(0)

# Convert to grayscale
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('2 - Grayscale Image', img_gray)
cv2.waitKey(0)

# Apply binary threshold
# Adjust threshold (e.g., between 50 and 150) to fine-tune contour detection
ret, img_thresh = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY)
cv2.imshow('3 - Binary Threshold Image', img_thresh)
cv2.waitKey(0)

# Detect contours on binary image
contours, _ = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print(f"Total contours detected: {len(contours)}")

# Draw contours on a copy of the original image
img_copy = image.copy()
cv2.drawContours(img_copy, contours, -1, (0, 255, 0), 2, lineType=cv2.LINE_AA)

# Display final contour image
cv2.imshow('4 - Contour Detected Image', img_copy)
cv2.waitKey(0)

cv2.destroyAllWindows()
