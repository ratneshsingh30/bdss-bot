# LLaMA 4 Quiz Tutor for MCQs + File & Image Support + OCR + MCQ Highlighting

This app fine-tunes LLaMA 4 on MCQ-style questions from your Decision and Behavioural Analytics course.
It supports:
- `.txt`, `.docx`, `.pdf`, `.pptx`
- `.png`, `.jpg`, `.jpeg`
- Paste or upload screenshots
- Auto-detect MCQs from OCR or slides
- Highlights correct MCQ option automatically

## How to Use

1. Clone this repo.
2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Launch the tutor app:
```bash
streamlit run app.py
```

4. Upload or paste a screenshot or document.
5. Confirm extracted text (or MCQ).
6. Get the answer with explanation and correct option highlighted!
