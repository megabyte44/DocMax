from docmax.menu import extract_menu
from pathlib import Path

from docmax.menu import extract_menu
from docmax.extractor import (
    extract_text,
    extract_images,
    extract_metadata,
)

from docmax.workflows.common import (
    select_single_pdf,
    get_output_name,
    success_screen,
    failure_screen
)
def extract_workflow():

    while True:
        try:
            choice = extract_menu()

            # ==================================================
            # Extract Text
            # ==================================================

            if choice == "Extract Text":

                input_file = select_single_pdf()

                if not input_file:
                    continue

                output = get_output_name(
                    f"{input_file.stem}.txt"
                )

                if not output:
                    continue

                output_path = Path(output)

                extract_text(
                    input_file,
                    output_path,
                )

                success_screen(
                    "Text Extracted",
                    output_file=output_path.name,
                    extra_lines=[
                        f"Location : {output_path.resolve()}"
                    ]
                )

            # ==================================================
            # Extract Images
            # ==================================================

            elif choice == "Extract Images":

                input_file = select_single_pdf()

                if not input_file:
                    continue

                output_dir = (
                    input_file.parent
                    / f"{input_file.stem}_images"
                )

                extract_images(
                    input_file,
                    output_dir,
                )

                success_screen(
                    "Images Extracted",
                    extra_lines=[
                        f"Folder : {output_dir.resolve()}"
                    ]
                )

            # ==================================================
            # Extract Metadata
            # ==================================================

            elif choice == "Extract Metadata":

                input_file = select_single_pdf()

                if not input_file:
                    continue

                output = get_output_name(
                    f"{input_file.stem}_metadata.json"
                )

                if not output:
                    continue

                output_path = Path(output)

                extract_metadata(
                    input_file,
                    output_path,
                )

                success_screen(
                    "Metadata Extracted",
                    output_file=output_path.name,
                    extra_lines=[
                        f"Location : {output_path.resolve()}"
                    ]
                )

            # ==================================================
            # Back
            # ==================================================

            elif choice == "⬅ Back":
                break
        except Exception as e:
            failure_screen("Extraction Failed", str(e))