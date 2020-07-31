#!/usr/bin/env python3

import bioc
from .datatransform import DataTransform
from .document import Document
from .annotators import Annotation
import uuid

class BioC(DataTransform):
    def load_collection(bioc_input,format =0):
        #Generalize load and add as an argument type 0 default is an xml, 1 a json bioc collection
        collection = None
        if format == 0:
            collection = BioC.__load_collection_xml(bioc_input)
        else :
            collection = BioC.__load_collection_json(bioc_input)
        annotations_list=[]
        raw_text = ""
        raw_text_ID=str(uuid.uuid1())
        # document source = collection.source
        for passage in collection.documents[0].passages:
            raw_text = raw_text + passage.text
            passageID= str(uuid.uuid1())
            passageAttribute = {value:passage.infons[value]
                          for value in passage.infons  if value not in ["section_type"] }
            annotations_list.append(
                Annotation(type=passage.infons["section_type"],
                                      value=raw_text,
                                      ngram = passage.text,
                                      source_ID=raw_text_ID,
                                      ID=passageID,
                                      source="BioCPassage",
                                      span=(passage.offset,passage.offset+len(passage.text)))
                )
            if passage.annotations:
                for thisAnnotation in passage.annotations:
                    annotationID= str(uuid.uuid1())
                    identifier =None
                    if "identifier" in thisAnnotation.infons.keys() :
                        identifier=thisAnnotation.infons["identifier"]
                    else:
                        identifier=thisAnnotation.infons["Identifier"]
                    thisAttributes = {value:thisAnnotation.infons[value]
                                      for value in thisAnnotation.infons  if value not in ["type","identifier","Identifier"] }
                    annotations_list.append(
                       Annotation(type=thisAnnotation.infons["type"],
                                              value=identifier,
                                              ngram =thisAnnotation.text,
                                              source_ID=passageID,
                                              ID=annotationID,
                                              source="BioCAnnotation",
                                              span=(thisAnnotation.locations[0].offset,thisAnnotation.locations[0].offset+ thisAnnotation.locations[0].length))
                        )
        thisDocument = Document(raw_text =raw_text,ID =raw_text_ID, source = collection.source, documentDate = collection.date)
        # attributes=collection.key,collection.standalone,
        # collection.encoding,collection.version
        # collection.infons
        thisDocument.annotations.extend(annotations_list)
        return(thisDocument)

    def __load_collection_xml(bioc_xml):
        with open(bioc_xml, 'r') as fp:
            collection = bioc.load(fp)
        return(collection)

     def __load_collection_json(bioc_json):
        with open(bioc_json, 'r') as fp:
            collection = bioc.biocjson.load(fp)
        return(collection)
