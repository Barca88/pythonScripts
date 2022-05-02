from PyPDF2 import PdfFileReader
import os




if __name__ == "__main__":
    d = input("A pasta chama-se: ")
    directory = os.listdir(d)
    pages = 0
    for pdf in directory:
        if pdf.endswith('.pdf'):
            print(pdf)
            pages += PdfFileReader(open(d + '/' + pdf, 'rb')).getNumPages()

    print("Directory has the following:")
    for pdf in directory:
        print(pdf)
    print("Total =", pages, "pages")
    print("Total files =", len(directory))
