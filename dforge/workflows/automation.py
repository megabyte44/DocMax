from pathlib import Path

import questionary

from dforge.menu import automation_menu
from dforge.watcher import watch


def automation_workflow():

    while True:

        choice = automation_menu()

        if choice == "Auto OCR":

            folder = questionary.path(
                "Folder to watch:"
            ).ask()

            if not folder:
                continue

            fmt = questionary.select(
                "Output format:",
                choices=[
                    "txt",
                    "pdf"
                ]
            ).ask()

            lang = questionary.text(
                "OCR language:",
                default="eng"
            ).ask()

            watch(
                Path(folder),
                action="ocr",
                lang=lang,
                fmt=fmt
            )

        elif choice == "Auto Searchable PDF":

            folder = questionary.path(
                "Folder to watch:"
            ).ask()

            if not folder:
                continue

            lang = questionary.text(
                "OCR language:",
                default="eng"
            ).ask()

            watch(
                Path(folder),
                action="searchable",
                lang=lang
            )

        elif choice == "Auto Compress PDF":

            folder = questionary.path(
                "Folder to watch:"
            ).ask()

            if not folder:
                continue

            watch(
                Path(folder),
                action="compress"
            )

        elif choice == "Auto Preprocess Images":

            folder = questionary.path(
                "Folder to watch:"
            ).ask()

            if not folder:
                continue

            watch(
                Path(folder),
                action="preprocess"
            )

        elif choice == "⬅ Back":
            break