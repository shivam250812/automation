# Robust RAG System with Agent Interaction

This project is a Robust Retrieval-Augmented Generation (RAG) system designed to generate and review question-answer (QA) pairs from a given document (e.g., PDF). It supports generating QA pairs, reviewing them, and then running an agent pipeline using the generated or reviewed pairs.

🔗 **GitHub Repository**: [https://github.com/shivam250812/automation/tree/main](https://github.com/shivam250812/automation/tree/main)

---

## 📁 Project Structure

```
.
├── agent.py                    # Main agent file (run after QA generation/review)
├── generated_qa_pairs.json    # Auto-generated QA pairs
├── reviewed_qa_pairs.json     # Manually reviewed QA pairs
├── questions.json             # Input questions (required to run the RAG system)
├── robust_rag_system/         # Core RAG system that handles document processing and QA generation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/shivam250812/automation.git
cd automation
```

### 2. Install Dependencies

Make sure you have Python 3.7+ installed. Then install required packages:

```bash
pip install -r requirements.txt
```

> Make sure `Tesseract` is also installed and its path is properly set.  
> Example (for Windows):

```python
# In your Python file before using pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 🧠 Running the RAG System

### Step 1: Prepare Input

Ensure you have a `questions.json` file ready with your questions.

### Step 2: Run QA Generator

```bash
python -m robust_rag_system
```

- When prompted, **enter the path of your PDF/document** and press **Enter twice**.
- This will generate either:
  - `generated_qa_pairs.json` (auto-generated), or
  - `reviewed_qa_pairs.json` (if reviewed manually).

---

## 🤖 Run the Agent

Once you have your QA pairs:

```bash
python agent.py
```

- The script will prompt you to enter the path to either `generated_qa_pairs.json` or `reviewed_qa_pairs.json`.

---

## 🧾 Example

```bash
# Example run
python -m robust_rag_system
# -> Input: ./data/document.pdf
# -> Press Enter again

# After QA pair generation:
python agent.py
# -> Input: ./generated_qa_pairs.json
```

---

## 🧠 Notes

- Make sure `Tesseract` OCR is properly installed and accessible by `pytesseract`.
- You can manually review the QA pairs by editing `generated_qa_pairs.json` and saving as `reviewed_qa_pairs.json`.

---

## 📄 License

MIT License (or update accordingly)
