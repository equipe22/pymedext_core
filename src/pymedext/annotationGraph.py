#!/usr/bin/env python3

# TODO add id to the init function
#
class AnnotationGraph:
    def __init__(self, value, type, span,  attributes,  isEntity,ngram=""):
        self.value = value
        self.ngram = ngram
        self.type = type
        self.span = span
        self.parent = None
        self.children = None
        self.root = None
        self.attributes = attributes
        self.isEntity=isEntity

    def to_dict(self):
        return {'type':self.type,
               'value':self.value,
               'span':self.span,
               'ngram':self.ngram,
               'isEntity': self.isEntity,
               'attributes': self.attributes}
        
    def addProperty(self, neighbor):
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
        if self.parent != None:
            if self.parent.type == fromType :
                return(self.parent)
            else:
                self.parent.getParent(fromType)
        else:
            return(None)

    def setParent(self, parent):
        self.parent = parent

    def setRoot(self, root):
        self.root = root

    def getNgram(self):
        return(self.root.value[self.span[0]:self.span[1]])

    def addChild(self, child):
        child.setParent(self)
        if self.children == None:
            self.children = [child]
        else:
            self.children.append(child)

    def getSpan(self):
        return(self.span)

    def getChildrenSpan(self):
        childrenSpans = []
        if self.children != None:
            for child in self.children:
                childrenSpans.append(child.getSpan())
        return(childrenSpans)

    def getAttributes(self):
        return(self.attributes+self.parents.getAttributes())

    def getEntitiesChildren(self):
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

    def getParentsProperties(self, filterType= ["drwh_sentences", "drwh_syntagms"]):
        properties =[]
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


    def getProperties(self, filterType) :
        properties=[]
        if self.type in filterType:
            properties.append(self.to_dict())
        return(properties)
