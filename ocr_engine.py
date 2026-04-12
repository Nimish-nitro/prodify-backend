# ocr_engine.py — extracts text from a preprocessed image using Tesseract OCR

import pytesseract
import cv2
from preprocessor import preprocess
import platform

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_text(image_path):
    """
    Takes a raw screenshot path, preprocesses it,
    runs Tesseract OCR, and returns extracted text as a string.
    """
    processed = preprocess(image_path)

    # OCR config: treat image as a single block of text
    config = "--psm 6"
    text = pytesseract.image_to_string(processed, config=config)

    cleaned = text.strip()
    print(f"[ocr] Extracted {len(cleaned)} characters")
    return cleaned


def extract_text_raw(image_path):
    """Skips preprocessing — runs OCR directly on the raw image."""
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()
