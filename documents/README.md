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