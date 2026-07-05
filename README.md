# Electoral Roll PDF to CSV Converter

## Overview

Government electoral rolls are often distributed as scanned PDF documents, making them difficult to search, filter, or analyze.

This project automates the conversion of scanned electoral rolls into structured CSV files through an OCR-based pipeline.

```
Scanned PDF
      │
      ▼
   Page Images
      │
      ▼
 Tesseract OCR
      │
      ▼
 Parsed Text
      │
      ▼
 Structured CSV
```

---

## Tech Stack

- Python
- PyMuPDF (PDF rendering)
- Tesseract OCR
- Pandas

---

## Features

- Batch processing of electoral roll PDFs
- Hindi OCR support
- Multi-page document processing
- Structured CSV export
- Modular parsing pipeline
- Easy to customize for different electoral roll formats

---

## Project Structure

```
project/
│
├── input/              # Input PDF files
├── images/             # Extracted page images
├── text/               # OCR output (optional)
├── output/             # Final CSV files
│
├── pdf_to_images.py
├── ocr.py
├── parser.py
├── main.py
│
└── README.md
```

---

## Workflow

1. Read the scanned PDF.
2. Convert each page into an image using **PyMuPDF**.
3. Perform OCR using **Tesseract** (Hindi language model).
4. Extract required voter information.
5. Export the results to a structured CSV file.

---

## Output

The generated CSV can be used for:

- Searching voter records
- Data analysis
- Deduplication
- Filtering
- Integration with other applications

---

---

## License

This project is intended for educational and public-interest purposes. Users are responsible for complying with applicable laws and regulations governing the use of electoral roll data.
