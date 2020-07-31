from pymedext_core import pymedext

import os, sys, csv
import argparse
import time
import random


"""
Wrapper that creats DoccanoDocument files for evaluate DrWH annotations, ready to be sent to Doccano
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
parser.add_argument("--annotation", required=True, help=" 'neg' for negation, 'fam' for family, 'hyp' for hypothesis")
parser.add_argument("--numbEval", required=True, help="Get desired number of evaluations")
parser.add_argument("--projectName", help="the name of the current project. ex : COVID")


args = parser.parse_args()


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
else :
    print("You must choose an annotation to be evaluated between fam (family), neg (negation) or hyp (hypothesis)")
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
else :
    doccano_file_name = str(args.projectName) + "_" + timestr + "_" + str(numbEval) + "_" + doccano_file_name
    if args.rappel :
        doccano_rappel_file_name = str(args.projectName) + "_" + timestr + "_" + doccano_rappel_file_name

thisDoccanoDoc = pymedext.DoccanoDocument()


#### Tirage aléatoire de N documents dans chaque classe

if typeEval == "classes" :

    if annotation == "neg" :
        while count_Neg < numbEval or count_No_Neg < numbEval :

            docFromJson = pymedext.Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            dictToDoccano = pymedext.Doccano.toDoccanoDrWH(docFromJson,type="drwh_negation", segment="drwh_syntagms")
            listDoccanoEval = pymedext.Doccano.DoccanoEvalClass(thisDoccanoDoc, dict_doccano=dictToDoccano, dictClasses=dictClasses,
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
            docFromJson = pymedext.Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            dictToDoccano = pymedext.Doccano.toDoccanoDrWH(docFromJson, type="drwh_family", segment="drwh_sentences")
            listDoccanoEval = pymedext.Doccano.DoccanoEvalClass(thisDoccanoDoc, dict_doccano=dictToDoccano, dictClasses=dictClasses,
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
            docFromJson = pymedext.Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            dictToDoccano = pymedext.Doccano.toDoccanoDrWH(docFromJson, type="hypothesis", segment="drwh_sentences")
            listDoccanoEval = pymedext.Doccano.DoccanoEvalClass(thisDoccanoDoc, dict_doccano=dictToDoccano, dictClasses=dictClasses,
                                                   number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
            dictClasses = listDoccanoEval[1]

            if "realise" in dictClasses :
                count_No_Neg = dictClasses["realise"] # = nombre de non négatifs trouvés jusqu'à présent
            if "non realise" in dictClasses :
                count_Neg = dictClasses["non realise"]


            thisDoccanoDoc = listDoccanoEval[0]
            counter_doc += 1

    thisDoccanoDoc.writeJsonDoccano(doccano_file_name)

#### Tirage aléatoire de N documents, pas de classe

if typeEval == "N":

    if annotation == "neg":
        while count_Neg < numbEval :

            docFromJson = pymedext.Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            dictToDoccano = pymedext.Doccano.toDoccanoDrWH(docFromJson, type="drwh_negation",
                                                segment="drwh_syntagms")

            listDoccanoEval = pymedext.Doccano.DoccanoEvalN(thisDoccanoDoc, dict_doccano=dictToDoccano,
                                                    number_annoted=count_Neg, number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
            count_Neg = listDoccanoEval[1]
            thisDoccanoDoc = listDoccanoEval[0]
            counter_doc += 1

        thisDoccanoDoc.writeJsonDoccano(doccano_file_name)

    if annotation == "fam":
        while count_Neg < numbEval :
            docFromJson = pymedext.Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            dictToDoccano = pymedext.Doccano.toDoccanoDrWH(docFromJson, type="drwh_family",
                                                segment="drwh_sentences")
            listDoccanoEval = pymedext.Doccano.DoccanoEvalN(thisDoccanoDoc, dict_doccano=dictToDoccano,
                                                    number_annoted=count_Neg, number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
            count_Neg = listDoccanoEval[1]
            thisDoccanoDoc = listDoccanoEval[0]
            counter_doc += 1

        thisDoccanoDoc.writeJsonDoccano(doccano_file_name)

    if annotation == "hyp":
        while count_Neg < numbEval:
            docFromJson = pymedext.Document(raw_text="load", ID=None, documentDate = None, pathToconfig=[folderName + listAnnotedDoc[counter_doc]])
            dictToDoccano = pymedext.Doccano.toDoccanoDrWH(docFromJson, type="hypothesis",
                                                segment="drwh_sentences")
            listDoccanoEval = pymedext.Doccano.DoccanoEvalN(thisDoccanoDoc, dict_doccano=dictToDoccano,
                                                    number_annoted=count_Neg, number_eval=numbEval, path_to_doc=folderName + listAnnotedDoc[counter_doc])
            count_Neg = listDoccanoEval[1]
            thisDoccanoDoc = listDoccanoEval[0]
            counter_doc += 1

        thisDoccanoDoc.writeJsonDoccano(doccano_file_name)
