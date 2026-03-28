from aiParser import *
from ocr import *

import json

pdf_file = r'C:\Users\Edward\Desktop\test\LRK0494.pdf'
prompt_injection = r''

print("Running OCR...")
raw_content = process_pdf_to_text(pdf_file)

print("Standardizing with Gemini...")
structured_data = standardize_with_gemini(raw_content, prompt_injection)

print(json.dumps(structured_data, indent=4))

def send_json_to_db():
    print('todo')