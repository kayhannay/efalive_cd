#!/bin/bash

DOC_NAME=efaLive_de

mkdir build
pdflatex -output-directory=./build/ $DOC_NAME.tex
bibtex build/$DOC_NAME
pdflatex -output-directory=./build/ $DOC_NAME.tex
pdflatex -output-directory=./build/ $DOC_NAME.tex

