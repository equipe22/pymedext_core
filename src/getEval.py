from document import Document

from doccanodocument import DoccanoDocument

from doccanotransform import Doccano
from doccanoannotator import *
from doccanosource import *

import os, sys, csv
import argparse
import time
import random

"""

"""


def list_files(directory, extension):
    list_files=[]
    for f in os.listdir(directory):
        if f.endswith(extension) :
            list_files.append(f)
    return (list_files)

parser = argparse.ArgumentParser()
parser.add_argument("--inputFolder",required=True, help="Name of the annotation pymendext results folder ")
parser.add_argument("--typeEval", required=True, help=" 'N or classes")
parser.add_argument("--annotation", required=True, help=" 'neg' for negation, 'fam' for family, 'hyp' for hypothesis, 'ima' for scanner ")
parser.add_argument("--numbEval", required=True, help="Get desired number of evaluations")
parser.add_argument("--regexp", help="a regexp expression with its type separeted by a comma ( ex : ISCOVID,motif ) OR a csv file with list of regexp. If it's a file, 1st column for regexp, 2nd column for pymendext type")
parser.add_argument("--projectName", help="the name of the current project. ex : COVID")
parser.add_argument("--rappel",help="rappel", action='store_true') # where action='store_true' implies default=False


args = parser.parse_args()

if parser.parse_known_args()[0].annotation.lower().startswith('ima'):
    # print("la")
    # ima_parser = argparse.ArgumentParser()
    # ima_parser.add_argument("--regexp", required=True, help="a regexp expression with its type separeted by a comma ( ex : ISCOVID,motif ) OR a csv file with list of regexp. If it's a file, 1st column for regexp, 2nd column for pymendext type")
    # ima_parser.parse_known_args()
    # ima_args = ima_parser.parse_args()
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

if args.annotation == "neg":
    listAnnotedDoc = list_files(args.inputFolder, "negation.json")
    random.shuffle(listAnnotedDoc)
    doccano_file_name = "neg.jsonl"
    annotation = "neg"
elif args.annotation == "fam":
    listAnnotedDoc =  list_files(args.inputFolder, "family.json")
    random.shuffle(listAnnotedDoc)
    doccano_file_name = "fam.jsonl"
    annotation = "fam"
elif args.annotation == "hyp":
    listAnnotedDoc = list_files(args.inputFolder, "hypo.json")
    random.shuffle(listAnnotedDoc)
    doccano_file_name = "hyp.jsonl"
    annotation = "hyp"
elif args.annotation == "ima":
    listAnnotedDoc = os.listdir(args.inputFolder)
    random.shuffle(listAnnotedDoc)
    doccano_file_name ="ima"
    annotation = "ima"
    if args.rappel :
        rappel = True
        doccano_rappel_file_name = "rappel"
    else :
        rappel = False
else :
    print("You must choose an annotation to be evaluated between fam (family), neg (negation), hyp (hypothesis) or ima (regexp)")
    sys.exit()


if args.typeEval == "classes" :
    typeEval = args.typeEval
    doccano_file_name = "classes_" + doccano_file_name
elif args.typeEval == "N" :
    typeEval = args.typeEval
    doccano_file_name = "N_" + doccano_file_name
else :
    print("You must choose a type of evaluation between 'N' or 'classes'")
    sys.exit()




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

thisDoccanoDoc = DoccanoDocument()


#### Tirage aléatoire de N documents dans chaque classe

