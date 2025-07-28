# AdobeChallenge1a
For the Challenge 1a .
# SmartPDF Assistant with Multilingual Summarization

This Python script extracts text from a PDF, summarizes its content page-by-page using a transformer model (`distilbart-cnn-12-6`), and optionally translates the summaries into a specified language using Google Translate API (via `deep-translator`).

---

##  Features

- Extracts text from each page of a PDF using `PyMuPDF`
- Generates concise summaries using Hugging Face Transformers
- Supports translation to over 100 languages via Google Translate
- Saves the summarized output to a JSON file (`output.json`)

---

## Requirements

Install the required libraries with:

```bash
pip install transformers deep-translator pymupdf

