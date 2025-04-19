import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def detect_text_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return {"medicine": "Unknown", "raw_text": ""}

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=0.8, fy=0.8)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                 cv2.THRESH_BINARY, 11, 2)

    text = pytesseract.image_to_string(gray).strip()

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    medicine_name = lines[0] if lines else "Unknown"

    return {
        "medicine": medicine_name,
        "raw_text": text
    }
