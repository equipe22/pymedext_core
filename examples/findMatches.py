
from pymedextcore import annotators
import re 
import uuid
import os 
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class findMatches(annotators.Annotator):
    """
    Annotator based on linux grep to search regext from a source file
    """
    def __init__(self, key_input, key_output, ID, findValues ):
        """FIXME! initialize the annotator

        :param key_input: input ['raw_text']
        :param key_output: Annotation type here "Liposarcom.V0"
        :param ID: regex_fast.version
        :param findValues: "list of value to identify in the text"
        :returns:
        :rtype:

        """
        super().__init__(key_input, key_output, ID)
        self.findValues=findValues
        
    def annotate_function(self, _input):
        """ main annotation function
        :param _input: in this case raw_text
        :returns: a list of annotations
        :rtype:
        """
        logger.debug(_input)
        inp = self.get_key_input(_input,0)[0]
        annotationsList=[]
        for thisValue in self.findValues:
            #result = [i.start() for i in re.finditer(thisValue, inp.value.lower())] 
            for i in re.finditer(thisValue, inp.value.lower()):				
                matchPos=i.start()
                if matchPos is not []:
                    logger.debug("ok go in loop")
                    logger.debug(matchPos)
                    ID = str(uuid.uuid1())
                    annotationsList.append(annotators.Annotation(type= self.key_output,
                					                          value=thisValue, #thisMatch,
                					                          span=(int(matchPos), int(matchPos)+len(thisValue)),
                					                          source=self.ID,
                					                          isEntity=True,
                					                          ID=ID,
                					                          source_ID = inp.ID))
                logger.debug(annotationsList)                					                          
        return(annotationsList)
