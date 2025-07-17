from flask import Flask, request, send_file, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import shutil
import zipfile
import tempfile
import subprocess
from pathlib import Path
from multiprocessing import Pool, cpu_count

app = Flask(__name__, template_folder="templates")
UPLOAD_FOLDER = Path("../uploads")
OUTPUT_FOLDER = Path("../output")
SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)


def convert_with_soffice(args):
    soffice_path, input_file, output_folder = args
    temp_profile = tempfile.mkdtemp(prefix="lo_profile_")
    profile_url = f"file:///{temp_profile.replace(os.sep, '/')}"

    try:
        subprocess.run([
            soffice_path,
            "--headless",
            f"-env:UserInstallation={profile_url}",
            "--convert-to", "pdf",
            "--outdir", str(output_folder),
            str(input_file)
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return (input_file.name, True, "")
    except subprocess.CalledProcessError as e:
        return (input_file.name, False, e.stderr.decode(errors="ignore"))
    finally:
        shutil.rmtree(temp_profile, ignore_errors=True)


def extract_zip_to_folder(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


@app.route("/")
def index():
    return render_template("frontend.html")


@app.route("/convert", methods=["POST"])
def convert():
    try:
        uploaded_files = request.files.getlist("files")
        if not uploaded_files:
            return jsonify({"error": "No files uploaded"}), 400

        print("🧹 Cleaning old folders...")
        shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
        shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)

        UPLOAD_FOLDER.mkdir(exist_ok=True)
        OUTPUT_FOLDER.mkdir(exist_ok=True)

        word_paths = []

        # Save uploaded files
        print("💾 Saving uploaded files...")
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            file_path = UPLOAD_FOLDER / filename
            file.save(file_path)

            if file_path.suffix.lower() == ".zip":
                print(f"📦 Extracting zip: {filename}")
                extract_zip_to_folder(file_path, UPLOAD_FOLDER)
            elif file_path.suffix.lower() in [".doc", ".docx"]:
                word_paths.append(file_path)

        # Collect all Word files, including from extracted ZIPs
        for path in UPLOAD_FOLDER.rglob("*"):
            if path.suffix.lower() in [".doc", ".docx"]:
                word_paths.append(path)

        if not word_paths:
            print("⚠️ No Word files found for conversion.")
            return jsonify({"error": "No .doc or .docx files found"}), 400

        print(f"📄 Files to convert: {[str(p.name) for p in word_paths]}")

        args = [(SOFFICE_PATH, f, OUTPUT_FOLDER) for f in word_paths]
        with Pool(cpu_count() // 2 or 1) as pool:
            results = pool.map(convert_with_soffice, args)

        success = [name for name, ok, _ in results if ok]
        failed = [(name, err) for name, ok, err in results if not ok]

        print(f"✅ Successfully converted: {success}")
        for name, err in failed:
            print(f"❌ Failed: {name} — {err}")

        # Check for any PDF output
        pdf_files = list(OUTPUT_FOLDER.glob("*.pdf"))
        if not pdf_files:
            return jsonify({"error": "No PDF files were generated."}), 500

        # Zip the converted PDFs
        zip_path = OUTPUT_FOLDER / "converted.zip"
        print(f"📦 Creating ZIP archive at {zip_path}...")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for pdf in pdf_files:
                zipf.write(pdf, pdf.name)

        if not zip_path.exists():
            print("🚨 ZIP file was not created.")
            return jsonify({"error": "ZIP creation failed"}), 500

        print("✅ Returning converted.zip to user.")
        return send_file(
            zip_path,
            as_attachment=True,
            download_name="converted.zip"
        )

    except Exception as e:
        print(f"🚨 Unhandled exception: {e}")
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=63342)
