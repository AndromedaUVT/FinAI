import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

def process_pdf_to_text(pdf_path):
    pages = convert_from_path(pdf_path, 300)
    full_text = []
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        full_text.append(f"--- Page {i + 1} ---\n{text}")
    return "\n".join(full_text)