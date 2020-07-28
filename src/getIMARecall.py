from document import Document

from doccanodocument import DoccanoDocument

from doccanotransform import Doccano
from doccanoannotator import *
from doccanosource import *


import os, sys, csv
import argparse
import time
import random


def list_files(directory, extension):
    list_files=[]
    for f in os.listdir(directory):
        if f.endswith(extension) :
            list_files.append(f)
    return (list_files)

parser = argparse.ArgumentParser()
parser.add_argument("--inputFolder",required=True, help="Name of the annotation pymendext results folder ")
parser.add_argument("--regexp", help="a csv file with list of regexp. 1st column for regexp, 2nd column for pymendext type")
parser.add_argument("--projectName", help="the name of the current project. ex : COVID")

args = parser.parse_args()

try:
    with open(args.regexp, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        dict_regexp = dict((rows[0], rows[1]) for rows in csvreader)
        print("dict:",dict_regexp)

except ValueError :
    sys.exit()

folderName = args.inputFolder
if folderName[-1] != "/" :
    folderName = folderName + "/"

timestr = time.strftime("%Y%m%d-%H%M%S")
doccano_rappel_file_name = "IMA_recall"


listAnnotedDoc = os.listdir(args.inputFolder)
random.shuffle(listAnnotedDoc)
doccano_file_name ="ima"
annotation = "ima"

if args.projectName is None :
    doccano_rappel_file_name = timestr + "_" + doccano_rappel_file_name
else :
    doccano_rappel_file_name = str(args.projectName) + "_" + timestr + "_" + doccano_rappel_file_name

thisDoccanoDocRappel = DoccanoDocument()

for doc in listAnnotedDoc :

    docFromJsonRappel = Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + doc])
    dictToDoccanoRappel = Doccano.toDoccanoImaRappel(Document=docFromJsonRappel, dict_regexp_type=dict_regexp, value="NULL", span=[0,0])
    thisDoccanoRappel = Doccano.DoccanoEvalRappel(DoccanoDocument=thisDoccanoDocRappel, dict_doccano=dictToDoccanoRappel, path_to_doc=folderName + doc)

thisDoccanoDocRappel.writeJsonDoccano(doccano_rappel_file_name + ".jsonl")
