"""Build the submission files for Automation in Construction (pip install pypandoc_binary python-docx).

    python scripts/build_docx.py

Writes paper/build/*.docx and assembles paper/submission/:
    manuscript.docx       single column, continuous line numbers (left) from the title page, page numbers,
                          no underlined text, numbered references in order of citation (Elsevier CSL)
    highlights.docx       separate highlights file
    cover_letter.docx
    graphical_abstract.tif / .pdf
    Figure_1..5.pdf / .png  each figure as a separate file, vector PDF and 600-dpi PNG
"""
import shutil
import subprocess
from pathlib import Path

import docx
import pypandoc
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
PAPER, BUILD, SUB = ROOT / "paper", ROOT / "paper" / "build", ROOT / "paper" / "submission"
FIGURES = ["fig_role_by_granularity", "fig_role_by_access", "fig_t2_levels", "fig_t2_coverage",
           "fig_weights_eui_error"]  # order of appearance in the manuscript
PANDOC = pypandoc.get_pandoc_path()


def pandoc(src: str, out: Path, cite: bool = False) -> None:
    cmd = [PANDOC, src, "-o", str(out), "--resource-path=."]
    if cite:
        cmd += ["--citeproc", "--bibliography", "references.bib", "--csl", "build/elsevier-with-titles.csl"]
    subprocess.run(cmd, cwd=PAPER, check=True)


def _page_number_footer(section) -> None:
    p = section.footer.paragraphs[0] if section.footer.paragraphs else section.footer.add_paragraph()
    p.alignment = 1  # center
    run = p.add_run()
    for tag, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)


def finish(path: Path, line_numbers: bool) -> None:
    d = docx.Document(path)
    for st in d.styles:  # no underlined text anywhere (hyperlinks included)
        try:
            if st.font is not None and st.font.underline:
                st.font.underline = False
        except AttributeError:
            pass
    for p in d.paragraphs:
        for r in p.runs:
            if r.font.underline:
                r.font.underline = False
    for section in d.sections:
        if line_numbers:
            ln = OxmlElement("w:lnNumType")
            ln.set(qn("w:countBy"), "1")
            ln.set(qn("w:restart"), "continuous")
            ln.set(qn("w:distance"), "360")
            pg = section._sectPr.find(qn("w:pgSz"))
            pg.addnext(ln) if pg is not None else section._sectPr.append(ln)
        _page_number_footer(section)
    d.save(path)


def main() -> None:
    BUILD.mkdir(exist_ok=True)
    pandoc("manuscript.md", BUILD / "manuscript.docx", cite=True)
    finish(BUILD / "manuscript.docx", line_numbers=True)
    pandoc("highlights.md", BUILD / "highlights.docx")
    pandoc("cover_letter.md", BUILD / "cover_letter.docx")
    for f in ("highlights.docx", "cover_letter.docx"):
        finish(BUILD / f, line_numbers=False)

    SUB.mkdir(exist_ok=True)
    for f in ("manuscript.docx", "highlights.docx", "cover_letter.docx"):
        shutil.copy(BUILD / f, SUB / f)
    for ext in (".tif", ".pdf"):
        shutil.copy(PAPER / "figures" / f"graphical_abstract{ext}", SUB / f"graphical_abstract{ext}")
    for i, name in enumerate(FIGURES, 1):
        for ext in (".pdf", ".png"):
            shutil.copy(PAPER / "figures" / f"{name}{ext}", SUB / f"Figure_{i}{ext}")
    print("wrote", SUB)


if __name__ == "__main__":
    main()
