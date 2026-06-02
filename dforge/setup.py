from setuptools import setup, find_packages

setup(
    name="dforge",
    version="1.0.0",
    description="DForge - Forge your documents from your terminal.",
    author="DForge Contributors",
    packages=find_packages(),
    install_requires=[
        "typer[all]>=0.9.0",
        "pypdf>=3.0.0",
        "pikepdf>=8.0.0",
        "pytesseract>=0.3.10",
        "Pillow>=10.0.0",
        "opencv-python-headless>=4.8.0",
        "img2pdf>=0.4.4",
        "pdf2image>=1.16.3",
        "watchdog>=3.0.0",
        "tqdm>=4.66.0",
        "rich>=13.0.0",
        "pdfplumber>=0.10.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "dforge=dforge.cli:app",
        ],
    },
    python_requires=">=3.9",
)
