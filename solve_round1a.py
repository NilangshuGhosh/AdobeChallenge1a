import fitz  # PyMuPDF
from transformers import pipeline
from deep_translator import GoogleTranslator
import json

def extract_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []

    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        if text.strip():
            sections.append({
                "page": page_num + 1,
                "content": text.strip()
            })
    return sections

def summarize_content(sections, target_lang="en"):
    print("🔁 Loading summarization model...")
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    summaries = []

    for sec in sections:
        raw = sec["content"]
        clipped = raw[:1024] if len(raw) > 1024 else raw

        if len(clipped.split()) < 10:
            summary = clipped
        else:
            summary = summarizer(clipped, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
        
        # Translate summary if needed
        if target_lang != "en":
            try:
                summary = GoogleTranslator(source='auto', target=target_lang).translate(summary)
            except Exception as e:
                summary = "[Translation failed] " + summary
        
        summaries.append({
            "page": sec["page"],
            "summary": summary
        })

    return summaries

def main():
    print("📄 SmartPDF Assistant with Multilingual Summarization")
    pdf_path = input("Enter path to PDF (e.g. sample.pdf): ").strip()
    lang = input("Translate summaries to language (e.g., en, hi, fr, es): ").strip().lower()

    try:
        print("🔍 Extracting content...")
        sections = extract_pdf_content(pdf_path)

        if not sections:
            print("⚠ No text found in the PDF.")
            return

        print(f"✅ Found {len(sections)} pages with text.")
        print("🧠 Generating summaries...\n")

        summaries = summarize_content(sections, lang)

        for s in summaries:
            print(f"\n📄 Page {s['page']} Summary:\n{s['summary']}\n{'-'*50}")

        save = input("\n💾 Save summaries to output.json? (y/n): ").strip().lower()
        if save == 'y':
            with open("output.json", "w", encoding='utf-8') as f:
                json.dump(summaries, f, indent=2, ensure_ascii=False)
            print("✅ Summary saved to output.json")

    except Exception as e:
        print("❌ Error:", str(e))

if _name_ == "_main_":
    main()
