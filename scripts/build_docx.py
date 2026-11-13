"""Build paper/build/manuscript.docx from paper/manuscript.md with pandoc (pip install pypandoc_binary).

Citations are rendered with the Elsevier numeric style (paper/build/elsevier-with-titles.csl, from the
Citation Style Language repository).
"""
import subprocess
from pathlib import Path

import pypandoc

PAPER = Path(__file__).resolve().parents[1] / "paper"
cmd = [pypandoc.get_pandoc_path(), "manuscript.md", "--citeproc", "--bibliography", "references.bib",
       "--csl", "build/elsevier-with-titles.csl", "--resource-path=.", "-o", "build/manuscript.docx"]
subprocess.run(cmd, cwd=PAPER, check=True)
subprocess.run([pypandoc.get_pandoc_path(), "cover_letter.md", "-o", "build/cover_letter.docx"], cwd=PAPER, check=True)
print("wrote", PAPER / "build" / "manuscript.docx")
