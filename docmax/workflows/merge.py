from pathlib import Path

import questionary
from rich.console import Console

from docmax.operations import merge

from docmax.workflows.common import (
    select_multiple_pdfs,
    show_file_info,
    success_screen,
    get_output_name,
    failure_screen,
)

console = Console()


def merge_workflow():
    console.print("\n[bold cyan]Merge PDFs[/bold cyan]\n")

    folder, selected = select_multiple_pdfs()
    for pdf in selected:
        show_file_info(folder / pdf)
    if not folder or not selected:
        return

    if len(selected) < 2:
        console.print(
            "[red]Select at least 2 PDFs.[/red]"
        )
        return

    console.print("\n[bold cyan]Selected PDFs[/bold cyan]\n")

    for i, pdf in enumerate(selected, start=1):
        console.print(f"{i}. {pdf}")

    console.print(
        f"\n[green]Total PDFs:[/green] {len(selected)}\n"
    )

    if not questionary.confirm(
        "Continue?",
        default=True,
    ).ask():
        return

    sort_mode = questionary.select(
        "Sort PDFs before merging?",
        choices=[
            "Keep Current Order",
            "Alphabetical",
            "Reverse Alphabetical",
        ],
    ).ask()

    if sort_mode == "Alphabetical":
        selected.sort()

    elif sort_mode == "Reverse Alphabetical":
        selected.sort(reverse=True)

    output = get_output_name(
        f"merged_{len(selected)}_files.pdf"
    )

    if not output:
        return

    output_path = Path(output)

    if output_path.exists():

        overwrite = questionary.confirm(
            f"{output} already exists. Overwrite?",
            default=False,
        ).ask()

        if not overwrite:
            return

    console.print(
        "\n[bold cyan]Merging PDFs...[/bold cyan]\n"
    )

    inputs = [
        folder / pdf
        for pdf in selected
    ]

    try:

        merge(
            inputs,
            output_path,
        )

        success_screen(
            "Merge Complete",
            output_file=output_path.name,
            extra_lines=[
                f"Input Files : {len(selected)}",
                f"Location    : {output_path.resolve()}",
            ],
        )

    except Exception as e:

        failure_screen(
            "Merge Failed",
            str(e),
        )

    next_action = questionary.select(
        "What next?",
        choices=[
            "Merge More PDFs",
            "Back to PDF Tools",
        ],
    ).ask()

    if next_action == "Merge More PDFs":
        merge_workflow()