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
            "⚡ Batch Processing",
            "👀 Watch Folder",
            "⚙ Settings",
            "❌ Exit",
        ],
    )


def pdf_menu():
    return show_menu(
        "PDF Tools",
        [
            "Merge PDFs",
            "Split PDF",
            "Compress PDF",
            "Rotate PDF",
            "Extract Pages",
            "Encrypt PDF",
            "Decrypt PDF",
            "⬅ Back",
        ],
    )
def ocr_menu():
    return show_menu(
        "OCR Tools",
        [
            "OCR Image/PDF",
            "Searchable PDF",
            "Batch OCR",
            "OCR Folder",
            "Watch Folder",
            "Extract Tables",
            "OCR Settings",
            "⬅ Back",
        ],
    )