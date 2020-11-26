#!/usr/bin/env python3

import uuid
import bioc
from bioc import biocjson
from .datatransform import DataTransform
from .document import Document
from .annotators import Annotation

class BioC(DataTransform):
    @staticmethod
    def load_collection(bioc_input,format =0, isFile = True):
        #Generalize load and add as an argument type 0 default is an xml, 1 a json bioc collection
        collection = None
        if format == 0:
            collection = BioC.__load_collection_xml(bioc_input, isFile)
        else :
            collection = BioC.__load_collection_json(bioc_input, isFile)
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
                    #passageAttribute = {value:passage.infons[value]
                    #              for value in passage.infons  if value not in ["section_type"] }
                    annotations_list.append(
                        Annotation(type=passage.infons["section_type"],
                                  value=passage.text,
                                  ngram = passage.text,
                                  source_ID=raw_text_ID,
                                  ID=passageID,
                                  source="BioCPassage",
                                  span=(passage.offset,passage.offset+len(passage.text)))
                        )
                else:
                    annotations_list.append(
                        Annotation(type="BioCPassage",
                                  value=passage.text,
                                  ngram = passage.text,
                                  source_ID=raw_text_ID,
                                  ID=passageID,
                                  source="BioCPassage",
                                  span=(passage.offset,passage.offset+len(passage.text)))
                        )

                relations_annot_dict=dict()
                if passage.annotations:
                    for thisAnnotation in passage.annotations:
                        annotationID= str(uuid.uuid1())
                        identifier =None
                        if "identifier" in thisAnnotation.infons.keys() :
                            identifier=thisAnnotation.infons["identifier"]
                        elif "Identifier" in thisAnnotation.infons.keys() :
                            identifier=thisAnnotation.infons["Identifier"]
                        thisAttributes = {value:thisAnnotation.infons[value]
                                          for value in thisAnnotation.infons  \
                                          if value not in ["type","identifier","Identifier"] }
                        thisAttributes["id"]=thisAnnotation.id
                        relations_annot_dict[thisAnnotation.id]= \
                                (thisAnnotation.locations[0].offset,
                                 thisAnnotation.locations[0].offset + thisAnnotation.locations[0].length)
                        thisType = str(type(thisAnnotation)).replace(">","") \
                                                            .replace("<","") \
                                                            .replace("class ","") \
                                                            .replace("bioc.bioc.","") \
                                                            .replace("'","")
                        annotations_list.append(
                           Annotation(type=thisAnnotation.infons["type"],
                                      value=identifier,
                                      ngram =thisAnnotation.text,
                                      source_ID=passageID,
                                      ID=annotationID,
                                      source=thisType,
                                      span=(thisAnnotation.locations[0].offset,
                                            thisAnnotation.locations[0].offset+ thisAnnotation.locations[0].length),
                                      attributes =thisAttributes, isEntity=True)
                            )
                if passage.relations:
                    for thisrelation in passage.relations:
                        annotationID= str(uuid.uuid1())
                        identifier =None
                        if "identifier" in thisrelation.infons.keys() :
                            identifier=thisrelation.infons["identifier"]
                        elif "Identifier" in thisrelation.infons.keys():
                            identifier=thisrelation.infons["Identifier"]
                        thisAttributes = {value:thisrelation.infons[value]
                                          for value in thisrelation.infons
                                          if value not in ["type","identifier","Identifier"] }
                        thisAttributes["id"]=thisrelation.id
                        thisType = str(type(thisrelation)).replace(">","") \
                                                          .replace("<","") \
                                                          .replace("class ","") \
                                                          .replace("bioc.bioc.","") \
                                                          .replace("'","")
                        for refNode in thisrelation.nodes:
                            annotations_list.append(
                               Annotation(type=thisrelation.infons["type"],
                                          value=identifier,
                                          ngram ="Null",
                                          source_ID=passageID,
                                          ID=annotationID,
                                          source=thisType,
                                          span= relations_annot_dict[refNode.refid],
                                          attributes=thisAttributes)
                                )

            thisDocument = Document(raw_text =raw_text,
                                    ID =raw_text_ID,
                                    source = collection.source,
                                    documentDate = collection.date)
            # attributes=collection.key,collection.standalone,
            # collection.encoding,collection.version
            # collection.infons
            thisDocument.annotations.extend(annotations_list)
            documents_collection.append(thisDocument)
        return documents_collection

    @staticmethod
    def __load_collection_xml(bioc_xml, isFile=True):
        if isFile :
            with open(bioc_xml, 'r') as fp:
                collection = bioc.load(fp)
            return collection
        else:
            collection = bioc.loads(bioc_xml)
            return collection

    @staticmethod
    def __load_collection_json(bioc_json, isFile=True):
        if isFile:
            with open(bioc_json, 'r') as fp:
                collection = biocjson.load(fp)
            return collection
        else:
            collection = biocjson.loads(bioc_json)
            return collection

    @staticmethod
    def save_as_collection(list_of_pymedDocs):
        thisBiocCollection = bioc.BioCCollection()
        for thisPymedDoc in list_of_pymedDocs:
            thisBiocDoc = bioc.BioCDocument()
            for annot in thisPymedDoc.annotations:
                # print(annot.type)
                print(annot.source)
                if annot.type == "raw_text":
                    if thisBiocCollection.source =='':
                        thisBiocCollection.source=annot.source
                if annot.source == "BioCPassage":
                    print(annot.ngram)
                    print(annot.value)
                    thisPassage = bioc.BioCPassage()
                    thisPassage.text = annot.ngram
                    thisPassage.offset = annot.span[0]
                    thisBiocDoc.add_passage(thisPassage)
                    # passageAttributes to add
                elif annot.source =="BioCAnnotation":
                    thisAnnotation = bioc.BioCAnnotation()
                    thisAnnotation.infons = annot.attributes
                    thisAnnotation.id = annot.attributes["id"]
                    thisAnnotation.text = annot.ngram
                    thisLocation = bioc.BioCLocation(annot.span[0],annot.span[1]-annot.span[0])
                    thisAnnotation.add_location(thisLocation)
                    thisBiocDoc.passages[-1].add_annotation(thisAnnotation)
            thisBiocCollection.add_document(thisBiocDoc)

    @staticmethod
    def writeBiocCollection(filename, collection):
        with bioc.BioCXMLDocumentWriter(filename) as writer:
            writer.write_collection_info(collection)
            for document in collection.documents:
                writer.write_document(document)
        return 1
