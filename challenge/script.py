import logging  # To harvest logs
import pandas as pd  # To create csv file
from xml.etree import ElementTree as ET  # To Parse XML
import requests as reqs  # To get the xml via link
from io import StringIO as ioS  # To create unicode text file
import os  # To create dirs
import zipfile  # For Unzipping file

"""
@author: Marco Gonçalves

This program will open DLTINS_20210117_01of01/DLTINS_20210117_01of01.xml and processes it. Using BeautifulSoup to 
navigate in the xml he iterates all the FinInstrm and will store the Id, FullNm, ClssfctnTp, CmmdtyDerivInd, NtnlCcy 
and NtnlCcy on list1. With the list1 populated a dataFrame is created and then the output.csv is created.
"""


def process_xml_and_print_csv(xml_path, csv_path):
    """
    This function read the xml and process it to generate a csv and write it.
    :param xml_path: Is a path to the xml
    :param csv_path: The path to output csv
    """
    logging.info('Start process the xml')
    try:
        xml_iter = ET.iterparse(xml_path,
                                events=("start",))  # Creating xml file itertor

        extracted_data = []  # List to store the extracted data
        csv_columns = ["Id", "FullNm", "ClssfctnTp", "CmmdtyDerivInd", "NtnlCcy", "Issr"]
        logging.info("Extracting the required data from xml")
        i = 0
        for event, element in xml_iter:
            if event == "start":  # Checking for start of the tags

                if "TermntdRcrd" in element.tag:  # Checking for TermntdRcrd tag in which the required data is
                    i += 1
                    logging.info('Loop TermntdRcrd %d', i)
                    data = {}  # Dictionary to store require data in single element
                    # List of the required tags (FinInstrmGnlAttrbts, Issr)
                    req_elements = [
                        (elem.tag, elem)
                        for elem in element
                        if "FinInstrmGnlAttrbts" in elem.tag or "Issr" in elem.tag
                    ]
                    for tag, elem in req_elements:  # Processing the required elements
                        if "FinInstrmGnlAttrbts" in tag:
                            for attribute in elem:  # Loop the FinInstrmGnlAttrbts to populate data
                                if "Id" in attribute.tag is not None:
                                    data[csv_columns[0]] = attribute.text
                                if "FullNm" in attribute.tag is not None:
                                    data[csv_columns[1]] = attribute.text
                                if "ClssfctnTp" in attribute.tag is not None:
                                    data[csv_columns[2]] = attribute.text
                                if "CmmdtyDerivInd" in attribute.tag is not None:
                                    data[csv_columns[3]] = attribute.text
                                if "NtnlCcy" in attribute.tag is not None:
                                    data[csv_columns[4]] = attribute.text
                        elif "Issr" in tag is not None:  # Extracting Issr Tag value
                            data[csv_columns[5]] = elem.text

                    if data != {}:
                        if data[csv_columns[0]] == "" or data[csv_columns[0]] is None:
                            continue
                        else:
                            extracted_data.append(data)  # Appending a element extracted to the extracted_data if has ID

        logging.info("All the required data extracted from xml file")

        df = pd.DataFrame(extracted_data, columns=csv_columns)  # Create DataFrame

        logging.info('DataFrame ready')
        df.to_csv(csv_path, index=False)  # Write the csv
        logging.info('Finished, TermntdRcrd parsed = %d', i)
        return

    except Exception as e:
        logging.error(f"Error occurred while extracting xml {str(e)}")


def get_download_links(url):
    """
     Get the file names and download links
    :param url: URL that has an xml with docs
    :return: A list of (file_name, download_link)
    """
    response = reqs.get(url)
    logging.info('Get the xml')
    response.raise_for_status()  # Raise errors from the HTTP request.
    xml_iter = ET.iterparse(ioS(response.text), events=("start",))
    r = []
    for event, element in xml_iter:
        if event == "start":
            if "doc" in element.tag:
                file_type = element.find(".//str[@name='file_type']")
                if file_type.text == "DLTINS":
                    logging.info('Found a doc with file_type = DLTINS')
                    file_name = element.find(".//str[@name='file_name']").text
                    download_link = element.find(".//str[@name='download_link']").text
                    r.append((file_name, download_link))
    return r


def download(url, download_path, filename):
    """
    Download file from url
    :param url          : download link of file
    :param download_path: dir path to save the downloaded file
    :param filename     : filename to give after download
    :return             : absolute path to the downloaded file
    """
    file = ""
    logging.info("Downloading the xml file.")

    try:
        response = reqs.get(url)  # Getting the content of the file
        if response.ok:  # Checking if the requests got a correct response
            if not os.path.exists(download_path):  # Creating directories in the given download path if not exists
                os.makedirs(download_path)

            file = os.path.join(download_path, filename)  # Creating the filepath for downloading the file

            with open(file, "wb") as f:  # Creating a file at the path with the given file name
                f.write(response.content)

                logging.info("File downloaded")
        else:
            logging.error("Error while downloading the file")
    except Exception as e:
        logging.error(f"Error occurred - {str(e)}")

    return file


def my_unzip(zipped_file, uncompressed_file_path):
    """
    Function to unzip the file
    :param zipped_file           : Compressed File path
    :param uncompressed_file_path: Dir path to store the uncompressed file
    :return                      : Boolean if worked or not
    """
    try:
        logging.info("Extracting the compressed file")
        with zipfile.ZipFile(zipped_file, "r") as zip_ref:
            zip_ref.extractall(uncompressed_file_path)

        logging.info("Compressed file extracted")

        return True
    except Exception as e:
        logging.error(f"Error occurred while extracting - {str(e)}")
        return False


def main():
    logging.basicConfig(format='%(asctime)s::%(name)s::%(levelname)s::%(message)s',
                        filename='log.txt',
                        level=logging.INFO)
    logging.info('Start')

    #  (file_name, download_link)
    files = get_download_links(
        'https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100')
    pwd = download(files[0][-1], os.getcwd(), files[0][0])

    unzip_xml = pwd.split('.')[0] + '.xml'

    if not my_unzip(pwd, os.getcwd()):
        logging.info('Unzip was not successful')
        return

    output = os.path.join(os.getcwd(), files[0][0].split('.')[0] + '.csv')

    process_xml_and_print_csv(unzip_xml,output)
    logging.info('Finish')
    return


if __name__ == '__main__':
    main()
