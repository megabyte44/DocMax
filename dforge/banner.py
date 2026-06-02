from rich.console import Console
from rich.panel import Panel
from rich.align import Align

console = Console()


def show_banner():
    title = """
⚡ DFORGE

Fast Local Document Automation
"""

    console.print()

    console.print(
        Panel(
            Align.center(f"[bold cyan]{title}[/bold cyan]"),
            border_style="cyan",
            padding=(1, 4),
        )
    )

    console.print(
        Align.center(
            "[dim]Forge your documents from your terminal[/dim]"
        )
    )

    console.print()