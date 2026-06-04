from rich.console import Console

from docmax.operations import split

from docmax.workflows.common import (
    select_single_pdf,
    success_screen,
    failure_screen
)

console = Console()


def split_workflow():
    console.print("\n[bold cyan]Split PDF[/bold cyan]\n")

    pdf = select_single_pdf()

    if not pdf:
        return

    console.print(
        "\n[bold cyan]Splitting PDF...[/bold cyan]\n"
    )

    
    try:
        split(pdf)
        success_screen(
                "Split Complete",
                extra_lines=[
                    f"Source : {pdf.name}",
                ],
            )
    except Exception as e:
        failure_screen("Split Failed", str(e))