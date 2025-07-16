# Renamorator 🗂️📄

Renamorator is a semi-automated document renaming tool built with Python. It helps standardize naming conventions for large batches of files (like scanned production reports or blend sheets) using a simple GUI. The tool extracts fields such as document number, blend name, volume, and equipment from messy filenames and renames them into a clean, searchable format:

**Format Example:**
VP123.456 | Blueberry Blend | 200gal | Line 5

---

## 🚀 Features

- Extracts and renames files using patterns in filenames
- GUI built in `tkinter` for ease of use
- Parses Excel data if needed (planned)
- Customizable naming convention
- Safe batch renaming (no overwrites)

---

## 🔧 Tech Stack

- Python 3.x
- `tkinter` (GUI)
- `pandas` (Excel parsing)
- `os`, `re`, and `shutil` (file system tools)

---

## 📁 File Structure

```
Renamorator/
├── main.py             # Entry point
├── gui.py              # GUI code
├── excel_utils.py      # Excel parsing helpers (in progress)
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🛠 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/CodexSoftwareDevelopment/Renamorator.git
cd Renamorator

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

---

## 📌 To Do

- [ ] Complete Excel file parsing logic
- [ ] Add drag-and-drop folder selection
- [ ] Implement undo feature
- [ ] Add test coverage

---

## 📜 License

This project is licensed under the MIT License – see the [LICENSE](./LICENSE) file for details.

---

## 👩‍💻 Author

**Deidra Clay**  
GitHub: [CodexSoftwareDevelopment](https://github.com/CodexSoftwareDevelopment)

*Built with purpose and caffeine.*
