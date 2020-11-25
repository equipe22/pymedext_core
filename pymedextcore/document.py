import uuid
import json
from .annotators import Annotator, Annotation

from .utils import generate_id

class Document:
    """
    Document is the main class of pymedext. It is use to load file and annotate them with annotators
    """
    def __init__(self, raw_text, ID=None, attributes=None, source=None, pathToconfig=None, documentDate = None):
        """create a Document object

        :param raw_text: raw_text of the doc. if raw_text = load
        will load a json PyMedExt and transform it back to a Document object
        :param ID: The document name
        :param attributes: Dict of attributes related to the document (e.g., person_id).
        :param source: not use yet but could be the source name I2B2, OMOP HEGP...
        :param pathToconfig: in case of (raw_text = load), it is a list which contains path to each PyMedExt file
        (could be use directly to filter)
        :returns: Document
        :rtype: Document

        """
        self.documentDate = documentDate
        self.attributes = attributes
        self.source = source

        if raw_text != "load":
            self.annotations = [Annotation(type="raw_text",
                                           value=raw_text,
                                           source_ID=ID,
                                           source=source,
                                           span=(0, len(raw_text)))]
            self.ID = generate_id(ID)
            self.source_ID = ID

        else:
            self.ID= None
            self.annotations=[]
            self.source_ID = None
            for thisPath in pathToconfig:
                self.loadFromData(thisPath)

    def __repr__(self):
        return str(self.to_dict())

    def __str__(self):
        if self.annotations is not None:
            anns = f'\n            annotations : {[ x.__str__() for x in self.annotations if x.type !="raw_text"]}'
        return f'Document( ID: {self.ID} \n\
          raw_text: "{self.raw_text}" ) {anns} '

    def loadFromData(self, pathToconfig):
         """Transform json Pymedext to Document

         :param pathToconfig: list of path to json files,
         :returns: add annotations to Document
         :rtype: Document

         """
         with open(pathToconfig) as f:
             mesannotations=json.load(f)
         for annot in mesannotations["annotations"]:
            #print("annot[value]", annot["value"])
            #print("type(annot[value])", type(annot["value"]))
            if "empty" not in annot["value"]:
                #print("empty not in annot[value]")

                if "raw_text" in annot["type"]:
                    if self.ID == None:
                        self.ID=annot["id"]
                    if self.source_ID == None:
                        self.source_ID=annot["source_ID"]
                    if self.source == None:
                        self.source=annot["source"]

                    self.annotations.insert(0,Annotation(type=annot["type"],
                                                         value=annot["value"],
                                                         source_ID=annot["source_ID"],
                                                         ID=annot["id"],
                                                         source=annot["source"],
                                                         span=annot["span"]))
                else:
                     self.annotations.append(Annotation(type=annot["type"],
                                                        value=annot["value"],
                                                        source_ID=annot["source_ID"],
                                                        ID=annot["id"],
                                                        source=annot["source"],
                                                        span=annot["span"],
                                                        attributes=annot["attributes"],
                                                        isEntity=annot["isEntity"],
                                                        ngram=annot["ngram"]))


    def annotate(self, annotator):
        """Main function to annotate Document

        :param annotator: annotators list
        :returns: run _annotate which add annotations to Document
        :rtype: Document

        """
        if type(annotator) == Annotator:
            annotator = [annotator]

        for ann in annotator:
            self._annotate(ann)

    def _annotate(self, annotator):
        """ Hidden function to annotate document
        :param annotator: an annotator
        :returns: add annotations to a document
        :rtype: Document

        """
        new_annotations = annotator.annotate_function(self)
        #print(new_annotations)
        if new_annotations is not None:
            [self.annotations.append(x) for x in new_annotations]
        #setattr(self, annotator.key_output ,annotator.annotate_function(self))

    def to_json(self):
        """ transform annotations to a json

        :returns: transform annotation to json
        :rtype: json

        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """transform Document to dict PyMedExt
        TODO: Need to add the Document Date if available,
        the processing date, the annotators used

        :returns: json PyMedExt
        :rtype: dict

        """
        return {'annotations' : [x.to_dict() for x in self.annotations],
                'ID':self.ID,
                'source_ID': self.source_ID,
                'attributes': self.attributes,
                'documentDate':self.documentDate
               }

    @staticmethod
    def from_dict(d):
        """Create a Document from a dict of document (as created using to_dict)
        :param d: Dict
        :returns: Document
        :rtype: Document
        """
        doc = Document(raw_text='')
        for k,v in d.items():
            if k != 'annotations':
                setattr(doc, k ,v)
            else:
                doc.annotations = []
                for ann in v:
                    doc.annotations.append(Annotation(**ann))
        return doc



    def writeJson(self, pathToOutput):
        """Transform Document to json PyMedExt

        :param pathToOutput: path to result file
        :returns: none
        :rtype: none

        """
        with open(pathToOutput, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    def get_annotations(self, _type, source_id=None, target_id=None, attributes=None, value=None, span=None):
        """
        returns an annotations of a specific type from source. Can  filter from
        type, source_id or target_id, span, source_id, attributes and value.
        :param _type: annotation type
        :param source_id: annotation source id
        :param target_id: annotation target id
        :param attributes:
        :param value:
        :param span:
        :return:
        """

        res = []
        for anno in self.annotations:
            if source_id is not None:
                if anno.source_ID == source_id:
                    res.append(anno)
            if target_id is not None:
                if anno.ID == target_id:
                    res.append(anno)
            if attributes is not None:
                if anno.attributes == attributes:
                    res.append(anno)
            if value is not None:
                if anno.value == value:
                    res.append(anno)
            if span is not None:
                if anno.span == span:
                    res.append(anno)
            if anno.type == _type:
                res.append(anno)
        return res

    @property
    def raw_text(self):
        """return the Document raw_text

        :returns: raw_text
        :rtype: string

        """
        annot = self.get_annotations('raw_text')[0]
        return annot.value

    def getGraph(self):
        """return the graph associated with the raw_text
        :returns:
        :rtype:

        """
        annot = self.get_annotations('raw_text')[0]
        return annot


    def get_annotation_by_id(self, _id):

        res = [x for x in self.annotations if x.ID == _id]
        if res == []:
            return None
        else:
            return res[0]
