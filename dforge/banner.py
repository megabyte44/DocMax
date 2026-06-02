from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel
from rich.align import Align


console = Console()


def show_banner():
    fig = Figlet(font="slant")

    banner = fig.renderText("DForge")

    console.print(
        Panel(
            Align.center(f"[bold cyan]{banner}[/bold cyan]"),
            title="[bold green]v1.0.0[/bold green]",
            subtitle="[dim]Forge your documents from your terminal[/dim]",
            border_style="cyan",
        )
    )