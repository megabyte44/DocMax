# DForge — Forge your documents from your terminal.

A unified, offline-first Python CLI for all your document processing needs.

---

## Installation

```bash
pip install dforge
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
dforge merge a.pdf b.pdf c.pdf -o merged.pdf

# Split into pages
dforge split report.pdf

# Compress (uses Ghostscript)
dforge compress large.pdf --preset ebook

# Rotate pages
dforge rotate file.pdf 90

# Extract page range
dforge pages file.pdf 1-5

# Watermark
dforge watermark file.pdf logo.png

# Encrypt / Decrypt
dforge encrypt file.pdf
dforge decrypt protected.pdf
```

### OCR

```bash
# OCR an image
dforge ocr scan.png

# OCR a PDF
dforge ocr scan.pdf

# Output as JSON or Markdown
dforge ocr scan.pdf --fmt json
dforge ocr scan.pdf --fmt md

# Multi-language OCR
dforge ocr scan.png --lang eng+hin

# Make a scanned PDF searchable
dforge searchable scan.pdf

# Batch OCR an entire folder
dforge batch-ocr invoices/
```

### Document Conversion

```bash
# Convert DOCX → PDF
dforge convert report.docx pdf

# Convert Markdown → HTML
dforge convert notes.md html

# Combine images into a PDF
dforge img2pdf scans/

# Export PDF pages as images
dforge pdf2img report.pdf --dpi 300 --fmt png
```

### Content Extraction

```bash
# Extract text
dforge text report.pdf

# Extract embedded images
dforge images report.pdf

# Show / save metadata
dforge metadata report.pdf
dforge metadata report.pdf -o meta.json

# Extract tables
dforge tables invoice.pdf --fmt xlsx
dforge tables invoice.pdf --fmt csv
dforge tables invoice.pdf --fmt json
```

### Image Processing

```bash
# Enhance (contrast + sharpness)
dforge enhance scan.png

# Fix skewed scans
dforge deskew scan.png

# Remove noise
dforge denoise scan.png

# Resize
dforge resize photo.png --width 800
dforge resize photo.png --scale 0.5

# Full OCR preprocessing pipeline
dforge preprocess scan.png
```

### Batch Processing

```bash
# Batch OCR with 8 workers
dforge batch ./documents --ocr --workers 8

# Batch compress
dforge batch ./pdfs --compress

# Batch convert to markdown
dforge batch ./docs --convert md
```

### Watch Mode

```bash
# Auto-OCR new files dropped into a folder
dforge watch ./incoming --ocr

# Auto-make-searchable
dforge watch ./scans --searchable

# Auto-compress
dforge watch ./uploads --compress
```

---

## Project Structure

```
dforge/
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

MIT License — DForge Contributors
