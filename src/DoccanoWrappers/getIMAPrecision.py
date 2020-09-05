from pymedextcore import pymedext

import os, sys, csv
import argparse
import time
import random

"""
Wrapper that creats DoccanoDocument files for evaluate scanner-covid item extractor precision, ready to be sent to Doccano
"""


def list_files(directory, extension):
    list_files=[]
    for f in os.listdir(directory):
        if f.endswith(extension) :
            list_files.append(f)
    return (list_files)

parser = argparse.ArgumentParser()
parser.add_argument("--inputFolder",required=True, help="Name of the annotation pymendext results folder ")
parser.add_argument("--numbEval", required=True, help="Get desired number of evaluations")
parser.add_argument("--regexp", help="a regex expression with its type separeted by a comma ( ex : ISCOVID,motif ) OR a csv file with list of regexp. If it's a file, 1st column for regexp, 2nd column for pymendext type")
parser.add_argument("--projectName", help="the name of the current project. ex : COVID")
parser.add_argument("--rappel",help="rappel", action='store_true') # where action='store_true' implies default=False


args = parser.parse_args()


try :
    with open(args.regexp, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        dict_regexp = dict((rows[0], rows[1]) for rows in csvreader)
        REGEXP_FILE = True
        print("You gave a regex file.")

except:

    if "/" in args.regexp :
        print("The regexp file you gave doesn't exist")
        sys.exit()
    else :
        if "," not in args.regexp :
            print("You must put a regex and its type seperated by ',' as ISCOVID,motif")
            sys.exit()
        print("You gave a regex expression,its type. If you meant to give a file, this file doesn't exist.")
        regexp = args.regexp.split(",")[0]
        regexp_type = args.regexp.split(",")[1]
        REGEXP_FILE = False


folderName = args.inputFolder
if folderName[-1] != "/" :
    folderName = folderName + "/"

timestr = time.strftime("%Y%m%d-%H%M%S")


listAnnotedDoc = os.listdir(args.inputFolder)
random.shuffle(listAnnotedDoc)
doccano_file_name ="ima"
annotation = "ima"
if args.rappel :
    rappel = True
    doccano_rappel_file_name = "rappel"
else :
    rappel = False

numbEval = int(args.numbEval)

dictClasses = {}
counter_doc = 0
count_Neg = 0
count_No_Neg = 0

if args.projectName is None :
    doccano_file_name = timestr + "_" + str(numbEval) + "_" + doccano_file_name
    if args.rappel :
        doccano_rappel_file_name = timestr + "_" + doccano_rappel_file_name
else :
    doccano_file_name = str(args.projectName) + "_" + timestr + "_" + str(numbEval) + "_" + doccano_file_name
    if args.rappel :
        doccano_rappel_file_name = str(args.projectName) + "_" + timestr + "_" + doccano_rappel_file_name

thisDoccanoDoc = pymedext.DoccanoDocument()


if REGEXP_FILE :

    ### Precision pour un set d'item, rappel si rappel a été mis en option

    print("IF REGEXP_FILE")

    for regexp in dict_regexp :

        #print("regexp",regexp)

        count_already_annoted = 0
        counter_doc = 0


        thisDoccanoDocRappel = pymedext.DoccanoDocument()


        while count_already_annoted  < numbEval :

            if counter_doc > len(listAnnotedDoc) -1 :
                print("There are not enough files with " + regexp + " item.\nYou ask for " + str(numbEval) + " evaluations but there are only " + str(count_already_annoted) + " pymedext results with it.")
                if count_already_annoted == 0 :
                    print("0 file found with " + regexp + " .")
                break

            docFromJson = pymedext.Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            #print("file", folderName + listAnnotedDoc[counter_doc])
            dictToDoccano = pymedext.Doccano.toDoccanoImaPrecision(docFromJson, type=dict_regexp[regexp], attribute = regexp)
            listDoccanoEval = pymedext.Doccano.DoccanoEvalN(thisDoccanoDocRappel,dict_doccano=dictToDoccano, number_annoted=count_already_annoted, number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
            count_already_annoted = listDoccanoEval[1]
            thisDoccanoDocRappel = listDoccanoEval[0]
            counter_doc += 1

        thisDoccanoDocRappel.writeJsonDoccano(doccano_file_name + "_" + regexp +".jsonl")
        #thisDoccanoDoc.writePlainTextDoccano(pathToOutput=doccano_file_name + "_" + regexp + ".txt",regexp=regexp)

    if rappel:

        ### Rappel pour un set d'items

        thisDoccanoDocRappel = pymedext.DoccanoDocument()

        for doc in listAnnotedDoc :

            docFromJsonRappel = pymedext.Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + doc])
            dictToDoccanoRappel = pymedext.Doccano.toDoccanoImaRappel(docFromJsonRappel, dict_regexp_type=dict_regexp, value="NULL", span=[0,0])
            thisDoccanoRappel = pymedext.Doccano.DoccanoEvalRappel(thisDoccanoDocRappel, dict_doccano=dictToDoccanoRappel, path_to_doc=folderName + doc)

        thisDoccanoDocRappel.writeJsonDoccano(doccano_rappel_file_name + ".jsonl")

else :

    ### Precision pour un seul couple (regex,type) pas de rappel


    count_already_annoted = 0
    counter_doc = 0

    while count_already_annoted < numbEval:

        if counter_doc > len(listAnnotedDoc) - 1:
            print("There are not enough files with " + regexp + " item.\nYou ask for " + str(
                numbEval) + " evaluations but there are only " + str(
                count_already_annoted) + " pymedext results with it.")
            if count_already_annoted == 0:
                print("0 file found with " + regexp + " .")
            break


        docFromJson = pymedext.Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
        dictToDoccano = pymedext.Doccano.toDoccanoImaPrecision(docFromJson, type=regexp_type,
                                            attribute=regexp)
        listDoccanoEval = pymedext.Doccano.DoccanoEvalN(thisDoccanoDoc, dict_doccano=dictToDoccano,
                                                number_annoted=count_already_annoted, number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
        count_already_annoted = listDoccanoEval[1]
        thisDoccanoDoc = listDoccanoEval[0]
        counter_doc += 1

    #thisDoccanoDoc.writePlainTextDoccano(pathToOutput=doccano_file_name + "_" + regexp + ".txt", regexp=regexp)
    thisDoccanoDoc.writeJsonDoccano(doccano_file_name + "_" + regexp + ".jsonl")