if typeEval == "classes" :

    if annotation == "neg" :
        while count_Neg < numbEval or count_No_Neg < numbEval :

            docFromJson = Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            dictToDoccano = Doccano.toDoccanoDrWH(docFromJson,type="drwh_negation", segment="drwh_syntagms")
            listDoccanoEval = Doccano.DoccanoEvalClass(thisDoccanoDoc, dict_doccano=dictToDoccano, dictClasses=dictClasses,
                                                   number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
            dictClasses = listDoccanoEval[1]

            if "non negatif" in dictClasses :
                count_No_Neg = dictClasses["non negatif"] # = nombre de non négatifs trouvés jusqu'à présent
            if "negatif" in dictClasses :
                count_Neg = dictClasses["negatif"]

            thisDoccanoDoc = listDoccanoEval[0]
            counter_doc += 1


    if annotation == "fam":
        while count_Neg < numbEval or count_No_Neg < numbEval:
            docFromJson = Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            dictToDoccano = Doccano.toDoccanoDrWH(docFromJson, type="drwh_family", segment="drwh_sentences")
            listDoccanoEval = Doccano.DoccanoEvalClass(thisDoccanoDoc, dict_doccano=dictToDoccano, dictClasses=dictClasses,
                                                   number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
            dictClasses = listDoccanoEval[1]

            if "patient" in dictClasses :
                count_No_Neg = dictClasses["patient"] # = nombre de non négatifs trouvés jusqu'à présent
            if "famille" in dictClasses :
                count_Neg = dictClasses["famille"]

            thisDoccanoDoc = listDoccanoEval[0]
            counter_doc += 1

    if annotation == "hyp":
        while count_Neg < numbEval or count_No_Neg < numbEval:
            docFromJson = Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            dictToDoccano = Doccano.toDoccanoDrWH(docFromJson, type="hypothesis", segment="drwh_sentences")
            listDoccanoEval = Doccano.DoccanoEvalClass(thisDoccanoDoc, dict_doccano=dictToDoccano, dictClasses=dictClasses,
                                                   number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
            dictClasses = listDoccanoEval[1]

            if "realise" in dictClasses :
                count_No_Neg = dictClasses["realise"] # = nombre de non négatifs trouvés jusqu'à présent
            if "non realise" in dictClasses :
                count_Neg = dictClasses["non realise"]


            thisDoccanoDoc = listDoccanoEval[0]
            counter_doc += 1

    thisDoccanoDoc.writeJsonDoccano(doccano_file_name)

    if annotation == "ima":

        print("Class eval type doesn't exist for ima. Please enter 'N' to typeEval option.")


#### Tirage aléatoire de N documents, pas de classe

if typeEval == "N":

    # Pour précision et rappel des regex :

    if annotation == "ima":

        if REGEXP_FILE :

            ### Precision pour un set d'item, rappel si rappel a été mis en option

            print("IF REGEXP_FILE")

            for regexp in dict_regexp :

                #print("regexp",regexp)

                count_already_annoted = 0
                counter_doc = 0


                thisDoccanoDocRappel = DoccanoDocument()


                while count_already_annoted  < numbEval :

                    if counter_doc > len(listAnnotedDoc) -1 :
                        print("There are not enough files with " + regexp + " item.\nYou ask for " + str(numbEval) + " evaluations but there are only " + str(count_already_annoted) + " pymedext results with it.")
                        if count_already_annoted == 0 :
                            print("0 file found with " + regexp + " .")
                        break

                    docFromJson = Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
                    #print("file", folderName + listAnnotedDoc[counter_doc])
                    dictToDoccano = Doccano.toDoccanoImaPrecision(docFromJson, type=dict_regexp[regexp], attribute = regexp)
                    listDoccanoEval = Doccano.DoccanoEvalN(thisDoccanoDocRappel,dict_doccano=dictToDoccano, number_annoted=count_already_annoted, number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
                    count_already_annoted = listDoccanoEval[1]
                    thisDoccanoDocRappel = listDoccanoEval[0]
                    counter_doc += 1

                thisDoccanoDocRappel.writeJsonDoccano(doccano_file_name + "_" + regexp +".jsonl")
                #thisDoccanoDoc.writePlainTextDoccano(pathToOutput=doccano_file_name + "_" + regexp + ".txt",regexp=regexp)

            if rappel:

                ### Rappel pour un set d'items

                thisDoccanoDocRappel = DoccanoDocument()

                for doc in listAnnotedDoc :

                    docFromJsonRappel = Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + doc])
                    dictToDoccanoRappel = Doccano.toDoccanoImaRappel(docFromJsonRappel, dict_regexp_type=dict_regexp, value="NULL", span=[0,0])
                    thisDoccanoRappel=Doccano.DoccanoEvalRappel(thisDoccanoDocRappel, dict_doccano=dictToDoccanoRappel, path_to_doc=folderName + doc)

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


                docFromJson = Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
                dictToDoccano = Doccano.toDoccanoImaPrecision(docFromJson, type=regexp_type,
                                                    attribute=regexp)
                listDoccanoEval = Doccano.DoccanoEvalN(thisDoccanoDoc, dict_doccano=dictToDoccano,
                                                        number_annoted=count_already_annoted, number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
                count_already_annoted = listDoccanoEval[1]
                thisDoccanoDoc = listDoccanoEval[0]
                counter_doc += 1

            #thisDoccanoDoc.writePlainTextDoccano(pathToOutput=doccano_file_name + "_" + regexp + ".txt", regexp=regexp)
            thisDoccanoDoc.writeJsonDoccano(doccano_file_name + "_" + regexp + ".jsonl")

    # Pour neg, fam et hyp :

    if annotation == "neg":
        while count_Neg < numbEval :

            docFromJson = Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            dictToDoccano = Doccano.toDoccanoDrWH(docFromJson, type="drwh_negation",
                                                segment="drwh_syntagms")

            listDoccanoEval = Doccano.DoccanoEvalN(thisDoccanoDoc, dict_doccano=dictToDoccano,
                                                    number_annoted=count_Neg, number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
            count_Neg = listDoccanoEval[1]
            thisDoccanoDoc = listDoccanoEval[0]
            counter_doc += 1

        thisDoccanoDoc.writeJsonDoccano(doccano_file_name)

    if annotation == "fam":
        while count_Neg < numbEval :
            docFromJson = Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            dictToDoccano = Doccano.toDoccanoDrWH(docFromJson, type="drwh_family",
                                                segment="drwh_sentences")
            listDoccanoEval = Doccano.DoccanoEvalN(thisDoccanoDoc, dict_doccano=dictToDoccano,
                                                    number_annoted=count_Neg, number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
            count_Neg = listDoccanoEval[1]
            thisDoccanoDoc = listDoccanoEval[0]
            counter_doc += 1

        thisDoccanoDoc.writeJsonDoccano(doccano_file_name)

    if annotation == "hyp":
        while count_Neg < numbEval:
            docFromJson = Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            dictToDoccano = Doccano.toDoccanoDrWH(docFromJson, type="hypothesis",
                                                segment="drwh_sentences")
            listDoccanoEval = Doccano.DoccanoEvalN(thisDoccanoDoc, dict_doccano=dictToDoccano,
                                                    number_annoted=count_Neg, number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
            count_Neg = listDoccanoEval[1]
            thisDoccanoDoc = listDoccanoEval[0]
            counter_doc += 1

        thisDoccanoDoc.writeJsonDoccano(doccano_file_name)
