#!/usr/bin/env python3
"""
Run a comprehensive smoke test against the DForge CLI.

This script creates test inputs, runs every CLI command, and checks outputs.
It skips steps that require missing external dependencies (Tesseract, Ghostscript,
Pandoc, Poppler) and reports a summary at the end.
"""

from __future__ import annotations

import argparse
import importlib
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def log(message: str) -> None:
    print(message, flush=True)


def module_available(name: str) -> bool:
    try:
        importlib.import_module(name)
        return True
    except Exception:
        return False


def ensure_module(name: str, package: str, auto_install: bool) -> bool:
    if module_available(name):
        return True
    if not auto_install:
        return False
    log(f"Installing missing Python package: {package}")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        log(result.stdout)
        log(result.stderr)
        return False
    return module_available(name)


def has_tool(*names: str) -> bool:
    return any(shutil.which(name) for name in names)


def resolve_cli(cli_arg: str | None) -> list[str]:
    if cli_arg:
        return shlex.split(cli_arg)
    if shutil.which("dforge"):
        return ["dforge"]
    return [sys.executable, "-m", "dforge.cli"]


def run_cmd(
    label: str,
    cmd: list[str],
    cwd: Path,
    expected_paths: list[Path] | None = None,
    timeout: int = 300,
) -> tuple[bool, str]:
    log("")
    log(f"==> {label}")
    log(f"$ {shlex.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        details = (result.stdout + "\n" + result.stderr).strip()
        return False, details
    if expected_paths:
        for path in expected_paths:
            if not path.exists():
                return False, f"Expected output not found: {path}"
            if path.is_file() and path.stat().st_size == 0:
                return False, f"Expected output is empty: {path}"
            if path.is_dir() and not any(path.iterdir()):
                return False, f"Expected directory is empty: {path}"
    return True, ""


def prepare_inputs(root: Path, auto_install: bool) -> dict[str, Path]:
    inputs_dir = root / "inputs"
    images_dir = inputs_dir / "images"
    pdfs_dir = inputs_dir / "pdfs"
    docs_dir = inputs_dir / "docs"
    img_pages_dir = images_dir / "pages"

    images_dir.mkdir(parents=True, exist_ok=True)
    pdfs_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    img_pages_dir.mkdir(parents=True, exist_ok=True)

    if not ensure_module("PIL", "Pillow", auto_install):
        raise RuntimeError("Pillow is required to generate test images.")

    from PIL import Image, ImageDraw

    test_ocr = images_dir / "test_ocr.png"
    img = Image.new("RGB", (600, 200), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((50, 70), "Hello DForge OCR Test 1234", fill="black")
    img.save(test_ocr)

    scan_img = images_dir / "scan.png"
    scan = Image.new("RGB", (800, 600), color="white")
    scan_draw = ImageDraw.Draw(scan)
    for i in range(5):
        scan_draw.text((80, 80 + i * 80), f"Line {i + 1}: Sample scanned text.", fill=(30, 30, 30))
    scan.save(scan_img)

    watermark_img = images_dir / "watermark.png"
    watermark = Image.new("RGBA", (200, 80), color=(0, 0, 0, 0))
    watermark_draw = ImageDraw.Draw(watermark)
    watermark_draw.text((10, 25), "DForge", fill=(255, 0, 0, 180))
    watermark.save(watermark_img)

    for i in range(1, 4):
        page_img = Image.new("RGB", (400, 300), color=(240, 240, 255))
        page_draw = ImageDraw.Draw(page_img)
        page_draw.text((150, 130), f"Page {i}", fill="black")
        page_img.save(img_pages_dir / f"page{i}.png")

    if not ensure_module("fpdf", "fpdf2", auto_install):
        raise RuntimeError("fpdf2 is required to generate test PDFs.")

    from fpdf import FPDF

    pdf_paths = []
    for name in ("a", "b", "c"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=24)
        pdf.cell(200, 10, txt=f"This is file {name}.pdf", ln=True)
        out_path = pdfs_dir / f"{name}.pdf"
        pdf.output(str(out_path))
        pdf_paths.append(out_path)

    table_pdf = pdfs_dir / "table_test.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.cell(60, 10, "Name", border=1)
    pdf.cell(60, 10, "Score", border=1)
    pdf.ln()
    pdf.cell(60, 10, "Alice", border=1)
    pdf.cell(60, 10, "95", border=1)
    pdf.ln()
    pdf.cell(60, 10, "Bob", border=1)
    pdf.cell(60, 10, "87", border=1)
    pdf.ln()
    pdf.output(str(table_pdf))

    image_pdf = pdfs_dir / "image_test.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.image(str(test_ocr), x=10, y=20, w=120)
    pdf.output(str(image_pdf))

    md_file = docs_dir / "test.md"
    md_file.write_text("# Hello DForge\n\nThis is a **test** document.\n\n- Item 1\n- Item 2\n", encoding="utf-8")

    return {
        "inputs_dir": inputs_dir,
        "images_dir": images_dir,
        "pdfs_dir": pdfs_dir,
        "docs_dir": docs_dir,
        "img_pages_dir": img_pages_dir,
        "test_ocr": test_ocr,
        "scan_img": scan_img,
        "watermark_img": watermark_img,
        "pdf_a": pdf_paths[0],
        "pdf_b": pdf_paths[1],
        "pdf_c": pdf_paths[2],
        "table_pdf": table_pdf,
        "image_pdf": image_pdf,
        "md_file": md_file,
    }


def preflight_imports() -> list[str]:
    expected = [
        "dforge.operations",
        "dforge.engine",
        "dforge.converter",
        "dforge.extractor",
        "dforge.processor",
        "dforge.batch",
        "dforge.watcher",
    ]
    missing = [mod for mod in expected if not module_available(mod)]
    return missing


def run_watch_test(
    label: str,
    cmd: list[str],
    drop_file: Path,
    expected_output: Path,
    watch_dir: Path,
    wait_seconds: int,
    cwd: Path,
) -> tuple[bool, str]:
    log("")
    log(f"==> {label}")
    log(f"$ {shlex.join(cmd)}")
    if expected_output.exists():
        if expected_output.is_dir():
            shutil.rmtree(expected_output, ignore_errors=True)
        else:
            expected_output.unlink(missing_ok=True)

    proc = subprocess.Popen(cmd, cwd=cwd)
    try:
        time.sleep(1.0)
        target = watch_dir / drop_file.name
        shutil.copy2(drop_file, target)
        time.sleep(wait_seconds)
        if not expected_output.exists():
            return False, f"Expected watch output not found: {expected_output}"
        if expected_output.is_file() and expected_output.stat().st_size == 0:
            return False, f"Expected watch output is empty: {expected_output}"
        if expected_output.is_dir() and not any(expected_output.iterdir()):
            return False, f"Expected watch output directory is empty: {expected_output}"
        return True, ""
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DForge CLI smoke tests.")
    parser.add_argument("--cli", help="CLI command prefix, e.g. 'dforge' or 'python -m dforge.cli'.")
    parser.add_argument("--work-dir", help="Directory to write test inputs/outputs. Defaults to a temp dir.")
    parser.add_argument("--keep", action="store_true", help="Keep the temporary work directory.")
    parser.add_argument("--auto-install", action="store_true", help="Auto-install fpdf2/Pillow if missing.")
    parser.add_argument("--skip-watch", action="store_true", help="Skip watch mode tests.")
    args = parser.parse_args()

    cli_base = resolve_cli(args.cli)
    repo_root = Path(__file__).resolve().parents[1]

    created_temp = False
    if args.work_dir:
        work_dir = Path(args.work_dir)
        work_dir.mkdir(parents=True, exist_ok=True)
    else:
        work_dir = Path(tempfile.mkdtemp(prefix="dforge_cli_tests_"))
        created_temp = True

    out_dir = work_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    missing_imports = preflight_imports()
    if missing_imports:
        log("WARNING: CLI imports refer to missing modules in this workspace:")
        for mod in missing_imports:
            log(f"  - {mod}")
        log("CLI commands may fail until this mismatch is resolved.\n")

    try:
        inputs = prepare_inputs(work_dir, args.auto_install)
    except Exception as exc:
        log(str(exc))
        return 1

    has_tesseract = has_tool("tesseract")
    has_ghostscript = has_tool("gs", "gswin64c", "gswin32c")
    has_pandoc = has_tool("pandoc")
    has_poppler = has_tool("pdftoppm", "pdftocairo")

    ocr_deps = has_tesseract and module_available("pytesseract")
    ocr_pdf_deps = ocr_deps and has_poppler and module_available("pdf2image")
    searchable_deps = ocr_pdf_deps
    pdf2img_deps = has_poppler and module_available("pdf2image")
    cv2_deps = module_available("cv2")
    pypdf_deps = module_available("pypdf")
    img2pdf_deps = module_available("img2pdf")
    pdfplumber_deps = module_available("pdfplumber")
    pandas_deps = module_available("pandas")
    openpyxl_deps = module_available("openpyxl")

    results: list[tuple[str, str, str]] = []

    def record(status: str, label: str, details: str = "") -> None:
        results.append((status, label, details))

    def maybe_run(label: str, args_list: list[str], expected: list[Path] | None = None) -> None:
        ok, details = run_cmd(label, cli_base + args_list, cwd=repo_root, expected_paths=expected)
        if ok:
            record("PASS", label)
        else:
            record("FAIL", label, details)

    def skip(label: str, reason: str) -> None:
        record("SKIP", label, reason)

    # Version and help
    maybe_run("version", ["--version"])
    maybe_run("help", ["--help"])

    merged_pdf = out_dir / "merged.pdf"
    split_dir = out_dir / "split_pages"
    compressed_pdf = out_dir / "compressed.pdf"
    rotated_pdf = out_dir / "rotated.pdf"
    pages_pdf = out_dir / "pages_1_2.pdf"
    watermarked_pdf = out_dir / "watermarked.pdf"
    encrypted_pdf = out_dir / "encrypted.pdf"
    decrypted_pdf = out_dir / "decrypted.pdf"

    if pypdf_deps:
        maybe_run(
            "merge",
            ["merge", str(inputs["pdf_a"]), str(inputs["pdf_b"]), str(inputs["pdf_c"]), "-o", str(merged_pdf)],
            expected=[merged_pdf],
        )
    else:
        skip("merge", "pypdf not available")

    if pypdf_deps and merged_pdf.exists():
        from pypdf import PdfReader

        try:
            merged_pages = len(PdfReader(str(merged_pdf)).pages)
            if merged_pages == 3:
                record("PASS", "verify-merge-pages")
            else:
                record("FAIL", "verify-merge-pages", f"Expected 3 pages, got {merged_pages}")
        except Exception as exc:
            record("FAIL", "verify-merge-pages", str(exc))
    else:
        skip("verify-merge-pages", "pypdf not available")

    if pypdf_deps:
        maybe_run(
            "split",
            ["split", str(merged_pdf), "--output-dir", str(split_dir)],
            expected=[split_dir],
        )
    else:
        skip("split", "pypdf not available")

    if has_ghostscript:
        maybe_run(
            "compress",
            ["compress", str(merged_pdf), "-o", str(compressed_pdf), "--preset", "ebook"],
            expected=[compressed_pdf],
        )
    else:
        skip("compress", "Ghostscript not found")

    if pypdf_deps:
        maybe_run(
            "rotate",
            ["rotate", str(merged_pdf), "90", "-o", str(rotated_pdf)],
            expected=[rotated_pdf],
        )
    else:
        skip("rotate", "pypdf not available")

    if pypdf_deps:
        maybe_run(
            "pages",
            ["pages", str(merged_pdf), "1-2", "-o", str(pages_pdf)],
            expected=[pages_pdf],
        )
    else:
        skip("pages", "pypdf not available")

    if pypdf_deps:
        maybe_run(
            "watermark",
            ["watermark", str(merged_pdf), str(inputs["watermark_img"]), "-o", str(watermarked_pdf)],
            expected=[watermarked_pdf],
        )
    else:
        skip("watermark", "pypdf not available")

    if pypdf_deps:
        maybe_run(
            "encrypt",
            ["encrypt", str(merged_pdf), "-o", str(encrypted_pdf), "--password", "testpass"],
            expected=[encrypted_pdf],
        )
    else:
        skip("encrypt", "pypdf not available")

    if pypdf_deps and encrypted_pdf.exists():
        from pypdf import PdfReader

        try:
            encrypted = PdfReader(str(encrypted_pdf))
            if encrypted.is_encrypted:
                record("PASS", "verify-encrypted")
            else:
                record("FAIL", "verify-encrypted", "Encrypted PDF is not marked as encrypted")
        except Exception as exc:
            record("FAIL", "verify-encrypted", str(exc))
    else:
        skip("verify-encrypted", "pypdf not available")

    if pypdf_deps:
        maybe_run(
            "decrypt",
            ["decrypt", str(encrypted_pdf), "-o", str(decrypted_pdf), "--password", "testpass"],
            expected=[decrypted_pdf],
        )
    else:
        skip("decrypt", "pypdf not available")

    metadata_json = out_dir / "metadata.json"
    if pypdf_deps:
        maybe_run("metadata", ["metadata", str(merged_pdf)])
        maybe_run(
            "metadata-json",
            ["metadata", str(merged_pdf), "-o", str(metadata_json)],
            expected=[metadata_json],
        )
    else:
        skip("metadata", "pypdf not available")
        skip("metadata-json", "pypdf not available")

    text_out = out_dir / "extracted.txt"
    if pypdf_deps:
        maybe_run(
            "text",
            ["text", str(merged_pdf), "-o", str(text_out)],
            expected=[text_out],
        )
    else:
        skip("text", "pypdf not available")

    images_out = out_dir / "extracted_images"
    if pypdf_deps:
        maybe_run(
            "images",
            ["images", str(inputs["image_pdf"]), "--output-dir", str(images_out)],
            expected=[images_out],
        )
    else:
        skip("images", "pypdf not available")

    tables_csv_dir = out_dir / "tables_csv"
    tables_json = out_dir / "tables.json"
    tables_xlsx = out_dir / "tables.xlsx"
    if pdfplumber_deps:
        if pandas_deps:
            maybe_run(
                "tables-csv",
                ["tables", str(inputs["table_pdf"]), "--fmt", "csv", "-o", str(tables_csv_dir)],
                expected=[tables_csv_dir],
            )
        else:
            skip("tables-csv", "pandas not available")

        maybe_run(
            "tables-json",
            ["tables", str(inputs["table_pdf"]), "--fmt", "json", "-o", str(tables_json)],
            expected=[tables_json],
        )

        if pandas_deps and openpyxl_deps:
            maybe_run(
                "tables-xlsx",
                ["tables", str(inputs["table_pdf"]), "--fmt", "xlsx", "-o", str(tables_xlsx)],
                expected=[tables_xlsx],
            )
        elif not pandas_deps:
            skip("tables-xlsx", "pandas not available")
        else:
            skip("tables-xlsx", "openpyxl not available")
    else:
        skip("tables-csv", "pdfplumber not available")
        skip("tables-json", "pdfplumber not available")
        skip("tables-xlsx", "pdfplumber not available")

    ocr_txt = out_dir / "ocr_result.txt"
    ocr_json = out_dir / "ocr_result.json"
    ocr_md = out_dir / "ocr_result.md"
    ocr_pdf_txt = out_dir / "ocr_pdf.txt"

    if ocr_deps:
        maybe_run(
            "ocr-image-txt",
            ["ocr", str(inputs["test_ocr"]), "-o", str(ocr_txt)],
            expected=[ocr_txt],
        )
        maybe_run(
            "ocr-image-json",
            ["ocr", str(inputs["test_ocr"]), "--fmt", "json", "-o", str(ocr_json)],
            expected=[ocr_json],
        )
        maybe_run(
            "ocr-image-md",
            ["ocr", str(inputs["test_ocr"]), "--fmt", "md", "-o", str(ocr_md)],
            expected=[ocr_md],
        )
    else:
        skip("ocr-image-txt", "Tesseract or pytesseract not available")
        skip("ocr-image-json", "Tesseract or pytesseract not available")
        skip("ocr-image-md", "Tesseract or pytesseract not available")

    if ocr_pdf_deps:
        maybe_run(
            "ocr-pdf",
            ["ocr", str(merged_pdf), "-o", str(ocr_pdf_txt)],
            expected=[ocr_pdf_txt],
        )
    else:
        skip("ocr-pdf", "Tesseract, pytesseract, or Poppler not available")

    searchable_pdf = out_dir / "searchable.pdf"
    if searchable_deps:
        maybe_run(
            "searchable",
            ["searchable", str(merged_pdf), "-o", str(searchable_pdf)],
            expected=[searchable_pdf],
        )
    else:
        skip("searchable", "Tesseract, pytesseract, or Poppler not available")

    batch_ocr_dir = work_dir / "batch_ocr"
    batch_ocr_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(inputs["test_ocr"], batch_ocr_dir / "img1.png")
    shutil.copy2(inputs["scan_img"], batch_ocr_dir / "img2.png")
    if ocr_deps:
        maybe_run(
            "batch-ocr",
            ["batch-ocr", str(batch_ocr_dir), "--fmt", "txt"],
            expected=[batch_ocr_dir],
        )
    else:
        skip("batch-ocr", "Tesseract or pytesseract not available")

    if has_pandoc:
        html_out = out_dir / "test.html"
        docx_out = out_dir / "test.docx"
        txt_out = out_dir / "test.txt"
        maybe_run(
            "convert-html",
            ["convert", str(inputs["md_file"]), "html", "-o", str(html_out)],
            expected=[html_out],
        )
        maybe_run(
            "convert-docx",
            ["convert", str(inputs["md_file"]), "docx", "-o", str(docx_out)],
            expected=[docx_out],
        )
        maybe_run(
            "convert-txt",
            ["convert", str(inputs["md_file"]), "txt", "-o", str(txt_out)],
            expected=[txt_out],
        )
    else:
        skip("convert-html", "Pandoc not found")
        skip("convert-docx", "Pandoc not found")
        skip("convert-txt", "Pandoc not found")

    img2pdf_out = out_dir / "from_images.pdf"
    if img2pdf_deps:
        maybe_run(
            "img2pdf",
            ["img2pdf", str(inputs["img_pages_dir"]), "-o", str(img2pdf_out)],
            expected=[img2pdf_out],
        )
    else:
        skip("img2pdf", "img2pdf not available")

    pdf2img_dir = out_dir / "pdf_images"
    if pdf2img_deps:
        maybe_run(
            "pdf2img",
            ["pdf2img", str(merged_pdf), "--output-dir", str(pdf2img_dir), "--dpi", "150", "--fmt", "png"],
            expected=[pdf2img_dir],
        )
    else:
        skip("pdf2img", "Poppler not found")

    enhanced = out_dir / "scan_enhanced.png"
    deskewed = out_dir / "scan_deskewed.png"
    denoised = out_dir / "scan_denoised.png"
    resized_w = out_dir / "scan_400w.png"
    resized_s = out_dir / "scan_half.png"
    resized_wh = out_dir / "scan_640x480.png"
    preprocessed = out_dir / "scan_preprocessed.png"

    maybe_run(
        "enhance",
        ["enhance", str(inputs["scan_img"]), "-o", str(enhanced)],
        expected=[enhanced],
    )

    if cv2_deps:
        maybe_run(
            "deskew",
            ["deskew", str(inputs["scan_img"]), "-o", str(deskewed)],
            expected=[deskewed],
        )
        maybe_run(
            "denoise",
            ["denoise", str(inputs["scan_img"]), "-o", str(denoised)],
            expected=[denoised],
        )
    else:
        skip("deskew", "opencv-python-headless not available")
        skip("denoise", "opencv-python-headless not available")

    maybe_run(
        "resize-width",
        ["resize", str(inputs["scan_img"]), "--width", "400", "-o", str(resized_w)],
        expected=[resized_w],
    )
    maybe_run(
        "resize-scale",
        ["resize", str(inputs["scan_img"]), "--scale", "0.5", "-o", str(resized_s)],
        expected=[resized_s],
    )
    maybe_run(
        "resize-width-height",
        ["resize", str(inputs["scan_img"]), "--width", "640", "--height", "480", "-o", str(resized_wh)],
        expected=[resized_wh],
    )

    if cv2_deps:
        maybe_run(
            "preprocess",
            ["preprocess", str(inputs["scan_img"]), "-o", str(preprocessed)],
            expected=[preprocessed],
        )
    else:
        skip("preprocess", "opencv-python-headless not available")

    batch_pdf_dir = work_dir / "batch_pdf"
    batch_pdf_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(inputs["pdf_a"], batch_pdf_dir / "a.pdf")
    shutil.copy2(inputs["pdf_b"], batch_pdf_dir / "b.pdf")
    shutil.copy2(inputs["pdf_c"], batch_pdf_dir / "c.pdf")

    if has_ghostscript:
        maybe_run(
            "batch-compress",
            ["batch", str(batch_pdf_dir), "--compress", "--workers", "2"],
            expected=[batch_pdf_dir],
        )
    else:
        skip("batch-compress", "Ghostscript not found")

    if ocr_deps:
        maybe_run(
            "batch-ocr-flag",
            ["batch", str(batch_ocr_dir), "--ocr", "--fmt", "txt", "--workers", "2"],
            expected=[batch_ocr_dir],
        )
    else:
        skip("batch-ocr-flag", "Tesseract or pytesseract not available")

    batch_md_dir = work_dir / "batch_md"
    batch_md_dir.mkdir(parents=True, exist_ok=True)
    (batch_md_dir / "doc1.md").write_text("# Doc 1\nContent here", encoding="utf-8")
    (batch_md_dir / "doc2.md").write_text("# Doc 2\nMore content", encoding="utf-8")

    if has_pandoc:
        maybe_run(
            "batch-convert",
            ["batch", str(batch_md_dir), "--convert", "html", "--workers", "2"],
            expected=[batch_md_dir],
        )
    else:
        skip("batch-convert", "Pandoc not found")

    if not args.skip_watch:
        watch_dir = work_dir / "watch"
        watch_dir.mkdir(parents=True, exist_ok=True)

        if ocr_deps:
            expected = watch_dir / "test_ocr.txt"
            ok, details = run_watch_test(
                "watch-ocr",
                cli_base + ["watch", str(watch_dir), "--ocr", "--fmt", "txt"],
                drop_file=inputs["test_ocr"],
                expected_output=expected,
                watch_dir=watch_dir,
                wait_seconds=8,
                cwd=repo_root,
            )
            record("PASS" if ok else "FAIL", "watch-ocr", details)
        else:
            skip("watch-ocr", "Tesseract or pytesseract not available")

        if has_ghostscript:
            expected = watch_dir / "a_compressed.pdf"
            ok, details = run_watch_test(
                "watch-compress",
                cli_base + ["watch", str(watch_dir), "--compress"],
                drop_file=inputs["pdf_a"],
                expected_output=expected,
                watch_dir=watch_dir,
                wait_seconds=6,
                cwd=repo_root,
            )
            record("PASS" if ok else "FAIL", "watch-compress", details)
        else:
            skip("watch-compress", "Ghostscript not found")

        if searchable_deps:
            expected = watch_dir / "a_searchable.pdf"
            ok, details = run_watch_test(
                "watch-searchable",
                cli_base + ["watch", str(watch_dir), "--searchable"],
                drop_file=inputs["pdf_a"],
                expected_output=expected,
                watch_dir=watch_dir,
                wait_seconds=8,
                cwd=repo_root,
            )
            record("PASS" if ok else "FAIL", "watch-searchable", details)
        else:
            skip("watch-searchable", "Tesseract, pytesseract, or Poppler not available")

        if cv2_deps:
            expected = watch_dir / "scan_preprocessed.png"
            ok, details = run_watch_test(
                "watch-preprocess",
                cli_base + ["watch", str(watch_dir), "--preprocess"],
                drop_file=inputs["scan_img"],
                expected_output=expected,
                watch_dir=watch_dir,
                wait_seconds=6,
                cwd=repo_root,
            )
            record("PASS" if ok else "FAIL", "watch-preprocess", details)
        else:
            skip("watch-preprocess", "opencv-python-headless not available")
    else:
        skip("watch-ocr", "--skip-watch")
        skip("watch-compress", "--skip-watch")
        skip("watch-searchable", "--skip-watch")
        skip("watch-preprocess", "--skip-watch")

    passed = [r for r in results if r[0] == "PASS"]
    failed = [r for r in results if r[0] == "FAIL"]
    skipped = [r for r in results if r[0] == "SKIP"]

    log("\n=== Summary ===")
    log(f"PASS: {len(passed)}  FAIL: {len(failed)}  SKIP: {len(skipped)}")

    if failed:
        log("\nFailures:")
        for _, label, details in failed:
            log(f"- {label}")
            if details:
                log(details)

    if skipped:
        log("\nSkipped:")
        for _, label, reason in skipped:
            log(f"- {label}: {reason}")

    if created_temp and not args.keep:
        shutil.rmtree(work_dir, ignore_errors=True)
    else:
        log(f"\nOutputs kept at: {work_dir}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
