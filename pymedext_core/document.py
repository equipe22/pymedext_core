import uuid
import json
from .annotators import Annotator, Annotation
        
class Document:
    """
    Document is the main class of pymedext. It is use to load file and annotate them with annotators
    """
    def __init__(self, raw_text, ID, source=None, pathToconfig=None, documentDate = None):
        """create a Document object

        :param raw_text: raw_text of the doc. if raw_text = load
        will load a json PyMedExt and transform it back to a Document object
        :param ID: The document name
        :param source: not use yet but could be the source name I2B2, OMOP HEGP...
        :param pathToconfig: in case of (raw_text = load), it is a list which contains path to each PyMedExt file
        (could be use directly to filter)
        :returns: Document
        :rtype: Document

        """
        self.source_ID = ID
        self.documentDate = documentDate
        if raw_text != "load":
            self.annotations = [Annotation(type="raw_text",
                                           value=raw_text,
                                           source_ID=ID,
                                           source=source,
                                           span=(0, len(raw_text)))]
            self.ID = str(uuid.uuid1())

        else:
            self.ID= None
            self.annotations=[]
            for thisPath in pathToconfig:
                self.loadFromData(thisPath)

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
                                                        isEntity=annot["isEntity"]))



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
        return json.dump(self.to_dict())
    
    def to_dict(self):
        """transform Document to dict PyMedExt
        TODO: Need to add the Document Date if available,
        the processing date, the annotators used

        :returns: json PyMedExt
        :rtype: dict

        """
        return {'annotations' : [x.to_dict() for x in self.annotations],
                'ID':self.ID,
                'source_ID': self.source_ID 
               }

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
        :param _type:
        :param source_id:
        :param target_id:
        :param attributes:
        :param value:
        :param span:
        :return:
        """

        res = []
        for anno in self.annotations:
            if source_id is not None:
                if anno.source_ID != source_id:
                    continue
            if target_id is not None:
                if anno.ID != target_id:
                    continue
            if attributes is not None:
                if anno.attributes != attributes:
                    continue
            if value is not None:
                if anno.value != value:
                    continue
            if span is not None:
                if anno.span != span:
                    continue
            if anno.type == _type:
                res.append(anno)

        return res
    
    def raw_text(self):
        """return the Document raw_text

        :returns: raw_text
        :rtype: string

        """
        annot = self.get_annotations('raw_text')[0]
        return annot.value
