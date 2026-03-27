# preprocessor.py — cleans up a raw screenshot for better OCR accuracy

import cv2
import numpy as np

def preprocess(image_path):
    """
    Takes a raw screenshot path, applies OpenCV cleanup,
    and returns a processed image ready for OCR.
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Resize to standard width (keeps aspect ratio)
    target_width = 1280
    height, width = img.shape[:2]
    if width != target_width:
        scale = target_width / width
        img = cv2.resize(img, (target_width, int(height * scale)))

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    # Improve contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    # Threshold to make text sharper (black text on white background)
    _, processed = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return processed


def save_processed(image_path, output_path="processed.png"):
    """Saves the processed image to disk (useful for debugging)."""
    processed = preprocess(image_path)
    cv2.imwrite(output_path, processed)
    print(f"[preprocessor] Saved processed image to {output_path}")
    return output_path
