import boto3
import pandas as pd
from bs4 import BeautifulSoup as b
import logging



s3_client = boto3.client('s3')


def main(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    content = s3_client.get_object(Bucket='barca-bucket', Key="DLTINS_20210117_01of01/DLTINS_20210117_01of01.xml")['Body'].read()
    logger.info('I got the xml')
    
    soup = b(content, features='xml')  # This is the slowest part I don't know how to improve it

    list1 = []
    i = 0
    logger.info('Going for the loop')
    for values in soup.findAll("FinInstrm"):
        i += 1
        logger.info('Iteration = %d',i)
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
        break

    df = pd.DataFrame(list1, columns=['Id', 'FullNm', 'ClssfctnTp', 'CmmdtyDerivInd', 'NtnlCcy', 'Issr'])
    logger.info('Works and i=%d',i)
    #df.to_csv("output.csv", index=False) Never reach this part :(
    #s3_client.put_object(Bucket='barca-bucket',Key='teste.txt',Body=content)