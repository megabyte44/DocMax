from pathlib import Path

import questionary
from rich.console import Console

from docmax.operations import compress

from docmax.workflows.common import (
    select_single_pdf,
    success_screen,
    get_output_name,
    failure_screen,
    show_file_info,
)

console = Console()


def compress_workflow():
    console.print("\n[bold cyan]Compress PDF[/bold cyan]\n")

    input_file = select_single_pdf()

    if not input_file:
        return

    show_file_info(input_file)

    preset = questionary.select(
    "Compression Quality",
    choices=[
        "ebook    - 📚 Recommended (~150 DPI)",
        "screen   - 📱 Smallest file (~72 DPI)",
        "printer  - 🖨 High quality (~300 DPI)",
        "prepress - 🏢 Professional print (~300+ DPI)",
        "default  - ⚖ Balanced",
    ],
    ).ask().split()[0]

    output = get_output_name(
        f"{input_file.stem}_compressed.pdf"
    )

    if not output:
        return

    output_path = Path(output)

    console.print(
        "\n[bold cyan]Compressing PDF...[/bold cyan]\n"
    )

    try:

        compress(
            input_file,
            output_path,
            preset,
        )

        success_screen(
            "Compression Complete",
            output_file=output_path.name,
            extra_lines=[
                f"Preset     : {preset}",
                f"Location   : {output_path.resolve()}",
            ],
        )

    except Exception as e:

        failure_screen(
            "Compression Failed",
            str(e),
        )

    next_action = questionary.select(
        "What next?",
        choices=[
            "Compress Another PDF",
            "Back to PDF Tools",
        ],
    ).ask()

    if next_action == "Compress Another PDF":
        compress_workflow()