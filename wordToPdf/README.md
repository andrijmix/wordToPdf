# 📝 Word to PDF Converter

Ця утиліта дозволяє масово конвертувати документи `.doc` та `.docx` у формат `.pdf`. Вона підтримує завантаження ZIP-архівів з документами, автоматично їх розпаковує, конвертує та повертає архів з PDF-файлами.

## ⚙️ Технології

- Python (Flask)
- HTML + JavaScript (frontend)
- LibreOffice CLI (`soffice.exe`) для конвертації
- Мультипроцесорна обробка (через `multiprocessing.Pool`)

## 📁 Структура

.
├── service.py # Flask-сервер, який обробляє запити і виконує конвертацію
├── frontend.html # Інтерфейс для завантаження файлів і показу прогресу
├── uploads/ # Тимчасова папка для збереження вхідних файлів
├── output/ # Папка, де зберігаються згенеровані PDF

markdown
Copy
Edit

## 🚀 Як запустити

1. **Встанови залежності** (якщо ще не зроблено):

   ```bash
   pip install flask
Переконайся, що LibreOffice встановлений і шлях до soffice.exe правильно вказано у SOFFICE_PATH (рядок 13):

python
Copy
Edit
SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"
Запусти сервер:

bash
Copy
Edit
python service.py
Відкрий у браузері:

arduino
Copy
Edit
http://localhost:63342
💡 Можливості
Підтримка масового завантаження .doc, .docx і .zip

Прогрес завантаження і обробки

Можливість зупинити завантаження

Безпечна обробка назв файлів

Конвертація ізоляційно (кожен процес має свій профіль користувача LibreOffice)

📦 Вхідні формати
.doc, .docx

.zip (який містить DOC-файли)

📤 Вихід
ZIP-архів converted.zip, який містить PDF-файли

⚠️ Обмеження
Тільки для Windows (через шлях до soffice.exe)

Не підтримує вкладені ZIP-архіви