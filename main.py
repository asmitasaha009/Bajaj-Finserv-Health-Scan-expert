from io import BytesIO
from typing import List, Dict, Any

import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from PIL import Image

from utils import clean, TEST_NAME_RE, VALUE_RE, RANGE_RE  # Fixed import

def _bytes_to_cv2(img_bytes: bytes) -> np.ndarray:
    """Convert raw bytes -> OpenCV BGR image"""
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def _preprocess(bgr: np.ndarray) -> np.ndarray:
    """Quick grayscale + adaptive threshold"""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)
    thr = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV, 25, 15
    )
    return cv2.bitwise_not(thr)  # white text, black BG – better for OCR

def extract_lab_tests(img_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Extract lab test results from image bytes.
    Returns a list of dicts with:
        - lab_test_name
        - lab_test_value
        - unit
        - bio_reference_range
        - lab_test_out_of_range
    """
    image = _bytes_to_cv2(img_bytes)
    preprocessed = _preprocess(image)

    ocr_text = pytesseract.image_to_string(preprocessed, config="--oem 3 --psm 6")
    lines = [clean(line) for line in ocr_text.splitlines() if line.strip()]

    results = []
    for line in lines:
        name_match = TEST_NAME_RE.match(line)
        value_match = VALUE_RE.search(line)
        range_match = RANGE_RE.search(line)

        if not (name_match and value_match):
            continue  # Skip if we can't extract value or name

        name = name_match.group().strip()
        value = float(value_match.group(1))
        unit = value_match.group(2) or ""

        low, high = None, None
        if range_match:
            low, high = map(float, range_match.groups())

        out_of_range = (
            (low is not None and value < low) or
            (high is not None and value > high)
        ) if (low is not None or high is not None) else None

        results.append({
            "lab_test_name": name,
            "lab_test_value": value,
            "unit": unit,
            "bio_reference_range": f"{low}-{high}" if low is not None else None,
            "lab_test_out_of_range": out_of_range
        })

    return results
