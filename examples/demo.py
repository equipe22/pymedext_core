from pymedextcore import pymedext # contains all pymedextcore  objects
import os
import logging
from grepWrapperAnnotator import findMatches # import findMatches Annotator
from grepWrapperAnnotator import regexFast # a wrapper annotator arround the grep cmd regexFast
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

#advance annotator wrapper arround the grep command
getRegex = regexFast(key_input = ['raw_text'],
                     key_output = 'regex_fast',
                     ID = "regex_fast.v1",
                     regexResource=resourcePath+"regexResource.txt ",
                     pathToPivot=resourcePath+"pivotResource.csv"
                     )
# add all your annotators in a list
annotators =[getRegex]
# annotate your document
LetterPyMedExt.annotate(annotators)
LetterPyMedExt.to_dict()
#write your annotation in PymedExt json
LetterPyMedExt.writeJson("outputfile.json")





## Export PyMedExt Document as a Brat file
path="outputfolder"
try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

pymedext.brat.savetobrat(LetterPyMedExt,path)


#this will output three files on the outputfolder:
#- xxx.txt --> the raw Text
#- xxx.ann --> the annotations
#-  annotation.conf
