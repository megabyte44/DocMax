import questionary


def show_menu(title: str, choices: list[str]):
    return questionary.select(
        title,
        choices=choices,
    ).ask()


PDF_MENU = {
    "📑 Merge PDFs": "merge",
    "✂ Split PDF": "split",
    "🗜 Compress PDF": "compress",
    "🔄 Rotate PDF": "rotate",
    "📄 Extract Pages": "pages",
    "💧 Watermark PDF": "watermark",
    "🔒 Encrypt PDF": "encrypt",
    "🔓 Decrypt PDF": "decrypt",
    "⬅ Back": None,
}

OCR_MENU = {
    "🔍 OCR Image/PDF": "ocr",
    "📄 Searchable PDF": "searchable",
    "⚡ Batch OCR": "batch_ocr",
    "📁 OCR Folder": "ocr_folder",
    "📊 Extract Tables": "tables",
    "⚙ OCR Settings": "settings",
    "⬅ Back": None,
}

CONVERSION_MENU = {
    "📝 Markdown → PDF": "md2pdf",
    "📝 Markdown → DOCX": "md2docx",
    "📄 DOCX → PDF": "docx2pdf",
    "📄 DOCX → Markdown": "docx2md",
    "🖼 Images → PDF": "img2pdf",
    "📑 PDF → Images": "pdf2img",
    "⬅ Back": None,
}

EXTRACT_MENU = {
    "📜 Extract Text": "text",
    "🖼 Extract Images": "images",
    "🏷 Extract Metadata": "metadata",
    "⬅ Back": None,
}

BATCH_MENU = {
    "🔄 Batch Convert": "convert",
    "🗜 Batch Compress": "compress",
    "⚡ Batch OCR": "ocr",
    "⬅ Back": None,
}

IMAGE_MENU = {
    "📏 Resize Images": "resize",
    "🔄 Convert Format": "convert",
    "🗜 Compress Images": "compress",
    "↩ Rotate Images": "rotate",
    "✂ Crop Images": "crop",
    "↔ Flip Horizontal": "flip_h",
    "↕ Flip Vertical": "flip_v",
    "💧 Watermark Images": "watermark",
    "🪄 Remove Background": "remove_bg",
    "⬅ Back": None,
}

AUTOMATION_MENU = {
    "🤖 Auto OCR": "ocr",
    "📄 Auto Searchable PDF": "searchable",
    "🗜 Auto Compress PDF": "compress",
    "🪄 Auto Preprocess Images": "preprocess",
    "⬅ Back": None,
}

SETTINGS_MENU = {
    "⚙ OCR Settings": "ocr_settings",
    "🩺 System Check": "doctor",
    "🚀 Run Setup": "setup",
    "📂 Show Tool Paths": "paths",
    "⬅ Back": None,
}


def main_menu():
    return show_menu(
        "What would you like to do?",
        [
            "📄 PDF Tools",
            "🔍 OCR",
            "🔄 Conversion",
            "🖼 Image Processing",
            "📂 Extract",
            "⚡ Batch Processing",
            "👀 Watch Folder",
            "⚙ Settings",
            "📦 Install Guide",
            "❌ Exit",
        ],
    )


def pdf_menu():
    return show_menu("PDF Tools", list(PDF_MENU.keys()))


def ocr_menu():
    return show_menu("OCR Tools", list(OCR_MENU.keys()))


def conversion_menu():
    return show_menu("Conversion Tools", list(CONVERSION_MENU.keys()))


def extract_menu():
    return show_menu("Extract Tools", list(EXTRACT_MENU.keys()))


def batch_menu():
    return show_menu("Batch Tools", list(BATCH_MENU.keys()))


def image_menu():
    return show_menu("Image Tools", list(IMAGE_MENU.keys()))


def automation_menu():
    return show_menu("Automation Tools", list(AUTOMATION_MENU.keys()))


def settings_menu():
    return show_menu("Settings", list(SETTINGS_MENU.keys()))