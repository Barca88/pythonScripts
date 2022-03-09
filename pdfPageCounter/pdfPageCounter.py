from PyPDF2 import PdfFileReader
import os

if __name__ == "__main__":
    d = "print out"
    directory = os.listdir(d)
    pages = 0
    for pdf in directory:
        if pdf.endswith('.pdf'):
            pages += PdfFileReader(open(d + '/' + pdf, 'rb')).getNumPages()

    for pdf in directory:
        print(pdf)
    print("Total =", pages, "pages")
