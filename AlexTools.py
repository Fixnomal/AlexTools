# To import this toolset copy paste the following (uncommented) 3 lines- path might need to be edited or omitted if in same folder:
# import sys
# sys.path.append(r"C:\Users\Sulley\Dropbox\Macros\Python")
# import AlexTools as ac


def PDFtoJPG(PDFpath, saveAs="[inputfilename].jpg"):
    # Saves a JPG file from a specified PDF. Saves JPG at specified location and returns path of jpg file as String.
    # Multipage PDFs will be split up into multiple JPGs and page number appended in the format "-#" (starting at zero, no leading zeros)
    from wand.image import Image as Img #requires ImageMagik requires ghostscript and paths.Tedious, but best solution found so far.
    
    #convert potential paths into strings
    saveAs = str(saveAs)
    PDFpath = str(PDFpath)
    try:
        with Img(filename = PDFpath, resolution = 300) as pdf:
            pdf.compression_quality = 99
            if saveAs == "[inputfilename].jpg":
                pdf.convert("jpg").save(filename=PDFpath.replace(".pdf", ".jpg"))
                return PDFpath.replace(".pdf", ".jpg")
            if not saveAs.endswith(".jpg"):
                saveAs = saveAs + ".jpg"
            pdf.convert("jpg").save(filename=saveAs)
            return saveAs
    except:
        print("PDF file for jpg conversion not found at specified location:", PDFpath)
        return

def OCRonImage(imagePath, deleteImage = False):
    # Performs optical character rocognition on image and returns contents as string.
    # Image can be deleted after text extraction.
    # Not all image types might be supported, tested on jpgs.

    import pytesseract #requires tesseract installation (see path)
    from PIL import Image #needed to convert image formats not natively supported by something
    import os
    try:
        # If you don't have tesseract executable in your PATH, include the following:
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    except:
        print("Tesseract installation not found. Tesseract must be installed on this computer and the correct path "
              "provided in OCRonJPG routine.")
        return
    try:
        with Image.open(str(imagePath)) as img:
            extractedText = pytesseract.image_to_string(img)
    except:
        print("Image file for OCR not found at specified location:", str(imagePath))
        return

    if deleteImage == True:
        os.remove(imagePath)
    return extractedText

def PDFToText(PDFFilePath):
    # Returns text from PDF as list of strings (1 string per page). Empty list if nothing read.
    # returns none and error message if file not found.
    import PyPDF2
    from pathlib import Path


    if not Path(PDFFilePath).is_file(): # check if file exists
        print("PDF file for text extraction not found at specified location:", str(PDFFilePath))
        return

    extractedText = list()
    try: #This will produce error if PDF file returns no text, likely because OCR has not been performed
        with open(str(PDFFilePath), "rb") as fileHandle:
            PDFhandler = PyPDF2.PdfFileReader(fileHandle)
            numberOfPages = PDFhandler.getNumPages()
            for page in range(numberOfPages):
                PDFpage = PDFhandler.getPage(page)
                pageText = PDFpage.extractText()
                extractedText.append(pageText)
    except: #error, sometimes because no text. Sometimes no text just returns empty strings, don't know why the difference
        pass
    return extractedText

def PDFOCRToText(PDFFilePath):
    # Calls PDFtoText, checks if text returned and if yes returns the text.
    # If no text returned, performs OCR (PDFtoImage and OCRonImage) and calls PDFtoText on the result.
    # If still not text returns none and error message if file not found or list with single entry "No text found in this file"    # if not (and OCR set to true) the by using PDFtoJPG and forwarding output of OCRonImage
    # Every page stored in individual JPG in temporary folder tempFolder. Make sure it exists and is writable.
    # returns none and error message if file not found or list with single entry "No text found in this file".

    from pathlib import Path
    tempFolder = Path.home()/"Downloads"

    extractedText = PDFToText(PDFFilePath)
    #Check whether there's any text content in result or if it's just an empty list
    textContent = False
    for page in extractedText:
        if not page == "":
            textContent = True
            break
    if textContent == True: #Text recognized, no OCR necessary, return result.
        return extractedText
    extractedText.clear()
    PDFtoJPG(PDFFilePath, tempFolder / "OCRtempJPG")
    imageFiles = list()
    for image in Path.glob(tempFolder, "OCRtempJPG*.jpg"):
        imageFiles.append(image)
    if len(imageFiles) == 0:
        print("Can't find image files to OCR. Something went wrong with PDF to JPG conversion and/or saving")
        return
    if len(imageFiles) == 1: #When only one page the imageJPGs are not numbered
        extractedText.append(OCRonImage(tempFolder / "OCRtempJPG.jpg",True))
    if len(imageFiles) > 1:
        for imageFileNumber in range(len(imageFiles)):#append to results list page by page. Each jpg one page
            extractedText.append(OCRonImage(tempFolder / f"OCRtempJPG-{imageFileNumber}.jpg",True))
    for page in extractedText:
        if not page =="":
            textContent = True
            break
    if textContent == False:
        extractedText.append("No text found in this file")
    return extractedText

