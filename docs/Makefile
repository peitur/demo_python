
all : main


python: clean
	latex doc.tex
	pdflatex -halt-on-error doc.tex


clean:
	rm -f *.aux *.dvi *.log *.toc

clear: clean
	rm -f *.pdf

