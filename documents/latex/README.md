# LaTeX
## Files Used in all Projects
*The following files are used for all LaTeX projects*
- `glossary.tex`
    - Do not change how glossary terms and acronyms are called, as this will create errors for other LaTeX projects.
- `IEEEtran.cls`
- `preamble.tex`
    - Make sure you have the right toc depth (`\setcounter{tocdepth}{2}`), as it might have been changed when others have built their projects.
- `refs.bib`
    - Do not change how references are called, as this will create errors for other LaTeX projects.

## Template Files Used in all Projects
*The following files in `templates` must be copied to and used in all LaTex projects*
- `review-page.tex`
- `title-page.tex`

## How to use LaTeX Locally
1. Go to https://miktex.org/download and download the installer
1. Install MiKTeX
1. Open MiKTeX Console, check for updates and download/install them
1. Go to https://strawberryperl.com/ and download the MSI installer
1. Install Strawberry Perl
1. Open VSCode
1. Get the LaTeX Workshop extension

## How to set up your project
1. Put your main file (e.g., `CE-01_pre-study.tex` *(i.e., the file called `main.tex`on Overleaf)*) directly in the `latex` folder.
1. Copy the code from `template/main-template.tex` to your main file.
1. Put all images in `latex/figures` in a folder specific for your project (e.g., `latex/figures/pre-study`).
1. Put the rest of your files in a folder specific for your project (e.g., `latex/pre-study`).

## Get Glossary & References to Work
1. In VSCode, open a Terminal and run 
```bash
cd documents/latex
```
1. In the same terminal, run 
```bash
pdflatex main.tex
bibtex main
makeglossaries main
pdflatex main.tex
pdflatex main.tex
```
**NOTE**: Switch out `main` with the name of your file, e.g. `CE-01_pre-study.tex`

## Useful Links
- Font sizing: https://www.overleaf.com/learn/latex/Font_sizes%2C_families%2C_and_styles
- Math symbols: https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols