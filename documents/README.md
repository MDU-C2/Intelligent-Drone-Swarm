## Use LaTeX locally
1. Go to https://miktex.org/download and download the installer
1. Install MiKTeX
1. Open MiKTeX Console, check for updates and download/install them
1. Go to https://strawberryperl.com/ and download the MSI installer
1. Install Strawberry Perl
1. Open VSCode
1. Get the LaTeX Workshop extension

### Build glossary
1. Open a Terminal and make sure you're in the correct folder (type `cd` followed by the start of the folder's name, then press TAB and then ENTER). Thereafter, run this command:
```bash
pdflatex main.tex
```
1. Then this command
```bash
makeglossaries main
```
1. Then this command
```bash
pdflatex main.tex
```
1. Then this command
```bash
pdflatex main.tex
```

cd .\documents\