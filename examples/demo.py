from pymedextcore import pymedext # contains all pymedextcore  objects
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

dataPath=os.getcwd().replace("src","data/frenchReport/")
resourcePath=os.getcwd().replace("src","ressources/")
letter=open(dataPath+"letter.txt","r").read()
print(letter)

LetterPyMedExt=pymedext.Document(raw_text= letter, ID="ID_letter01")
LetterPyMedExt.to_dict()

#detect the presence or absence of the liposarcome word in the text and return if present the span of the word.



demoAnnotator = findMatches(key_input = ['raw_text'],
                     key_output = 'Liposarcom.V0',
                     ID = "demoreiter", findValues = ["liposarcome"])
                     
# add all your annotators in a list
annotatorsList =[demoAnnotator]
# annotate your document
LetterPyMedExt.annotate(annotatorsList)








thisDoc=pymedext.Document(raw_text= " a document demo you want to work with and contains evidence of. covid 19, sras, sars ", ID="ID01")


#Load a file from path

LetterPyMedExt=pymedext.Document(raw_text= " a document demo you want to work with and contains evidence of. covid 19, sras, sars ", ID="ID01")


thisDoc=pymedext.Document(raw_text= "load", ID="ID01")





from grepWrapperAnnotator import regexFast # contains your local annotator

getRegex = regexFast(key_input = ['raw_text'],
                     key_output = 'regex_fast',
                     ID = "regex_fast.v1",
                     regexResource=resourcePath+"regexResource.txt ",
                     pathToPivot=resourcePath+"pivotResource.csv"
                     )
# add all your annotators in a list
annotators =[getRegex]
# annotate your document
thisDoc.annotate(annotators)
thisDoc.to_dict()
#write your annotation in PymedExt json
thisDoc.writeJson("outputfile.json")
