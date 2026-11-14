"""
Edge Detection using OpenCV (Canny & Laplacian)
Requires: opencv-python (pip install opencv-python)
"""

from pathlib import Path
import cv2

# Determine image path relative to script directory
BASE_DIR = Path(__file__).resolve().parent
image_path = BASE_DIR / 'test.jpg'

# Read the image
img = cv2.imread(str(image_path))
if img is None:
    raise FileNotFoundError(
        f"Unable to read image at '{image_path}'. "
        "Please verify that 'test.jpg' exists in the script directory."
    )

# Resize the image for consistent display
img = cv2.resize(img, (300, 300))

# Display the original image
cv2.imshow('1 - Original Image', img)
cv2.waitKey(0)

# Convert to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Blur the image for noise reduction prior to edge detection
blur_img = cv2.GaussianBlur(img_gray, (3, 3), 0)
cv2.imshow('2 - Gaussian Blurred Image', blur_img)
cv2.waitKey(0)

# Canny edge detection
canny = cv2.Canny(blur_img, 100, 200)
cv2.imshow('3 - Canny Edge Detection', canny)
cv2.waitKey(0)

# Laplacian edge detection
laplacian = cv2.Laplacian(blur_img, cv2.CV_64F)
cv2.imshow('4 - Laplacian Edge Detection', laplacian)
cv2.waitKey(0)

cv2.destroyAllWindows()
