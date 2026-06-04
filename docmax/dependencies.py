from pathlib import Path

from rich.console import Console
from rich.table import Table
from shutil import which
from docmax.config_manager import get_tool_path

console = Console()


def has_pandoc():
    path = (
        get_tool_path("pandoc")
        or which("pandoc")
    )

    return path is not None

def has_tesseract():
    path = (
        get_tool_path("tesseract")
        or which("tesseract")
    )

    return path is not None

def has_pandoc():
    path = (
        get_tool_path("pandoc")
        or which("pandoc")
    )

    return path is not None

def has_ghostscript():
    path = (
        get_tool_path("ghostscript")
        or which("gswin64c")
        or which("gswin32c")
        or which("gs")
    )

    return path is not None
def has_poppler():
    path = (
        get_tool_path("poppler")
        or which("pdftotext")
    )

    return path is not None

def doctor():
    table = Table(title="DocMax System Check")

    table.add_column("Dependency")
    table.add_column("Status")

    deps = [
        ("Poppler", has_poppler()),
        ("Tesseract", has_tesseract()),
        ("Ghostscript", has_ghostscript()),
        ("Pandoc", has_pandoc()),
    ]

    for name, status in deps:
        table.add_row(
            name,
            "✓ Installed" if status else "✗ Missing",
        )

    console.print(table)


def check_poppler():
    if has_poppler():
        return True

    console.print(
        "\n[red]Poppler is required for PDF OCR.[/red]\n"
        "Run:\n"
        "[cyan]DocMax setup[/cyan]\n"
    )
    return False


def check_tesseract():
    if has_tesseract():
        return True

    console.print(
        "\n[red]Tesseract OCR is not installed.[/red]\n"
        "Run:\n"
        "[cyan]DocMax setup[/cyan]\n"
    )
    return False


def check_ghostscript():
    if has_ghostscript():
        return True

    console.print(
        "\n[red]Ghostscript is not installed.[/red]\n"
        "Run:\n"
        "[cyan]DocMax setup[/cyan]\n"
    )
    return False


def check_pandoc():
    if has_pandoc():
        return True

    console.print(
        "\n[red]Pandoc is not installed.[/red]\n"
        "Run:\n"
        "[cyan]DocMax setup[/cyan]\n"
    )
    return False