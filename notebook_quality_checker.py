"""
Jupyter Notebook Quality Checker

Basis:
This script was developed by combining ideas from:
1. Stack Overflow discussion:
   https://stackoverflow.com/questions/71194571/word-count-of-markdown-cells-in-jupyter-notebook
   - Used the approach of reading the .ipynb file format and counting words
     specifically from Markdown cells.

2. Datamics GitHub repository:
   https://github.com/datamics/jupyter-word-count
   - Used the idea of scanning notebook cells and calculating word counts
     for different cell types.

Additional modification:
- Added a figure checker to count visual outputs generated in code cells.

Purpose:
This checker was created to help verify Jupyter Notebook submission requirements:
- Maximum of 5,000 words across all Markdown cells
- Maximum of 100 words per Markdown cell explaining code blocks
- Maximum of 15 figures

The script was adapted and updated for modern Jupyter Notebook formats
using nbformat.
"""

import nbformat
import re
import os


# Settings
notebook_path = "MCO2.ipynb"
MAX_MARKDOWN_WORDS = 5000
MAX_WORDS_PER_CELL = 100
MAX_FIGURES = 15

# Functions
def clean_markdown(text):
    """
    Remove Markdown formatting before counting words.
    """
    # Remove code formatting
    text = re.sub(r"`.*?`", "", text)

    # Remove hyperlinks but keep visible text
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

    # Remove Markdown symbols
    text = re.sub(r"[#>*_~\-]", "", text)

    return text

def count_words(text):
    """
    Count words accurately.
    """
    return len(text.split())

# Read Notebook
with open(notebook_path, "r", encoding="utf-8") as f:
    notebook = nbformat.read(f, as_version=4)

total_markdown_words = 0
markdown_cell_counts = []

figure_count = 0

# Check Cells
for index, cell in enumerate(notebook.cells, start=1):
    # Markdown cells
    if cell.cell_type == "markdown":

        cleaned_text = clean_markdown(cell.source)

        words = count_words(cleaned_text)

        total_markdown_words += words

        markdown_cell_counts.append(
            {
                "cell": index,
                "words": words,
                "preview": cell.source[:80].replace("\n", " ")
            }
        )

    # Code outputs / figures
    elif cell.cell_type == "code":

        for output in cell.get("outputs", []):

            data = output.get("data", {})

            if (
                "image/png" in data
                or "image/jpeg" in data
                or "image/svg+xml" in data
            ):
                figure_count += 1

# Generate Report
print("=" * 40)
print("JUPYTER NOTEBOOK QUALITY REPORT")
print("=" * 40)

# Markdown total
print("\nMarkdown word count:")
print(f"{total_markdown_words} / {MAX_MARKDOWN_WORDS}")

if total_markdown_words <= MAX_MARKDOWN_WORDS:
    print("✅ PASS")
else:
    print("❌ FAIL")


# Markdown cell limits
print("\nMarkdown cells above 100 words:")

too_long_cells = [
    c for c in markdown_cell_counts
    if c["words"] > MAX_WORDS_PER_CELL
]


if len(too_long_cells) == 0:
    print("✅ No cells exceed 100 words")

else:
    print("❌ These cells need shortening:")

    for cell in too_long_cells:
        print(
            f"Cell {cell['cell']}: {cell['words']} words"
        )
        print(
            f"  Preview: {cell['preview']}..."
        )


# Figures
print("\nFigures detected:")
print(f"{figure_count} / {MAX_FIGURES}")

if figure_count <= MAX_FIGURES:
    print("✅ PASS")
else:
    print("❌ FAIL")


print("\nFinished.")