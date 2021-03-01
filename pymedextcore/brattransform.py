# -*- coding: utf-8 -*-

"""
Created 2020/04/14

@author: David BAUDOIN

fonction : creation ou update  d'un fichier BRAT a partir d'un dic pymedext

"""
from typing import List, Optional

from .datatransform import DataTransform
import logging
logger = logging.getLogger(__name__)
import uuid
from .brat_parser import read_file_annotations
from .annotators import Annotation, Relation
from .document import Document


class brat(DataTransform):
    def savetobrat(dic_pymedext: Document, folder_path: str,
                   exclusion: List[str] = ["raw_text", "sentence", "endlines"],
                   export_attributes: bool = False):
        """
        This function will write all Annotations in Brat files at file_path.
        It will create (or overwrite) 3 files:
            - annotation.conf:
            - ID.ann: Brat annotation file (with ID = dic_pymedext.id)
            - ID.txt: Raw text of the document (with ID = dic_pymedext.id)

        :param dic_pymedext: Document input, should containes annotations
        :param folder_path: path in string format. It will store files at this location. Folder needs to be created.
        :param exclusion: list of "type" to exclude from saving = ["raw_text", "sentence", "endlines"] by default
        :param export_attributes: if True, it will export attributes as Brat attributes.
        :return: None
        """
        all_annotation_types: List[str] = []
        all_attribute_types: dict = {}
        doc_id = dic_pymedext.ID
        # ----- Annotation file -----
        brat_annotations: str = ""
        instance_annotation = 0
        instance_attributes = 0
        for annotation in dic_pymedext.annotations:
            if annotation.type not in exclusion:
                # -- adding type to unique list of annotation type (for conf file) --
                if annotation.type not in all_annotation_types:
                    all_annotation_types.append(annotation.type)

                # -- Writing annotations --
                bratline = 'T' + str(instance_annotation) + '\t' + annotation.type + ' ' + str(annotation.span[0]) \
                           + ' ' + str(annotation.span[1] + 1) + '\t' + str(annotation.value)
                brat_annotations += f"{bratline}\n"

                # Dealing with attributes
                attributes: dict = annotation.attributes
                if export_attributes and attributes:
                    for attribute_key in attributes:
                        # adding entry for attribute key (like Negation or Family)
                        if attribute_key not in all_attribute_types:
                            """
                            all_attribute_types is like:
                            {"Family": (
                                    "syntagme",
                                    ["patient", "family"])
                            }
                            """
                            all_attribute_types.update(
                                {attribute_key: (annotation.type, [attributes.get(attribute_key)])})
                        # adding entry for attribute values like "neg" or "aff" for Negation key to the list (2nd in tuple)
                        elif attributes.get(attribute_key) not in all_attribute_types.get(attribute_key)[1]:
                            all_attribute_types.get(attribute_key)[1].append(attributes.get(attribute_key))

                        # -- writing attributes --
                        bratline = 'A' + str(instance_attributes) + '\t' + attribute_key + ' ' + \
                                   f"T{instance_annotation}" + " " + attributes.get(attribute_key)
                        brat_annotations += f"{bratline}\n"

                        instance_attributes += 1

                instance_annotation += 1

        f_brat = open(f"{folder_path}/{doc_id}.ann", 'w')
        f_brat.write(brat_annotations)
        f_brat.close()

        # ----- raw text -----
        raw_text = dic_pymedext.raw_text()
        f_brat = open(f"{folder_path}/{doc_id}.txt", 'w')
        f_brat.write(raw_text)
        f_brat.close()

        # ----- conf file -----
        """
        Attributes section is like:

        [attributes]
        hypothesis	Arg:Syntagme, Value:certain|hypothesis
        context Arg:Syntagme, Value:family|patient
        negation Arg:Syntagme, Value:neg|aff
        """
        entities: str = "[entities]\n\n"
        for entity in all_annotation_types:
            entities += f"{entity}\n"

        relations: str = "\n[relations]\n\n"
        events: str = "\n[events]\n"
        attributes: str = "\n[attributes]\n\n"
        if export_attributes:
            for attribute in all_attribute_types:
                list_value = all_attribute_types.get(attribute)[1]
                annotation_type = all_attribute_types.get(attribute)[0]
                # add default value in order to make the attribute multi valuated.
                # If not, it will mark the attribute as true
                if len(list_value) == 1:
                    list_value.append("default")
                attributes += attribute + "\t" + "Arg:" + annotation_type + ", Value:" + "|".join(list_value) + "\n"
        conf_file = entities + relations + events + attributes
        f_brat = open(f"{folder_path}/annotation.conf", 'w')
        f_brat.write(conf_file)
        f_brat.close()
        return(1)

    @staticmethod
    def load_from_brat(ann_file: str,
                       txt_file: Optional[str] = None) -> Document:
        """Load annotations from a .ann file in the Brat format

        :param ann_file: path to the .ann file
        :param txt_file: path to the corresponding .txt file, if None: defaults to replacing .ann by .txt
        :returns: Document
        :rtype: Document
        """
        entities, relations, attributes =read_file_annotations(ann_file)
        annotations_list=[]
        relations_list = []

        if txt_file is None:
            txt_file = ann_file.replace(".ann",".txt")

        raw_text = open(txt_file, 'r').read()
        raw_text_ID=str(ann_file.replace(".ann", ""))

        doc = Document(raw_text =raw_text,ID =raw_text_ID, source = ann_file)

        raw_id = doc.get_annotations('raw_text')[0].ID

        for entity in entities:
            for span in entity.span:
                ID = entity.id
                annotations_list.append(
                            Annotation(type=entity.type,
                                    value=entity.text,
                                    ngram = entity.text,
                                    source_ID=raw_id,
                                    ID=ID,
                                    source="BratFile",
                                    span=(span[0],span[1]),
                                    isEntity=True
                            )
                    )

        for relation in relations:
            relations_list.append(
                Relation(type= relation.type,
                        head = relation.subj,
                        target = relation.obj,
                        ID = relation.id,
                        source_ID = raw_id,
                        source = "BratFile")
            )

        doc.annotations.extend(annotations_list)
        doc.relations.extend(relations_list)

        return(doc)




    # def update(dic_pymedext, bratFilePath_ann):
    #     f_brat = open(bratFilePath_ann, 'r')
    #     lastline = ''
    #     for line in f_brat:
    #         lastline = line
    #     f_brat.close()
    #     try:
    #         instance_brat = int(lastline.split('   ')[0][1:])
    #         f_brat = open(bratFilePath_ann, 'a')
    #         for element in dic_pymedext['annotations']:
    #             bratline = 'T' + str(instance_brat) + '	' + dic_pymedext['annotations']['type'] + ' ' + str(dic_pymedext['annotations']['span'][0]) \
    #                        + ' ' + str(dic_pymedext['annotations']['span'][0]) + '	' + str(dic_pymedext['annotations']['value'])
    #             instance_brat += 1
    #             f_brat.write(bratline)
    #             f_brat.write('\n')
    #         f_brat.close()
    #     except:
    #         logger.info('cannot turn into int the value : ' + str(lastline.split('   ')[0]))
