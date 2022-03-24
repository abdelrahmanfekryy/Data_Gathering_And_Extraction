import pandas as pd 
import xml.etree.ElementTree as ET
import os

def Explainers_func(src_dir,stacked=True,save=True):
    # creating a list to store the extracted data
    data = []

    # creating a list of all the files that only ends with .xml in the source directory
    XMLs = [file for file in os.listdir(src_dir) if file.endswith(".xml")]

    # iterate over XMLs file names
    for file in XMLs:
        # getting tree and root of the parsed XML file
        tree = ET.parse(f'{src_dir}/{file}')
        root = tree.getroot()
        # storing file_name, explainer_id, seo_meta_description, source_id, developer_name in a 2d list.
        # element.get() returns None if attribute not exist unlike element.attrib[] which returns an Error,
        # same as for root.findtext(path/to/element) and element.text
        data.append([file,root.get('id')] + [root.findtext(tag) for tag in ['seo_meta_description','source_id','developer_name']])

    # converting the 2d list to DataFrame   
    Explainers = pd.DataFrame(data,columns=['file_name','explainer_id','seo_meta_description','source_id','developer_name'])
    # repalcing empty string with None (if attribute = '' or element has no text we get empty string).
    Explainers[Explainers == ''] = None
    # reshaping the DataFram
    if stacked:
        Explainers = Explainers.set_index('file_name').stack(dropna=False)
    # saving the DataFrame with same file name .csv to source directory
    if save:
        Explainers.to_csv(f'{src_dir}/Explainers.csv',header=False)
        
    return Explainers

if '__main__' == __name__:
    src_dir = f'{os.path.dirname(os.path.realpath(__file__))}/Explainers'
    Explainers_func(src_dir,save=True)