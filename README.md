# AlexTools
Subroutines for python that I consider useful

The first 4 routines I wrote (PDFtoJPG, OCRonImage, PDFToText, PDFOCRToText) work together to return extracted text from PDF files.
Calling PDFOCRToText opens a PDF file, checks if text can be extracted and if not performs OCR on it and then returns the text.
It seems fairly complicated but I have not been able to find a simpler solution online and it was good training. It uses tesseract for OCR.
