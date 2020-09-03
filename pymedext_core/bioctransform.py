#!/usr/bin/env python3

import bioc
from bioc import biocjson
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
        documents_collection =[]
        for doc in collection.documents:
            for passage in doc.passages:
                raw_text = raw_text + passage.text
                passageID= str(uuid.uuid1())
                if "section_type" in passage.infons:
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
                else:
                     annotations_list.append(
                        Annotation(type="BioCPassage",
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
                        thisType = str(type(thisAnnotation)).replace(">","").replace("<","").replace("class ","").replace("bioc.bioc.","").replace("'","")
                        annotations_list.append(
                           Annotation(type=thisAnnotation.infons["type"],
                                      value=identifier,
                                      ngram =thisAnnotation.text,
                                      source_ID=passageID,
                                      ID=annotationID,
                                      source=thisType,
                                      span=(thisAnnotation.locations[0].offset,thisAnnotation.locations[0].offset+ thisAnnotation.locations[0].length),
                                      attributes =thisAttributes)
                            )
                if passage.relations:
                    for thisrelation in passage.relations:
                        annotationID= str(uuid.uuid1())
                        identifier =None
                        if "identifier" in thisrelation.infons.keys() :
                            identifier=thisrelation.infons["identifier"]
                        else:
                            identifier=thisrelation.infons["Identifier"]
                        thisAttributes = {value:thisrelation.infons[value]
                                          for value in thisrelation.infons  if value not in ["type","identifier","Identifier"] }
                        thisAttributes["id"]=thisrelation.id
                        thisType = str(type(thisrelation)).replace(">","").replace("<","").replace("class ","").replace("bioc.bioc.","").replace("'","")
                        annotations_list.append(
                           Annotation(type=thisrelation.infons["type"],
                                      value=identifier,
                                      ngram =thisrelation.text,
                                      source_ID=passageID,
                                      ID=annotationID,
                                      source=thisType,
                                      span=(thisrelation.locations[0].offset,thisrelation.locations[0].offset+ thisrelation.locations[0].length),
                                      attributes=thisAttributes)
                            )

            thisDocument = Document(raw_text =raw_text,ID =raw_text_ID, source = collection.source, documentDate = collection.date)
            # attributes=collection.key,collection.standalone,
            # collection.encoding,collection.version
            # collection.infons
            thisDocument.annotations.extend(annotations_list)
            documents_collection.append(thisDocument)
        return(documents_collection)

    def __load_collection_xml(bioc_xml):
        with open(bioc_xml, 'r') as fp:
            collection = bioc.load(fp)
        return(collection)

    def __load_collection_json(bioc_json):
        with open(bioc_json, 'r') as fp:
            collection = biocjson.load(fp)
        return(collection)
