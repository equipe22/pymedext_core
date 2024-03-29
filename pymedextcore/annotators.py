import uuid
import re
import json
import unidecode
from subprocess import Popen, PIPE
from os import path
from typing import List, Optional, Tuple, Dict
from deprecated.sphinx import deprecated
from deprecated.sphinx import versionadded
from deprecated.sphinx import versionchanged
import logging
logger = logging.getLogger(__name__)


class Annotation:
    """
    Based object which contains Annotation. Each Annotator must return a list of Annotations.
    """

    def __init__(self, type:str, value:str, source:str, source_ID:str,
                 span:Optional[Tuple[int,int]] = None, attributes:Optional[Dict] = None,
                 isEntity:bool=False, ID:Optional[str] = None, ngram:Optional[str] = None):
        """Intialize an Annotation object

        :param type: annotation type define by the user (linked to the Annotator)
        :param value: the annotation value, has to be a string
        :param source: the name of the Annotator
        :param source_ID: the Annotator id
        :param span: the (start, end) position of the annotators
        :param attributes: In some cases, the value is not enough so other key elements could be saved as dict in attributes
        :param isEntity: if the Annotation is an entity define as an annotation which can be normalized  (e.g. by a specific uri from an ontology) not the case for segment
        :param ID: Annotation ID of this specific annotation
        :returns: Annotation
        :rtype: Annotation

        """
        self.value = value
        self.type = type
        self.source = source
        self.span = span
        self.source_ID = source_ID
        self.attributes = attributes
        if ID is None:
            self.ID = str(uuid.uuid1())
        else:
            self.ID = ID
        self.isEntity = isEntity
        #add graph properties
        self.ngram = ngram # should be called raw_value?
        self.parent = None
        self.children = None
        self.root = None

    def to_json(self):
        """Tranform Annotation to json

        :returns: json
        :rtype: json

        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """Transform Annotation to a dict object
        :returns: dict
        :rtype: dict

        """
        return {'type':self.type,
                'value':self.value,
                'ngram':self.ngram,
                'span':self.span,
                'source':self.source,
                'source_ID': self.source_ID,
                'isEntity': self.isEntity,
                'attributes': self.attributes,
                'ID':self.ID}

    def get_attributes(self):
        """get Attributes from current and parents Node

        :returns: attributes
        :rtype: a dict

        """
        return(self.attributes+self.parent.get_attributes())

    def get_ngram(self):
        """get nGram of the current Annotation

        :returns: raw ngram
        :rtype: string

        """
        return(self.ngram)

    def set_ngram(self):
        """set nGram of the current Annotation

        :returns: 1
        :rtype: int

        """
        self.ngram = self.root.value[self.span[0]:self.span[1]]
        return(1)

    def get_span(self):
        """return current Annotation span

        :returns: span(start,end)
        :rtype: tuple

        """
        return(self.span)

    def get_children_span(self):
        """from current node, will return all children span

        :returns: tuple of span
        :rtype: list of tuple

        """
        childrenSpans = []
        if self.children != None:
            for child in self.children:
                childrenSpans.append(child.get_span())
        return(childrenSpans)

    def get_entities_children(self):
        """From current Node, return all children which are
        Annotation where isEntity =True
        entities

        :returns: children list
        :rtype: list

        """
        listChildren=[]
        if self.children != None:
            for child in self.children:
                if child.children == None:
                    if child.isEntity:
                        listChildren.append(child)
                else:
                    listChildren.extend(child.get_entities_children())
        else:
            if self.isEntity:
                listChildren.append(self)
        return(listChildren)

    def get_properties(self, filter_type:[str]):
        """return current node Properties if the Annotation is from a specific type

        :param filter_type: list of Annotations type
        :returns:  properties
        :rtype: list of dictionnary

        """
        properties=[]
        if self.type in filter_type:
            properties.append(self.to_dict())
        return(properties)

    def get_parents_properties(self, filter_type:[str]):
        """ return parent properties of current annotations if
        it's belong to a specific type

        :param filter_type: list of Annotations types
        :returns: list  of current and parents Annotation properties
        :rtype: list of dict

        """
        properties = []
        if self.parent != None:
            # print( " go see parents" )
            # print(properties)
            properties.extend(self.parent.get_parents_properties(filter_type))
            properties.extend(self.get_properties(filter_type))
        else:
            # print(self.type)
            # print(self.attributes)
            # print(self.span)
            # print(properties)
            properties.extend(self.get_properties(filter_type))
        return(properties)

    def set_parent(self, parent):
        """set Parent to current Annotation

        :param parent: Annotation
        :returns: 1
        :rtype: int

        """
        self.parent = parent
        return(1)

    def set_root(self, root):
        """set Root to current Annotation

        :param root: Annotation
        :returns: 1
        :rtype: int

        """
        self.root = root
        return(1)


    def add_child(self, child):
        """Add a child to current Annotation

        :param child: An annotation to set as child of current node
        :returns: None
        :rtype: None

        """
        child.set_parent(self)
        if self.children == None:
            self.children = [child]
        else:
            self.children.append(child)


    def add_property(self, neighbor):
        """add property of a neighbor to current annnotation, if both have the
        same span

        :param neighbor: the Annotation neighbor to add the same property
        :returns: None
        :rtype: None

        """
        if self.attributes is not None:
            if "properties" not in self.attributes.keys():
                # thisProperty = {"type" : neighbor.type, "value":neighbor.value }
                thisProperty = neighbor.to_dict()
                self.attributes["properties"] = [thisProperty]
            else:
                # thisProperty = {"type" : neighbor.type, "value":neighbor.value }
                thisProperty = neighbor.to_dict()
                self.attributes["properties"].append(thisProperty)
        else:
            # thisProperty = {"type" : neighbor.type, "value":neighbor.value }
            thisProperty = neighbor.to_dict()
            self.attributes = dict()
            self.attributes["properties"] = [thisProperty]




    def get_parent(self, from_type):
        """return  closest parent of the current Annotation
        of a specific type

        :param from_type: specific type to found
        :returns: Annotation of a specific type
        :rtype: Annotation

        """
        if self.parent != None:
            if self.parent.type == from_type :
                return(self.parent)
            else:
                self.parent.get_parent(from_type)
        else:
            return(None)








class Annotator:
    """
    Abstract class of each Annotator. For that purpose an Annotator must
    implement the function annotate_function(). This function return
    a list of Annotations object.

    """
    def __init__(self, key_input:[str], key_output:str, ID:str):
        """Initialised an Annotator

        :param key_input: a list of input annotation type (because annotators could use more than one type of annotation)
        :param key_output:  a string which is the type of Annotator
        :param ID: an uuid object, must be generate by the user to be uniq
        :returns: Annotator
        :rtype: Annotator

        """
        self.key_input = key_input # list
        self.key_output = key_output # str
        self.ID = ID

    @deprecated(version='0.3', reason="This function will be removed soon use instead select_first_input")
    def get_first_key_input(self,_input):
        """get_first_key_input, return the annotation type [0].

        :param _input: list of annotations input for the Annotator
        :returns: a list of annotations
        :rtype: a list of annotations

        """
        logger.debug("returns annotation")
        return  self.get_key_input(_input, 0)

    @versionadded(version='0.3', reason="This function will replace get_first_key_input")
    def select_first_input(self,_input):
        """return the first annotation from _input key list,

        :param _input: list of annotations input for the Annotator
        :returns: a list of annotations
        :rtype: a list of annotations

        """
        logger.debug("returns annotation")
        return  self.get_key_input(_input, 0)

    @deprecated(version='0.3', reason="This function will be removed soon use instead select_all_inputs")
    def get_all_key_input(self,_input):
        """returns all key input for the Annotator

        :param _input: return all annotations of a specific types from the Document
        :returns: a list of annotations
        :rtype: a list of annotation

        """
        logger.debug("returns all annotations")
        return [x for x in _input.annotations if x.type in self.key_input]

    @versionadded(version='0.3', reason="This function replaced get_all_key_input")
    def select_all_inputs(self,_input):
        """returns all key input for the Annotator

        :param _input: return all annotations of a specific types from the Document
        :returns: a list of annotations
        :rtype: a list of annotation

        """
        logger.debug("returns all annotations")
        return [x for x in _input.annotations if x.type in self.key_input]

    def get_key_input(self, _input, i):
        """return a specific annotations type from key_input
        :param _input: key_input list
        :param i: the indice of the list to selecy
        :returns:a list of annotations
        :rtype:a list of annotation

        """
        logger.debug("returns specific annotations")
        return [x for x in _input.annotations if x.type == self.key_input[i]]

    def annotate_function(self, _input):
        """ main annotation function
        each Annotator must implement this function

        :param _input: a list of Annotation typet
        :returns: a list of annotations. they will be added to Document.annotations
        :rtype: List[Annotation]
        """
        pass



class Relation:
    """
    Based object which contains Relation
    """

    def __init__(self, type: str, head: str, target:str, source:str,
                 source_ID:str, attributes:Optional[List] = None, ID:Optional[str] = None):
        """Intialize an Annotation object

        :param type: annotation type define by the user (linked to the Annotator)
        :param head: head of the relation, ID of the source entity
        :param target: target of the relation, ID of the target entity
        :param source: the name of the Annotator
        :param source_ID: the Annotator id
        :param attributes: In some cases, the value is not enough so other key elements could be saved as dict in attributes
        :param ID: Annotation ID of this specific annotation
        :returns: Relation
        :rtype: Relation
        """
        self.head = head
        self.target = target
        self.type = type
        self.source = source
        self.source_ID = source_ID
        self.attributes = attributes
        if ID is None:
            self.ID = str(uuid.uuid1())
        else:
            self.ID = ID

#         TODO: add graph properties
#         self.ngram = ngram # should be called raw_value?
#         self.parent = None
#         self.children = None
#         self.root = None

    def to_json(self):
        """Tranform Relation to json

        :returns: json
        :rtype: json
        """
        return json.dump(self.to_dict())

    def to_dict(self):
        """Transform Relation to a dict object

        :returns: dict
        :rtype: dict
        """
        return {'type':self.type,
                'head':self.head,
                'target': self.target,
                'source':self.source,
                'source_ID': self.source_ID,
                'attributes': self.attributes,
                'ID':self.ID}
