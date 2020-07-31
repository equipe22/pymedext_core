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
    Based object which contains Annotation
    """
    
    def __init__(self, type, value, source, source_ID, span = None, attributes = None, isEntity=False, ID = None, ngram = None):
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
        """Tranform Annotation  to json

        :returns: json
        :rtype: json

        """
        return json.dump(self.to_dict())
    
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
                'id':self.ID}

    def getAttributes(self):
        """get Attributes from current and parents Node

        :returns: attributes
        :rtype: a dict

        """
        return(self.attributes+self.parents.getAttributes())

    def getNgram(self):
        """get nGram from root

        :returns: raw ngram
        :rtype: string

        """
        return(self.ngram)

     def setNgram(self):
        """get nGram from root

        :returns: raw ngram
        :rtype: string

        """
        self.ngram = self.root.value[self.span[0]:self.span[1]]

    def getSpan(self):
        """return current Annotation span

        :returns: span(start,end)
        :rtype: tuple

        """
        return(self.span)

    def getChildrenSpan(self):
        """from current node  get all children span

        :returns: tuple of span
        :rtype: list of tuple

        """
        childrenSpans = []
        if self.children != None:
            for child in self.children:
                childrenSpans.append(child.getSpan())
        return(childrenSpans)

    def getEntitiesChildren(self):
        """From current Node, return all children which are
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
                    listChildren.extend(child.getEntitiesChildren())
        else:
            if self.isEntity:
                listChildren.append(self)
        return(listChildren)

    def getProperties(self, filterType):
        """return current node Properties if the Annotation is from a given type

        :param filterType: list of Annotations type
        :returns:  properties
        :rtype:list of dictionnary

        """
        properties=[]
        if self.type in filterType:
            properties.append(self.to_dict())
        return(properties)

    def getParentsProperties(self, filterType):
        """ return parent properties of current annotations if
        it's belong to a specific type

        :param filterType: list of Annotations types
        :returns: list  of current and parents Annotation properties
        :rtype: list of dict

        """
        properties = []
        if self.parent != None:
            # print( " go see parents" )
            # print(properties)
            properties.extend(self.parent.getParentsProperties(filterType))
            properties.extend(self.getProperties(filterType))
        else:
            # print(self.type)
            # print(self.attributes)
            # print(self.span)
            # print(properties)
            properties.extend(self.getProperties(filterType))
        return(properties)

    def setParent(self, parent):
        """set Parent to current Annotation

        :param parent: Annotation
        :returns: None
        :rtype: None

        """
        self.parent = parent

    def setRoot(self, root):
        """set Root to current Annotation

        :param root: Annotation
        :returns: None
        :rtype: None

        """
        self.root = root

    def addChild(self, child):
        """Add a child to current Annotation

        :param child: An annotation to set as child of current node
        :returns: None
        :rtype: None

        """
        child.setParent(self)
        if self.children == None:
            self.children = [child]
        else:
            self.children.append(child)


    def addProperty(self, neighbor):
        """add property of a neighbor who need to have the same span to
        the current Annotation

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




    def getParent(self, fromType):
        """return parent of the current Annottion
        of a specific type

        :param fromType: specific type to found
        :returns: Annotation of a specific type
        :rtype: Annotation

        """
        if self.parent != None:
            if self.parent.type == fromType :
                return(self.parent)
            else:
                self.parent.getParent(fromType)
        else:
            return(None)








class Annotator:
    """
    Abstract class of each Annotator. Furthermore each Annotator must returns a list of Annotation
    TODO: get_all_key_input	return the annotations oF Documents.annotations which have the same type of key_input list (rename as selectall)
    TODO: get_key_input	return the annotations oF Documents.annotations which have the same type of the i th key_input element  (rename as select)
    TODO: annotate_function	each annotator should implement this functionand return a list of annotations object
    """
    def __init__(self, key_input, key_output, ID):
        """Initialied an Annotator

        :param key_input: a list of input annotation type (because annotators could use more than one type of annotation)
        :param key_output:  a string which is the type of Annotator
        :param ID: an uuid object, must be generate by the user to be uniq
        :returns: Annotator
        :rtype: Annotator

        """
        self.key_input = key_input # list
        self.key_output = key_output # str
        self.ID = ID
        
    def get_first_key_input(self,_input):
        """get_first_key_input
	    return the annotation type [0],
        :param _input: list of annotations input for the Annotor
        :returns: a list of annotations
        :rtype: a list of annotations

        """
        logger.debug("returns annotation")
        return  self.get_key_input(_input, 0)
    
    def get_all_key_input(self,_input):
        """returns all key input for the Annotors
        TODO: rename selectAll
        :param _input: return all annotations of a specific types from the Documents
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
        each ANnotator must implement this function
        :param _input: a list of Annotation typet
        :returns: a list of annotations. they will be added to Document.annotations
        :rtype:a list of annotations
        """
        pass
