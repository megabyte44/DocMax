from rich.console import Console
from rich.panel import Panel

console = Console()


def show_install_help():
    console.print(
        Panel(
            """
[bold cyan]DocMax Installation Options[/bold cyan]

[yellow]Core:[/yellow]
pip install docmax

[yellow]OCR Support:[/yellow]
pip install "docmax[ocr]"

[yellow]Image Processing:[/yellow]
pip install "docmax[image]"

[yellow]Table Extraction:[/yellow]
pip install "docmax[tables]"

[yellow]Everything:[/yellow]
pip install "docmax[full]"
""",
            title="Install Extras",
            border_style="cyan",
        )
    )