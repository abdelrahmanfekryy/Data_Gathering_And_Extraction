import pandas as pd 
import xml.etree.ElementTree as ET
import os


def S_tag(src_dir,dest_dir,save=True):
    # creating destination directory if not exist 
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # creating a list of all the files that only ends with .xml in the source directory
    XMLs = [file for file in os.listdir(src_dir) if file.endswith(".xml")]

    # iterate over XMLs file names
    for file in XMLs:
        # getting tree and root of the parsed XML file
        tree = ET.parse(f'{src_dir}/{file}')
        root = tree.getroot()
        # search and itrate over all <p> and <td> elements in the tree
        for element in root.findall('.//p') + root.findall('.//td'):
            # copying all <p> or <td> elements contents (text and sub-elements) to a new created element <s>
            # then clearing the originals, Note: no modifications were implemented on the attributes, tail or tag
            S = ET.Element('s')
            S.text = element.text
            element.text = None
            for subelement in element.findall('./'):
                S.append(subelement)
                element.remove(subelement)
            # append the new element <s> to the empty <p> or <td> element
            element.append(S)
        # saving the edited tree with same file name to destination directory
        if save:
            tree.write(f'{dest_dir}/{file}')


if '__main__' == __name__:
    src_dir = f'{os.path.dirname(os.path.realpath(__file__))}/Explainers'
    dest_dir = f'{os.path.dirname(os.path.realpath(__file__))}/Updated'
    S_tag(src_dir,dest_dir,save=True)