import os
import shutil
import tempfile
import subprocess
from multiprocessing import Pool, cpu_count
from pathlib import Path
from tqdm import tqdm


def load_config(path="config.txt"):
    config = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=", 1)
                config[key.strip()] = val.strip()
    return config


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
        return (input_file, True, "")
    except subprocess.CalledProcessError as e:
        return (input_file, False, e.stderr.decode(errors="ignore"))
    finally:
        shutil.rmtree(temp_profile, ignore_errors=True)


def find_word_files(input_folder):
    exts = {".doc", ".docx"}
    return [
        p for p in Path(input_folder).rglob("*")
        if p.suffix.lower() in exts
    ]


def main():
    config = load_config()
    input_folder = Path(config["input_folder"])
    output_folder = Path(config["output_folder"])
    soffice_path = "C:\Program Files\LibreOffice\program\soffice.exe"

    output_folder.mkdir(parents=True, exist_ok=True)

    files = find_word_files(input_folder)
    print(f"📄 Found {len(files)} Word files.")

    if not files:
        return

    num_workers = int(cpu_count()/2)
    print(f"🚀 Converting using {num_workers} parallel processes...")

    args = [(soffice_path, f, output_folder) for f in files]

    results = []
    with Pool(processes=num_workers) as pool:
        for result in tqdm(pool.imap_unordered(convert_with_soffice, args), total=len(args)):
            results.append(result)

    success = [r for r in results if r[1]]
    failed = [r for r in results if not r[1]]

    print(f"\n✅ Converted: {len(success)}")
    print(f"❌ Failed: {len(failed)}")

    if failed:
        print("\n❗ Errors:")
        for path, _, err in failed:
            print(f"- {path}\n{err}")


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()
    main()
