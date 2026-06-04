# DocMax — Forge your documents from your terminal.

A unified, offline-first Python CLI for all your document processing needs.

---

## Installation

```bash
pip install DocMax
```

### External Dependencies

| Tool | Purpose | Install |
|------|---------|---------|
| Tesseract OCR | OCR engine | [Install guide](https://tesseract-ocr.github.io/tessdoc/Installation.html) |
| Ghostscript | PDF compression | [ghostscript.com](https://ghostscript.com/releases/gsdnld.html) |
| Pandoc | Document conversion | [pandoc.org](https://pandoc.org/installing.html) |
| Poppler | PDF → image (pdf2image) | `apt install poppler-utils` / `brew install poppler` |

---

## Quick Reference

### PDF Operations

```bash
# Merge PDFs
DocMax merge a.pdf b.pdf c.pdf -o merged.pdf

# Split into pages
DocMax split report.pdf

# Compress (uses Ghostscript)
DocMax compress large.pdf --preset ebook

# Rotate pages
DocMax rotate file.pdf 90

# Extract page range
DocMax pages file.pdf 1-5

# Watermark
DocMax watermark file.pdf logo.png

# Encrypt / Decrypt
DocMax encrypt file.pdf
DocMax decrypt protected.pdf
```

### OCR

```bash
# OCR an image
DocMax ocr scan.png

# OCR a PDF
DocMax ocr scan.pdf

# Output as JSON or Markdown
DocMax ocr scan.pdf --fmt json
DocMax ocr scan.pdf --fmt md

# Multi-language OCR
DocMax ocr scan.png --lang eng+hin

# Make a scanned PDF searchable
DocMax searchable scan.pdf

# Batch OCR an entire folder
DocMax batch-ocr invoices/
```

### Document Conversion

```bash
# Convert DOCX → PDF
DocMax convert report.docx pdf

# Convert Markdown → HTML
DocMax convert notes.md html

# Combine images into a PDF
DocMax img2pdf scans/

# Export PDF pages as images
DocMax pdf2img report.pdf --dpi 300 --fmt png
```

### Content Extraction

```bash
# Extract text
DocMax text report.pdf

# Extract embedded images
DocMax images report.pdf

# Show / save metadata
DocMax metadata report.pdf
DocMax metadata report.pdf -o meta.json

# Extract tables
DocMax tables invoice.pdf --fmt xlsx
DocMax tables invoice.pdf --fmt csv
DocMax tables invoice.pdf --fmt json
```

### Image Processing

```bash
# Enhance (contrast + sharpness)
DocMax enhance scan.png

# Fix skewed scans
DocMax deskew scan.png

# Remove noise
DocMax denoise scan.png

# Resize
DocMax resize photo.png --width 800
DocMax resize photo.png --scale 0.5

# Full OCR preprocessing pipeline
DocMax preprocess scan.png
```

### Batch Processing

```bash
# Batch OCR with 8 workers
DocMax batch ./documents --ocr --workers 8

# Batch compress
DocMax batch ./pdfs --compress

# Batch convert to markdown
DocMax batch ./docs --convert md
```

### Watch Mode

```bash
# Auto-OCR new files dropped into a folder
DocMax watch ./incoming --ocr

# Auto-make-searchable
DocMax watch ./scans --searchable

# Auto-compress
DocMax watch ./uploads --compress
```

---

## Project Structure

```
DocMax/
├── cli.py           ← Typer CLI entry point
├── config.py        ← Global configuration
├── utils.py         ← Shared utilities
├── pdf/
│   └── operations.py  ← merge, split, compress, rotate, pages, watermark, encrypt, decrypt
├── ocr/
│   └── engine.py      ← ocr_image, ocr_pdf, make_searchable_pdf, batch_ocr
├── convert/
│   └── converter.py   ← convert, images_to_pdf, pdf_to_images
├── extract/
│   └── extractor.py   ← extract_text, extract_images, extract_metadata, extract_tables
├── image/
│   └── processor.py   ← enhance, deskew, denoise, resize, preprocess_for_ocr
├── batch/
│   └── processor.py   ← parallel batch processing
└── watch/
    └── watcher.py     ← watchdog-based directory monitor
```

---

## Supported Formats

| Category | Formats |
|----------|---------|
| Input documents | PDF, DOCX, ODT, MD, HTML, TXT, RST, EPUB |
| Input images | PNG, JPG/JPEG, TIFF/TIF, BMP, WebP |
| OCR output | TXT, JSON, Markdown |
| Table export | CSV, XLSX, JSON |
| Image export | PNG, JPEG, TIFF |

---

## License

MIT License — DocMax Contributors
