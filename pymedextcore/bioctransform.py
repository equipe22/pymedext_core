
from typing import List, Optional

import bioc
from bioc import biocjson
from .datatransform import DataTransform
from .document import Document
from .annotators import Annotation
import uuid

class BioC(DataTransform):
    @staticmethod
    def load_collection(bioc_input: str,format: int =0, is_file: bool  = True):
        """load a bioc collection xml or json.
        It will return a list of Document object.

        :param bioc_input: a str path to a bioc file or a bioc input string
        :param format: xml or to_json type of the bioc file
        :param is_file: if True bioc_input is path else it is a string
        :returns: list of Document
        """
        collection = None
        if format == 0:
            collection = BioC.__load_collection_xml(bioc_input, is_file)
        else :
            collection = BioC.__load_collection_json(bioc_input, is_file)
        annotations_list=[]
        raw_text = ""
        raw_text_ID=str(uuid.uuid1())
        # document source = collection.source
        documents_collection =[]
        for doc in collection.documents:
            for passage in doc.passages:
                raw_text = raw_text + passage.text
                passage_ID= str(uuid.uuid1())
                if "section_type" in passage.infons:
                    passage_attribute = {value:passage.infons[value]
                                  for value in passage.infons  if value not in ["section_type"] }
                    annotations_list.append(
                        Annotation(type=passage.infons["section_type"],
                                              value=passage.text,
                                              ngram = passage.text,
                                              source_ID=raw_text_ID,
                                              ID=passage_ID,
                                              source="BioCPassage",
                                              span=(passage.offset,passage.offset+len(passage.text)))
                        )
                else:
                     annotations_list.append(
                        Annotation(type="BioCPassage",
                                              value=passage.text,
                                              ngram = passage.text,
                                              source_ID=raw_text_ID,
                                              ID=passage_ID,
                                              source="BioCPassage",
                                              span=(passage.offset,passage.offset+len(passage.text)))
                        )

                relations_annot_dict=dict()
                if passage.annotations:
                    for this_annotation in passage.annotations:
                        annotation_ID= str(uuid.uuid1())
                        identifier =None
                        if "identifier" in this_annotation.infons.keys() :
                            identifier=this_annotation.infons["identifier"]
                        elif "Identifier" in this_annotation.infons.keys() :
                            identifier=this_annotation.infons["Identifier"]
                        this_attributes = {value:this_annotation.infons[value]
                                          for value in this_annotation.infons  if value not in ["type","identifier","Identifier"] }
                        this_attributes["id"]=this_annotation.id
                        relations_annot_dict[this_annotation.id]=(this_annotation.locations[0].offset,this_annotation.locations[0].offset+ this_annotation.locations[0].length)
                        this_type = str(type(this_annotation)).replace(">","").replace("<","").replace("class ","").replace("bioc.bioc.","").replace("'","")
                        annotations_list.append(
                           Annotation(type=this_annotation.infons["type"],
                                      value=identifier,
                                      ngram =this_annotation.text,
                                      source_ID=passage_ID,
                                      ID=annotation_ID,
                                      source=this_type,
                                      span=(this_annotation.locations[0].offset,this_annotation.locations[0].offset+ this_annotation.locations[0].length),
                                      attributes =this_attributes, isEntity=True)
                            )
                if passage.relations:
                    for this_relation in passage.relations:
                        annotation_ID= str(uuid.uuid1())
                        identifier =None
                        if "identifier" in this_relation.infons.keys() :
                            identifier=this_relation.infons["identifier"]
                        elif "Identifier" in this_relation.infons.keys():
                            identifier=this_relation.infons["Identifier"]
                        this_attributes = {value:this_relation.infons[value]
                                          for value in this_relation.infons  if value not in ["type","identifier","Identifier"] }
                        this_attributes["id"]=this_relation.id
                        this_type = str(type(this_relation)).replace(">","").replace("<","").replace("class ","").replace("bioc.bioc.","").replace("'","")
                        for refNode in this_relation.nodes:
                            annotations_list.append(
                               Annotation(type=this_relation.infons["type"],
                                          value=identifier,
                                          ngram ="Null",
                                          source_ID=passage_ID,
                                          ID=annotation_ID,
                                          source=this_type,
                                          span= relations_annot_dict[refNode.refid],
                                          attributes=this_attributes)
                                )

            this_document = Document(raw_text =raw_text,ID =raw_text_ID, source = collection.source, documentDate = collection.date)
            # attributes=collection.key,collection.standalone,
            # collection.encoding,collection.version
            # collection.infons
            this_document.annotations.extend(annotations_list)
            documents_collection.append(this_document)
        return(documents_collection)

    @staticmethod
    def save_as_collection(list_of_pymedext_documents: List[Document]):
        """save a list of pymedext document as a bioc collection .
        It will return a bioc collection object.

        :param list_of_pymedext_documents: a list of Document
        :returns:  a bioc collection object
        """
        this_bioc_collection = bioc.BioCCollection()
        for this_pymedext_doc in list_of_pymedext_documents:
            this_bioc_doc = bioc.BioCDocument()
            for annot in this_pymedext_doc.annotations:
                # print(annot.type)
                print(annot.source)
                if annot.type == "raw_text":
                    if this_bioc_collection.source =='':
                        this_bioc_collection.source=annot.source
                if annot.source == "BioCPassage":
                    print(annot.ngram)
                    print(annot.value)
                    this_passage = bioc.BioCPassage()
                    this_passage.text = annot.ngram
                    this_passage.offset = annot.span[0]
                    this_bioc_doc.add_passage(this_passage)
                    # passageAttributes to add
                elif annot.source =="BioCAnnotation":
                    this_annotation = bioc.BioCAnnotation()
                    this_annotation.infons = annot.attributes
                    this_annotation.id = annot.attributes["id"]
                    this_annotation.text = annot.ngram
                    thisLocation = bioc.BioCLocation(annot.span[0],annot.span[1]-annot.span[0])
                    this_annotation.add_location(thisLocation)
                    this_bioc_doc.passages[-1].add_annotation(this_annotation)
            this_bioc_collection.add_document(this_bioc_doc)
        return(this_bioc_collection)


    @staticmethod
    def write_bioc_collection(filename:str, collection:bioc.BioCCollection):
        """write a BiocCollection as an xml document
        It will return 1

        :param filename: a str filename of the collection
        :param collection: a bioc collection
        :returns: 1
        """
        with bioc.BioCXMLDocumentWriter(filename) as writer:
            writer.write_collection_info(collection)
            for document in collection.documents:
                writer.write_document(document)
        return(1)

    def __load_collection_xml(bioc_xml: str, is_file: bool  = True):
        """load a xml bioc collection.
        It will return a bioc collection object.

        :param bioc_xml: a str path to a bioc file or a bioc input xml string
        :param is_file: if True bioc_input is a path else it is a string
        :returns:  a bioc collection object
        """
        if is_file :
            with open(bioc_xml, 'r') as fp:
                collection = bioc.load(fp)
            return(collection)
        else:
            collection = bioc.loads(bioc_xml)
            return(collection)

    def __load_collection_json(bioc_json: str, is_file: bool  =True):
        """load a json bioc collection .
        It will return a bioc collection object.

        :param bioc_json: a str path to a bioc file or a bioc input json string
        :param is_file: if True bioc_input is a path else it is a string
        :returns:  a bioc collection object
        """
        if is_file:
            with open(bioc_json, 'r') as fp:
                collection = biocjson.load(fp)
            return(collection)
        else:
            collection = biocjson.loads(bioc_json)
            return(collection)
