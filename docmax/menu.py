import questionary


def show_menu(title: str, choices: list[str]):
    return questionary.select(
        title,
        choices=choices,
    ).ask()


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
    return show_menu(
        "PDF Tools",
        [
            "📑 Merge PDFs",
            "✂ Split PDF",
            "🗜 Compress PDF",
            "🔄 Rotate PDF",
            "📄 Extract Pages",
            "💧 Watermark PDF",
            "🔒 Encrypt PDF",
            "🔓 Decrypt PDF",
            "⬅ Back",
        ],
    )


def ocr_menu():
    return show_menu(
        "OCR Tools",
        [
            "🔍 OCR Image/PDF",
            "📄 Searchable PDF",
            "⚡ Batch OCR",
            "📁 OCR Folder",
            "📊 Extract Tables",
            "⚙ OCR Settings",
            "⬅ Back",
        ],
    )


def conversion_menu():
    return show_menu(
        "Conversion Tools",
        [
            "📝 Markdown → PDF",
            "📝 Markdown → DOCX",
            "📄 DOCX → PDF",
            "📄 DOCX → Markdown",
            "🖼 Images → PDF",
            "📑 PDF → Images",
            "⬅ Back",
        ],
    )


def extract_menu():
    return show_menu(
        "Extract Tools",
        [
            "📜 Extract Text",
            "🖼 Extract Images",
            "🏷 Extract Metadata",
            "⬅ Back",
        ],
    )


def batch_menu():
    return show_menu(
        "Batch Tools",
        [
            "🔄 Batch Convert",
            "🗜 Batch Compress",
            "⚡ Batch OCR",
            "⬅ Back",
        ],
    )


def image_menu():
    return show_menu(
        "Image Tools",
        [
            "📏 Resize Images",
            "🔄 Convert Format",
            "🗜 Compress Images",
            "↩ Rotate Images",
            "✂ Crop Images",
            "↔ Flip Horizontal",
            "↕ Flip Vertical",
            "💧 Watermark Images",
            "🪄 Remove Background",
            "⬅ Back",
        ],
    )


def automation_menu():
    return show_menu(
        "Automation Tools",
        [
            "🤖 Auto OCR",
            "📄 Auto Searchable PDF",
            "🗜 Auto Compress PDF",
            "🪄 Auto Preprocess Images",
            "⬅ Back",
        ],
    )


def settings_menu():
    return show_menu(
        "Settings",
        [
            "⚙ OCR Settings",
            "🩺 System Check",
            "🚀 Run Setup",
            "📂 Show Tool Paths",
            "⬅ Back",
        ],
    )