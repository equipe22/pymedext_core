import uuid
import re
import json
import unidecode
from subprocess import Popen, PIPE
from os import path
import logging
logger = logging.getLogger(__name__)




class Annotation:
    """
    TODO: get_first_key_input	return the annotation of Document.annotations[0], should be called getRawText
    TODO: get_all_key_input	return the annotations oF Documents.annotations which have the same type of key_input list (rename as selectall)
    TODO: get_key_input	return the annotations oF Documents.annotations which have the same type of the i th key_input element  (rename as select)
    TODO: annotate_function	each annotator should implement this functionand return a list of annotations object
    """
    
    def __init__(self, type, value, source, source_ID, span = None, attributes = None, isEntity=False, ID = str(uuid.uuid1())):
        self.value = value
        self.type = type
        self.source = source
        self.span = span
        self.source_ID = source_ID
        self.attributes = attributes
        self.ID = ID
        self.isEntity = isEntity

        
    def to_json(self): 
        return json.dump(self.to_dict())
    
    def to_dict(self):
        return {'type':self.type,
               'value':self.value,
               'span':self.span,
               'source':self.source,
               'source_ID': self.source_ID,
               'isEntity': self.isEntity,
               'attributes': self.attributes,
               'id':self.ID}

class Annotator: 
    def __init__(self, key_input, key_output, ID):
        self.key_input = key_input # list
        self.key_output = key_output # str
        self.ID = ID
        
    def get_first_key_input(self,_input): 
        return  self.get_key_input(_input, 0)
    
    def get_all_key_input(self,_input): 
        return [x for x in _input.annotations if x.type in self.key_input]
    
    def get_key_input(self, _input, i):
        return [x for x in _input.annotations if x.type == self.key_input[i]]
    
    
