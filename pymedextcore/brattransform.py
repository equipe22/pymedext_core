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
    def save_to_brat(list_of_documents: List[Document] = None, folder_path: str = None,
                     pym_ann_types: List[str] = None,  # ["QuickUMLS", "regex"],
                     brat_entities_in_pym_types: List[str] = None,  # ["QuickUMLS", "regex"]
                     brat_entities_in_pym_types_value: List[str] = None,  # ["QuickUMLS", "regex"]
                     brat_entities_in_pym_att_values: dict = None,
                     brat_entities_in_pym_att_keys: dict = None,
                     brat_attributes: dict = None,  # {"QuickUMLS": ["negation", "context", "hypothesis"]},
                     pym_rel_types: List[str] = None,  # ["Stanza"]
                     brat_ents_of_rel_in_pym_rel_type: List[str] = None,  # ["Stanza"]
                     brat_ents_of_rel_in_pym_ent_value: List[str] = None,  # ["Stanza"]
                     brat_ents_of_rel_in_pym_att_values: dict = None,  # {"Stanza" : "upos" }
                     brat_type_of_rel_in_pym_rel_types: List[str] = None,  # ["Stanza"]
                     brat_type_of_rel_in_pym_rel_att_values: dict = None,  # {"Stanza": "deprel"}
                     level_annot: dict = None  # {"QuickUMLS : 0, "Stanza" : 1"}
                     # brat_ents_of_rel_in_pym_ent_att_keys : dict = None, #{"Stanza" : "upos"}
                     ):
        """
        This function will write all Annotations in Brat files at file_path.
        It will create (or overwrite) 2 files for each pymedext Documents in documents list input:
            - ID.ann: Brat annotation file (with ID = dic_pymedext.id)
            - ID.txt: Raw text of the document (with ID = dic_pymedext.id)
        It will create (or overwrite) an annotation.conf file.

        :param list_of_documents: List of Documents input. Documents should contain same type of annotations
        :param folder_path: path in string format. It will store files at this location. Folder needs to be created.


        For the other paramters, the extract of this pymedext document will be used in the examples, for a better understanding.

        '''

        {'type': 'QuickUMLS',
           'value': 'oesophagite',
           'ngram': None,
           'span': (188, 199),
           'source': 'QuickUMLS:v1',
           'source_ID': '6814e9fa-96f7-11eb-a8c8-0242ac110002',
           'isEntity': False,
           'attributes': {'hypothesis': 'certain',
                'context': 'patient',
                'negation': 'aff',
                'cui': 'C0014868',
                'label': 'oesophagite',
                'semtypes': ['T047'],
                'score': 1.0,
                'snippet': ' La fibroscopie oeso-gastro-duodénale avait révélé  une oesophagite peptique de grade II et a permis l’exérèse d’un petit papillome du tiers supérieur de l’œsophage',
                'snippet_span': (132, 296)},
       'ID': '681c2d82-96f7-11eb-a8c8-0242ac110002'},
        {'type': 'regex',
           'value': 'grade II',
           'ngram': None,
           'span': (212, 220),
           'source': 'RegexMatcher:v1',
           'source_ID': '68155570-96f7-11eb-a8c8-0242ac110002',
           'isEntity': True,
           'attributes': {'version': 'v1',
                'label': 'Grade',
                'id_regexp': 'id_grade',
                'snippet': '-gastro-duodénale avait révélé  une oesophagite peptique de grade II et a permis l’exérèse d’un petit papillome du tiers supérie',
                'hypothesis': 'certain',
                'context': 'patient',
                'negation': 'aff'},
           'ID': '682ca3ec-96f7-11eb-a8c8-0242ac110002'},

        '''

        annotations :
        :param pym_ann_types: Pymedext types of annotation selected.
        exemple : ['QuickUMLS', 'regex'] -> annotations in Brat will be about this two types of annotations. Depending on the different opitons filled (explained below), different labels will be displayed in brat.

        :param brat_entities_in_pym_types : (optional) if brat entities correpond to annotation types in pymedext, this list should be filled.
        exemple :  ['regex'] -> in brat, for each regex found, 'regex' will be displayed.
        With the extract given 'grade II' will be highlighted in the text with the label 'regex'.

        :param brat_entities_in_pym_types_value : if brat entities correpond to the value of annotation types in pymedext, this list should be filled.
        exemple :  ['QuickUMLS'] -> in brat, for each QuickUMLS found, the quickumls annotation value will be displayed.
        With the extract given 'oesophagite' will be highlighted in the text with the label 'QuickUMLS'.

        :param brat_entities_in_pym_att_values : (optional) if brat entities correspond to annotation attributes values in pymexdext, this dict should be filled. Keys correponds to pymedext annotation type, values correspond to pymedext attributes keys.
        exemple : {'regex': 'label'}  -> in brat for each regex found, the regex label in attributes  will be displayed.
        With the extract given 'grade II' will be highlighted in the text with the label 'Grade'.

        :param brat_entities_in_pym_att_keys : (optional) if brat entities correspond to annotation attributes keys in pymedext, this dict should be filled. Keys correponds to pymedext annotation type, values correspond to pymedext attributes keys.
        exemple : {'regex': 'label'} -> in brat, for each regex found, the string "label" will be diplayed.
        With the extract given 'grade II' will be highlighted in the text with the label 'label'.

        :param brat_attributes: (optional) Dict with pymedext annotation type as keys, and the correspondant attributes list that should be exported as Brat attributes.
        exemple : {"QuickUMLS": ['hypothesis', 'negation', 'context'] -> for each quickumls found, hypothesis, negation and context attribute values will be displayed.
        Put "all" as value if you want all the attributes for this annotation type
        exemple :{"QuickUMLS": "all"} for each QuickUMLS found, all attributes (semType, CUI code, hypothesis,... will be displayed.)

        relations :
        :param pym_rel_types: Pymedext types of relation selected.
        exemple : ['Stanza'] -> relations in Brat will be about this two types of relations. Depending on the different opitons filled (explained below), different labels will be displayed in brat.

        :param brat_ents_of_rel_in_pym_rel_type : (optional) if brat entities of relations correpond to relations types in pymedext, this list should be filled.

        :param brat_ents_of_rel_in_pym_ent_value : (optional) if brat entities of relations correpond to relations types in pymedext, this list should be filled.

        :return: 1
        """

        ### Initialisation

        all_brat_entities: List[str] = []
        all_brat_attributes: dict = {}

        if level_annot:
            dict_brat_level_entities = {}

        ### lists for annotations.conf file :

        # -- entities
        if brat_entities_in_pym_types:
            all_brat_entities = all_brat_entities + brat_entities_in_pym_types
        if brat_entities_in_pym_att_keys:
            all_brat_entities = all_brat_entities + list(brat_entities_in_pym_att_keys.values())
        # if brat_entities_in_pym_types_value, entities will be filled progressively in the loop.
        # if brat_entities_in_pym_att_values, entities will be filled progressively in the loop.

        ## -- entities of relations
        if brat_ents_of_rel_in_pym_rel_type:
            all_brat_entities = all_brat_entities + brat_ents_of_rel_in_pym_rel_type
        # if brat_ents_of_rel_in_pym_ent_value, entities will be filled progressively in the loop.

        ## -- relation types
        if pym_rel_types:
            dict_id_to_brat_ent_id: dict = {}  # keep the relation in a dict for the relation in the second loop
            dict_id_to_type_of_entity: dict = {}
            dict_type_of_relation: dict = {}
            if brat_type_of_rel_in_pym_rel_types:
                all_brat_entities = all_brat_entities + brat_type_of_rel_in_pym_rel_types
                for el_type in brat_type_of_rel_in_pym_rel_types:
                    dict_type_of_relation[el_type] = []
            # if brat_type_of_rel_in_pym_rel_att_values, relations types will be filled progressively

        ### Loop over the documents :

        for dic_pymedext in list_of_documents:

            # ----- Annotation file -----
            doc_id = dic_pymedext.ID
            brat_annotations: str = ""
            instance_annotation = 0
            instance_attributes = 0
            instance_relation = 0

            ## Loop over the annotation objects of the document
            for annotation in dic_pymedext.annotations:

                brat_entity = None

                # Entity of annotation
                if pym_ann_types and annotation.type in pym_ann_types:
                    # find the brat entity
                    if brat_entities_in_pym_types:
                        brat_entity = annotation.type
                    if brat_entities_in_pym_types_value:
                        brat_entity = annotation.value
                        # fill the conf file progressively for this option
                        if brat_entity not in all_brat_entities:
                            all_brat_entities.append(brat_entity)
                    if brat_entities_in_pym_att_keys:
                        if annotation.type in brat_entities_in_pym_att_keys:
                            attributes: dict = annotation.attributes
                            brat_entity = brat_entities_in_pym_att_keys[annotation.type]
                    if brat_entities_in_pym_att_values:
                        attributes: dict = annotation.attributes
                        brat_entity = attributes[brat_entities_in_pym_att_values[annotation.type]]
                        # fill the conf file progressively for this option
                        if brat_entity not in all_brat_entities:
                            all_brat_entities.append(brat_entity)

                # Entity of relation
                if pym_rel_types and annotation.type in pym_rel_types:  # entity of relation
                    # fill the dict
                    dict_id_to_brat_ent_id[annotation.ID] = 'T' + str(instance_annotation)
                    # find the entity
                    if brat_ents_of_rel_in_pym_rel_type:
                        brat_entity = annotation.type  # 'Stanza'
                        dict_id_to_type_of_entity[annotation.ID] = brat_entity
                    if brat_ents_of_rel_in_pym_ent_value:
                        brat_entity = annotation.value
                        dict_id_to_type_of_entity[annotation.ID] = brat_entity
                        # fill the conf file progressively for this option
                        if brat_entity not in all_brat_entities:
                            all_brat_entities.append(brat_entity)
                    if brat_ents_of_rel_in_pym_att_values:
                        attributes: dict = annotation.attributes
                        brat_entity = attributes[
                            brat_ents_of_rel_in_pym_att_values[annotation.type]]  # for Stanza, value of 'upos'
                        dict_id_to_type_of_entity[annotation.ID] = brat_entity
                        # fill the conf file progressively for this option
                        if brat_entity not in all_brat_entities:
                            all_brat_entities.append(brat_entity)

                if level_annot and annotation.type in level_annot:
                    dict_brat_level_entities[brat_entity] = level_annot[annotation.type]

                if brat_entity:
                    # -- Writing annotations --
                    bratline = 'T' + str(instance_annotation) + '\t' + brat_entity + ' ' + str(annotation.span[0]) \
                               + ' ' + str(annotation.span[1]) + '\t' + str(annotation.value)
                    brat_annotations += f"{bratline}\n"

                # Dealing with attributes
                if brat_attributes and annotation.type in brat_attributes:  # if export_attibutes dict is not None, and annotatio
                    attributes: dict = annotation.attributes
                    if "all" in brat_attributes[annotation.type]:
                        for attribute_key in attributes:
                            if attribute_key not in all_brat_attributes:
                                """
                                all_brat_attributes is like:
                                {"Family": (
                                        "syntagme",
                                        ["patient", "family"])
                                }
                                """
                                all_brat_attributes.update(
                                    {attribute_key: (annotation.type, [attributes.get(attribute_key)])})
                            # adding entry for attribute values like "neg" or "aff" for Negation key to the list (2nd in tuple)
                            elif attributes.get(attribute_key) not in all_brat_attributes.get(attribute_key)[1]:
                                all_brat_attributes.get(attribute_key)[1].append(attributes.get(attribute_key))

                            # -- writing attributes --
                            bratline = 'A' + str(instance_attributes) + '\t' + attribute_key + ' ' + \
                                       f"T{instance_annotation}" + " " + str(attributes.get(attribute_key))
                            brat_annotations += f"{bratline}\n"

                            instance_attributes += 1
                    else:
                        for attribute_key in brat_attributes[
                            annotation.type]:  # for each attributes expected to be annoted in the value list
                            # adding entry for attribute key (like Negation or Family)
                            if attribute_key not in all_brat_attributes:
                                all_brat_attributes.update(
                                    {attribute_key: (annotation.type, [attributes.get(attribute_key)])})
                            # adding entry for attribute values like "neg" or "aff" for Negation key to the list (2nd in tuple)
                            elif attributes.get(attribute_key) not in all_brat_attributes.get(attribute_key)[1]:
                                all_brat_attributes.get(attribute_key)[1].append(attributes.get(attribute_key))

                            # -- writing attributes --
                            bratline = 'A' + str(instance_attributes) + '\t' + attribute_key + ' ' + \
                                       f"T{instance_annotation}" + " " + str(attributes.get(attribute_key))
                            brat_annotations += f"{bratline}\n"

                            instance_attributes += 1

                # -- Increments instance_annotations --
                if brat_entity:
                    instance_annotation += 1

            # Dealing with relations
            ## Loop over the relation objects of the document
            if pym_rel_types:

                for relation in dic_pymedext.relations:

                    if relation.type in pym_rel_types:

                        brat_relation = None

                        ent_brat_ID_1 = dict_id_to_brat_ent_id[relation.head]
                        ent_brat_ID_2 = dict_id_to_brat_ent_id[relation.target]
                        type_ent_1 = dict_id_to_type_of_entity[relation.head]
                        type_ent_2 = dict_id_to_type_of_entity[relation.target]
                        if brat_type_of_rel_in_pym_rel_types:
                            brat_relation = relation.type
                            if [type_ent_1, type_ent_2] not in dict_type_of_relation[brat_relation]:
                                dict_type_of_relation[brat_relation].append([type_ent_1, type_ent_2])
                        if brat_type_of_rel_in_pym_rel_att_values:
                            attributes: dict = relation.attributes
                            brat_relation = attributes[brat_type_of_rel_in_pym_rel_att_values[relation.type]]
                            if brat_relation not in dict_type_of_relation:
                                dict_type_of_relation[brat_relation] = [[type_ent_1, type_ent_2]]
                            elif [type_ent_1, type_ent_2] not in dict_type_of_relation[brat_relation]:
                                dict_type_of_relation[brat_relation].append([type_ent_1, type_ent_2])
                        if brat_relation:
                            # -- Writing relations annotations --
                            bratline_rel = 'R' + str(
                                instance_relation) + '	' + brat_relation + ' Arg1:' + ent_brat_ID_1 + ' Arg2:' + ent_brat_ID_2
                            brat_annotations += f"{bratline_rel}\n"

                            # -- Increments instance_relation
                            instance_relation += 1

                            # writting file
            f_brat = open(f"{folder_path}/{doc_id}.ann", 'w')
            # print("brat_annotations", brat_annotations)
            f_brat.write(brat_annotations)
            f_brat.close()

            # ----- raw text -----
            # raw_text = dic_pymedext.raw_text()
            # raw_text = dic_pymedext.annotations[1]['value']
            raw_text = dic_pymedext.annotations[1].value
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
        for entity in all_brat_entities:
            if level_annot:
                if entity in dict_brat_level_entities:
                    level = "    " * dict_brat_level_entities[entity]
                    entities += level + entity + "\n"
                else:
                    entities += f"{entity}\n"
            else:
                entities += f"{entity}\n"

        relations: str = "\n[relations]\n\n"
        events: str = "\n[events]\n"
        attributes: str = "\n[attributes]\n\n"

        if brat_attributes:
            for attribute in all_brat_attributes:
                list_value = [str(el) for el in all_brat_attributes.get(attribute)[1]]
                annotation_type = all_brat_attributes.get(attribute)[0]
                # add default value in order to make the attribute multi valuated.
                # If not, it will mark the attribute as true
                if len(list_value) == 1:
                    list_value.append("default")
                attributes += str(attribute) + "\t" + "Arg:" + str(annotation_type) + ", Value:" + "|".join(
                    list_value) + "\n"

        if pym_rel_types:
            if dict_type_of_relation:
                for relation in dict_type_of_relation:
                    for el in dict_type_of_relation[relation]:
                        relations += relation + '	' + 'Arg1:' + el[0] + ', ' + 'Arg2:' + el[1] + "\n"

        conf_file = entities + relations + events + attributes
        f_brat = open(f"{folder_path}/annotation.conf", 'w')
        f_brat.write(conf_file)
        f_brat.close()
        return (1)

    @staticmethod
    def load_from_brat(ann_file: str,
                       txt_file: Optional[str] = None) -> Document:
        """Load annotations from a .ann file in the Brat format

        :param ann_file: path to the .ann file
        :param txt_file: path to the corresponding .txt file, if None: defaults to replacing .ann by .txt
        :returns: Document
        :rtype: Document
        """
        entities, relations, attributes = read_file_annotations(ann_file)
        annotations_list = []
        relations_list = []

        if txt_file is None:
            txt_file = ann_file.replace(".ann", ".txt")

        raw_text = open(txt_file, 'r').read()
        raw_text_ID = str(ann_file.replace(".ann", ""))

        doc = Document(raw_text=raw_text, ID=raw_text_ID, source=ann_file)

        raw_id = doc.get_annotations('raw_text')[0].ID

        for entity in entities:
            for span in entity.span:
                ID = entity.id
                annotations_list.append(
                    Annotation(type=entity.type,
                               value=entity.text,
                               ngram=entity.text,
                               source_ID=raw_id,
                               ID=ID,
                               source="BratFile",
                               span=(span[0], span[1]),
                               isEntity=True
                               )
                )

        for relation in relations:
            relations_list.append(
                Relation(type=relation.type,
                         head=relation.subj,
                         target=relation.obj,
                         ID=relation.id,
                         source_ID=raw_id,
                         source="BratFile")
            )

        doc.annotations.extend(annotations_list)
        doc.relations.extend(relations_list)

        return (doc)

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
