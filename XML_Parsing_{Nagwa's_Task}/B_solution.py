import pandas as pd 
import xml.etree.ElementTree as ET
import os


def Transcripts_func(src_dir,stacked=True,save=True):
    # creating a list of all the files that only ends with .xml in the source directory
    XMLs = [file for file in os.listdir(src_dir) if file.endswith(".xml")]

    # iterate over XMLs file names
    for file in XMLs:
        # getting tree and root of the parsed XML file
        tree = ET.parse(f'{src_dir}/{file}')
        root = tree.getroot()
        # creating a list to store the extracted data
        data = []
        # find and iterate over all question tag subelements on all levels
        for element in root.findall('.//question'):
            # storing question id, media identifier, question title, start time and end time in the 2d list.
            data.append([element.get('id'),
                        element.get('media_identifier'),
                        element.findtext('question_title'),
                        element.find('p[1]/s[1]').get('start_time'),
                        element.find('p[last()]/s[last()]').get('end_time')])
        # converting the 2d list to DataFrame 
        Transcript = pd.DataFrame(data,columns=['question_id','media_identifier','question_title','start_time','end_time'])
        # repalcing empty string with None (if attribute = '' or element has no text we get empty string).
        Transcript[Transcript == ''] = None
        # reshaping the DataFram
        if stacked:
            Transcript = Transcript.stack(dropna=False)
        # saving the DataFrame with same file name .csv to source directory
        if save:
            Transcript.to_csv(f"{src_dir}/{file.split('.')[0]}.csv",header=False)


if '__main__' == __name__:
    src_dir = f'{os.path.dirname(os.path.realpath(__file__))}/Video Transcripts'
    Transcripts_func(src_dir,save=True)