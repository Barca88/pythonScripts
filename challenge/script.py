import logging
import pandas as pd
from bs4 import BeautifulSoup as b

"""
This program will open DLTINS_20210117_01of01/DLTINS_20210117_01of01.xml and processes it. Using BeautifulSoup to 
navigate in the xml he iterates all the FinInstrm and will store the Id, FullNm, ClssfctnTp, CmmdtyDerivInd, NtnlCcy 
and NtnlCcy on list1. With the list1 populated a dataFrame is created and then the output.csv is created.
"""


def main():
    logging.basicConfig(format='%(asctime)s::%(name)s::%(levelname)s::%(message)s',
                        filename='log.txt',
                        level=logging.INFO)
    logging.info('Started')
    with open("DLTINS_20210117_01of01/DLTINS_20210117_01of01.xml", "r", encoding="utf8") as f:  # opening xml file
        content = f.read()
    logging.info('File read finish')
    soup = b(content, features='lxml-xml')  # This is the slowest part I don't know how to improve it

    list1 = []
    i = 0
    logging.info('Going for the loop')
    for values in soup.findAll("FinInstrm"):
        i += 1
        logging.info('Loop iteration %d', i)
        if values.find("Id") is None:
            imId = str(i)
        else:
            imId = values.find("Id").text
        if values.find("FullNm") is None:
            fullName = ""
        else:
            fullName = values.find("FullNm").text.replace(',', '')
        if values.find("ClssfctnTp") is None:
            clssfctnTp = ""
        else:
            clssfctnTp = values.find("ClssfctnTp").text
        if values.find("CmmdtyDerivInd") is None:
            cmmdtyDerivInd = ""
        else:
            cmmdtyDerivInd = values.find("CmmdtyDerivInd").text
        if values.find("NtnlCcy") is None:
            ntnlCcy = ""
        else:
            ntnlCcy = values.find("NtnlCcy").text
        if values.find("Issr") is None:
            issr = ""
        else:
            issr = values.find("Issr").text
        list1.append([imId, fullName, clssfctnTp, cmmdtyDerivInd, ntnlCcy, issr])

    logging.info('Out of the loop and size of list1 = %d', len(list1))
    df = pd.DataFrame(list1, columns=['Id', 'FullNm', 'ClssfctnTp', 'CmmdtyDerivInd', 'NtnlCcy', 'Issr'])
    logging.info('DataFrame ready')
    df.to_csv("output.csv", index=False)
    logging.info('Finished\nFinInstrm parsed = %d', i)


if __name__ == '__main__':
    main()
