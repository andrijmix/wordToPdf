import os
import io
import tempfile
import shutil
import threading
import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import numpy as np
import cv2
from concurrent.futures import ThreadPoolExecutor, as_completed

TESSERACT_LANG = "eng+ukr+deu+fra+ita+spa"
CONFIG = "-c tessedit_char_whitelist=$€₴₽¥₹£0123456789.,-"
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\a.mikhnevych\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def list_pdf_files(folder):
    pdf_paths = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                relative_path = os.path.relpath(os.path.join(root, file), folder)
                pdf_paths.append(relative_path)
    return pdf_paths

def is_cancel_requested(folder):
    return os.path.exists(os.path.join(folder, "cancel.txt"))

def convert_pdf_page_to_ocr_pdf(page):
    pix = page.get_pixmap(dpi=300)
    img_bytes = pix.tobytes("ppm")
    img = Image.open(io.BytesIO(img_bytes))
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    return pytesseract.image_to_pdf_or_hocr(
        cv_img,
        lang=TESSERACT_LANG,
        config=CONFIG,
        extension='pdf'
    )

def process_single_pdf(session_folder, pdf_name):
    pdf_path = os.path.join(session_folder, pdf_name)
    output_path = os.path.join(session_folder, f"ocr_{pdf_name}")

    print(f"🔍 Processing: {pdf_path}")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copy2(pdf_path, tmp.name)
            temp_pdf_path = tmp.name

        input_doc = fitz.open(temp_pdf_path)
        output_doc = fitz.open()

        for page in input_doc:
            pdf_bytes = convert_pdf_page_to_ocr_pdf(page)
            img_pdf = fitz.open("pdf", pdf_bytes)
            output_doc.insert_pdf(img_pdf)

        output_doc.save(output_path)
        output_doc.close()
        input_doc.close()
        os.remove(temp_pdf_path)
        os.remove(pdf_path)

        print(f"✅ OCR saved: {output_path}")

    except Exception as e:
        print(f"❌ Error processing {pdf_path}: {e}")

def ocr_pdf_preserve_structure(session_folder):
    print("start function ocr_pdf_preserve_structure")
    print(f"🔍 Starting OCR for session: {session_folder}")

    if not os.path.exists(session_folder):
        print(f"❌ Session folder does not exist: {session_folder}")
        return

    pdf_files = list_pdf_files(session_folder)
    if not pdf_files:
        print(f"⚠️ No PDF files found in session: {session_folder}")
        return

    status_file = os.path.join(session_folder, "progress.txt")
    total = len(pdf_files)
    completed = 0
    lock = threading.Lock()

    def task(pdf_name):
        nonlocal completed
        if is_cancel_requested(session_folder):
            print("❌ OCR canceled by user.")
            return
        process_single_pdf(session_folder, pdf_name)
        with lock:
            completed += 1
            percent = int((completed / total) * 100)
            with open(status_file, "w") as f:
                f.write(str(percent))

    max_workers = int(os.cpu_count()/2)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(task, pdf) for pdf in pdf_files]
        for future in as_completed(futures):
            future.result()

    print("🎉 All PDFs processed.")
