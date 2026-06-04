from pathlib import Path

import questionary

from dforge.batch import (
    batch_convert,
    batch_compress,
    batch_with_ocr
)

from dforge.menu import batch_menu
from dforge.workflows.common import select_folder


def batch_workflow():

    while True:

        choice = batch_menu()

        if choice == "Batch Convert":

            folder = select_folder()

            if not folder:
                continue

            target = questionary.select(
                "Convert documents to:",
                choices=[
                    "pdf",
                    "docx",
                    "md",
                ],
            ).ask()

            batch_convert(
                folder,
                target,
            )

        elif choice == "Batch Compress":

            folder = select_folder()

            if not folder:
                continue

            batch_compress(
                folder,
            )

        elif choice == "Batch OCR":

            folder = select_folder()

            if not folder:
                continue

            lang = questionary.text(
                "OCR language:",
                default="eng",
            ).ask()

            fmt = questionary.select(
                "Output format:",
                choices=[
                    "txt",
                    "pdf",
                ],
            ).ask()

            batch_with_ocr(
                folder,
                lang,
                fmt,
            )

        elif choice == "⬅ Back":
            break