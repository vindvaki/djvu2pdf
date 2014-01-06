
# WARNING

This is script is very fragile. Don't use it unless you know what it
does!


# About

generates compressed PDF from DjVu and tries to include text layers
from the original DjVu file. I have no idea what happens in case there
is no embedded text.


# (nontrivial) Dependencies

- [`djvused`](http://djvu.sourceforge.net/): To extract metadata like the TOC and the number of pages.
- [`ddjvu`](http://djvu.sourceforge.net/): To split the djvu file into tiff pages.
- [`djvu2hocr`](http://jwilk.net/software/ocrodjvu): To extract the OCR layers for `pdfbeads`.
- [`pdfbeads`](http://rubygems.org/gems/pdfbeads): To combine TIFF images and OCR content into a highly
  compressed pdf file.
- `djvu2pdf_toc_parser.py`: A python script to convert the TOC for `pdfbeads`.

# TODO

## Handle arguments

The basic use case for now is only `djvu2pdf [input] [output]`, but we
should at least make sure that

- exactly two arguments are provided
- `input` exists
- `output` is writable (otherwise we'd lose a lot of precious
  work)
  
Furthermore, it might be nice to have the option to include a
`pdfbeads`-compatible TOC with the input file (the indentation-based
syntax is nice, so one might decide to write a TOC). This feature could 
be introduced through the flag `--toc=[table of contents file]`


## Handle errors along the way

- If `input` is not a djvu file, then we should fail instantly.
- If some dependency isn't installed, we should quit immediately (but
  it is not our job to make sure they are set up correctly if they are
  there).
- If there is no embedded text then we should not output any temporary
  html files along the way.
