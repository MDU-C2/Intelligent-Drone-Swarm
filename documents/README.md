## Use LaTeX locally
1. Go to https://miktex.org/download and download the installer
1. Install MiKTeX
1. Open MiKTeX Console, check for updates and download/install them
1. Go to https://strawberryperl.com/ and download the MSI installer
1. Install Strawberry Perl
1. Open VSCode
1. Get the LaTeX Workshop extension

### Get Glossary & References to Work
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
**NOTE**: Switch out `main` with the name of your file, e.g. `CE-04_system-design-description`

## Command Snippets


```bash
pdflatex CE-04_system-design-description.tex
bibtex CE-04_system-design-description
makeglossaries CE-04_system-design-description
pdflatex CE-04_system-design-description.tex
pdflatex CE-04_system-design-description.tex
```

# About this Folder
- This folder contains **approved** deliverables.
- Deliverables that want reviewing/have not been approved are kept on SharePoint.
- CE & QM are responsible for uploading approved deliverables.

# Plans
- Project Plan
- Configuration Management Plan
- Quality Management Plan
- Requirements Management Plan
- Safety Management Plan
- Verification & Validation Management Plan

### Looking for something else?
- The project's purpose and goals are found in the Project Plan (PDF)
- Pre-Study is found here
- System Description (before applying our solution) is here

<b><ins>NOTE!! PLANS AND REPORTS ARE WRITTEN ON OVERLEAF</ins>, and then uploaded to this folder</b>
- Template etc. for Overleaf found [here](cheat-sheets/latex)
- Don't forget to to check if you have the latest version of:
  - review-page.tex
  - title-page.tex
  - glossary.tex
  - preamble.tex
  - refs.bib
  - You can find those files [here](main/cheat-sheets/latex)
    - The .zip in there might have an older version of the above mentioned files.
- Don't forget to check the [Quality Checklist](main/quality-checklist-report.md)