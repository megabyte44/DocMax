from pathlib import Path

import questionary
from rich.console import Console
from docmax.loading import Loader
from docmax.engine import ocr_image, ocr_pdf
from docmax.dependencies import has_poppler
from docmax.workflows.common import (
    failure_screen,
    success_screen,
    get_output_name,
)
from docmax.dependencies import (
    check_poppler,
    check_tesseract,
)

console = Console()




def ocr_workflow():
    if not check_tesseract():
        return
    
    input_file = questionary.path(
        "Image or PDF file:"
    ).ask()

    if not input_file:
        return

    input_file = Path(input_file)

    if input_file.suffix.lower() == ".pdf":
        if not check_poppler():
            return
    console.print("\n[bold cyan]OCR Image / PDF[/bold cyan]\n")


    lang = questionary.text(
        "OCR Language(s)",
        default="eng",
    ).ask()

    fmt = questionary.select(
        "Output Format",
        choices=[
            "txt",
            "json",
            "md",
        ],
    ).ask()

    output = get_output_name(
        f"{input_file.stem}_ocr.{fmt}"
    )

    if not output:
        return

    output_path = Path(output)

    try:
        with Loader("Running OCR..."):

            if input_file.suffix.lower() == ".pdf":
                ocr_pdf(
                    input_file,
                    output_path,
                    lang,
                    fmt,
                )
            else:
                ocr_image(
                    input_file,
                    output_path,
                    lang,
                    fmt,
                )

        success_screen(
            "OCR Complete",
            output_file=output_path.name,
            extra_lines=[
                f"Format : {fmt}",
                f"Lang   : {lang}",
            ],
        )
    except Exception as e:
        failure_screen("OCR Failed", str(e))
    if not has_poppler():
        console.print(
            "[red]Poppler not installed.[/red]"
        )
        return