import uuid
import re
from subprocess import Popen, PIPE
from os import path
import os
from pymedextcore import annotators

import logging
logger = logging.getLogger(__name__)


class regexFast(annotators.Annotator):
    """
    Annotator based on linux grep to search regext from a source file
    """
    def __init__(self, key_input, key_output, ID, regexResource, pathToPivot, ignore_syntax=False):
        """FIXME! initialize the annotator

        :param key_input: input [raw_text']
        :param key_output: either regex_fast or the normalized regex value need to discuss
        :param ID: regex_fast.version
        :param regexResource: path to regex value file
        :param pathToPivot: pivot table between regex and the normalized value
        :param ignore_syntax: not used yet
        :returns:
        :rtype:

        """
        super().__init__(key_input, key_output, ID)
        self.ignore_syntax=ignore_syntax
        self.fileAnnotation=None
        self.countValue=None
        self.pathToPivot=pathToPivot
        self.pivot=dict()
        self.cmds=["fgrep -iow -n -b -F -f "+regexResource]
        self.loadPivot()

    def annotate_function(self, _input):
        """ main annotation function
        :param _input: in this case raw_text
        :returns: a list of annotations
        :rtype:
        """
        logger.debug(_input)
        inp = self.get_key_input(_input,0)[0]
        fileAnnotation,countValue=self.makeMatch(inp)
        countValue=self.setPivot(countValue)
        logger.debug(countValue)
        annotations=[]
        for matchPos in list(fileAnnotation.keys()):
            for drug in fileAnnotation[matchPos]:
                ID = str(uuid.uuid1())
                attributes={"ngram":drug}
                annotations.append(annotators.Annotation(type= self.key_output,
                                              value=countValue[drug]["normalized"], #drug,
                                              span=(int(matchPos), int(matchPos)+len(drug)),
                                              source=self.ID,
                                              isEntity=True,
                                              ID=ID,
                                              attributes=attributes,
                                              source_ID = inp.ID))
        return(annotations)


    def loadPivot(self):
        """This function load the pivot table to normalized the value

        :returns:  pivot table
        :rtype:  dictonnary

        """
        with open(self.pathToPivot,'r') as f:
            for line in f:
                record=line.rstrip().split(",")
                if record[0] not in self.pivot.keys():
                    self.pivot[record[0]] = record[-1]


    def makeMatch(self, inputFileName):
        """ wrapper aroung grep to search words match
        :param inputFileName: file name
        :returns:   matches
        :rtype:  dict

        """
        fileAnnotation = dict()
        countValue = dict()
        logger.debug(inputFileName)
        inputFileName=inp.source_ID+"tmpfile"
        tmpFile=open(inputFileName,"w")
        tmpFile.write(inp.value)
        tmpFile.close()
        for cmd in self.cmds:
            p = Popen((cmd+" "+inputFileName).split() ,stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            logger.debug(out)
            logger.debug(err)
            for line in out.decode("utf-8").split("\n"):
                thisRecord = line.split(":")
                if len(thisRecord) ==3:
                    logger.debug(thisRecord)
                    if thisRecord[1] not in fileAnnotation.keys():
                        fileAnnotation[thisRecord[1]] = dict()
                        fileAnnotation[thisRecord[1]]= [thisRecord[2]]
                    else:
                        fileAnnotation[thisRecord[1]].append(thisRecord[2])
                    if thisRecord[2] not in countValue.keys():
                        countValue[thisRecord[2]] = {"count":1 ,"normalized":"" }
                    else:
                        countValue[thisRecord[2]]["count"]+=1
        os.remove(inputFileName)                        
        return(fileAnnotation,countValue)

    def setPivot(self, countValue):
        """ associated match to the mnormalized value
        :param countValue: dictonnary of match
        :returns: dictionnary with matches
        :rtype: dict

        """
        thisMatch = list(countValue.keys())
        for acall in thisMatch:
            if acall.lower() in self.pivot.keys():
                countValue[acall]["normalized"]=self.pivot[acall.lower()]
        return(countValue)
