import logging  # To harvest logs
import pandas as pd  # To create csv file
from xml.etree import ElementTree as ET  # To Parse XML

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


def main():
    logging.basicConfig(format='%(asctime)s::%(name)s::%(levelname)s::%(message)s',
                        filename='log.txt',
                        level=logging.INFO)
    logging.info('Start')
    process_xml_and_print_csv("DLTINS_20210117_01of01/DLTINS_20210117_01of01.xml", "output.csv")
    logging.info("Loading the xml iterator")
    return


if __name__ == '__main__':
    main()
