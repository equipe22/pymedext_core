import uuid
import json
import os

from .document import Document

from .doccanodocument import DoccanoDocument

from .annotators import Annotator, Annotation
from .doccanoannotator import DoccanoAnnotation

from .datatransform import DataTransform


class Doccano(DataTransform):
    """
    This class defines a set of transformation methods to build a DoccanoDocument with several pymedext Document objects.
    A doccanoDocument contains N doccanoAnnotations, that the user want to evaluate in Doccano interface.

    Here the transoformation methods are specific to scanner report extractions, and DrWH negation, hypothesis and family context detections.
    Other transformation methods could be defined according to what the user want to evaluate.
    """

    # def load(DoccanoDocument):
    #     return Document
    #
    # def save(Docment, type=None, attribute= None, value=None, span=None, dict_regex_type = None, path_to_pb_doc = None, regex = None, which_kind_of_doccano = None ):
    #     """
    #
    #     :param type:
    #     :param attribute:
    #     :param value:
    #     :param span:
    #     :param which_kind_of_doccano:
    #     :return:
    #     """
    #     if which_kind_of_doccano == "ima_precision" :
    #         dict_doccano = toDoccanoImaPrecision(Document, type=type, attribute=attribute)
    #
    #     elif which_kind_of_doccano == "ima_rappel":
    #         dict_doccano = toDoccanoImaRappel(Document, dict_regex_type=dict_regex_type, value=value, span=span)
    #
    #     elif which_kind_of_doccano == "ima_pb":
    #         dict_doccano = toDoccanoPb(Document, path_to_doc=path_to_pb_doc, regexp = regex)
    #
    #     else :
    #         print("Please enter the doccano eval you which to do.")
    #
    #     DoccanoDocument = docForDoccano(dict_doccano)
    #
    #     return DoccanoDocument



    def toDoccanoImaPrecision(Document, type, attribute=None):
        """Specific method for scanner extractor evaluation
        Selects the value extracted of the desired item in the pymedext Document.
        Returns a dict with the context as key, and the value extracted as value.

        Ex : Extract of a pymedextDocument  :
        "
        ...

        {
            "type": "motif",
            "value": "non évocateur",
            "span": [
                2026,
                2039
            ],
            "source": "annotator_section_img",
            "source_ID": "eae2fd1e-8096-11ea-9260-e470b8d2ff7c",
            "isEntity": false,
            "attributes": "ISCOVID",
            "id": "eae2fd1c-8096-11ea-b180-e470b8d2ff7c"
        }
        ...
        "

        An extract of pymedextDocument.toDoccanoImaPrecision(type="motif", attribute="ISCOVID") return will be :

        {...,<raw_text[2026,2039]> : "non évocateur",...}

        where raw_text[2026,2039] is the context of the extraction, a short extract of the report text around the extraction.

        :param type: the type of the item ("rubrique" or "motif")
        :param attribute: item of interest (ex : "ISCOVID")
        :return: a dict with litteral context as key and value extracted as value
        :rtype: dict
        """

        ## Les regexp sont dans attributes


        objects_list = Document.get_annotations(_type=type, attributes=attribute)
        raw_text = Annotation.to_dict(Document.get_annotations(_type="raw_text")[0])['value']
        dict_doccano = {}

        for el in objects_list:
            dict_el = Annotation.to_dict(el)
            span = dict_el["span"]
            if type != "rubrique":
                if dict_el["value"] != "NULL" and dict_el["value"] is not None:
                    text = "Valeur extraite :" + dict_el["value"] + "\n" + "Snippet : \n" + raw_text[
                                                                                            span[0] - 70:span[
                                                                                                             1] + 70]
                    dict_doccano[text] = attribute
            else:
                if dict_el["value"] != "NULL" and dict_el["value"] is not None:
                    text = "Valeur extraite :" + dict_el["value"] + "\n" + "Snippet : \n" + raw_text[
                                                                                            span[0]:span[1]]

                    dict_doccano[text] = attribute

        return dict_doccano


    def toDoccanoImaRappel(Document, dict_regexp_type, value, span):
        """Specific method for scanner extractor evaluation
        Founds the absent item in a pymedext Document.

        :param dict_regexp_type: a dict of with the item as key (ex: "ISCOVID") and their type as value ("motif" or "rubrique")
        :param value: "Null"
        :return: A dict with the report text as key and a list of absent item as value
        :rtype: dict
        """

        doccano_dict = {}

        for regexp in dict_regexp_type:

            objects_list = Document.get_annotations(_type=dict_regexp_type[regexp], attributes=regexp, value=value,
                                                span=span)

            if len(objects_list) > 0:
                raw_text = Annotation.to_dict(Document.get_annotations(_type="raw_text")[0])['value']
                if raw_text not in doccano_dict:
                    doccano_dict[raw_text] = [regexp]
                else:
                    doccano_dict[raw_text].append(regexp)

        return doccano_dict

    def toDoccanoPb(Document, path_to_doc, regexp):
        """Specific method for scanner extractor evaluation
        A specific format to display documents that were annoted with label "problem" in Doccano

        :param path_to_doc: the path to the doc that was annoted with problem label in Doccano
        :param regexp: the item of interest
        :return: a dict with the text report as key and the regex as value
        """

        doccano_dict_pb = {}
        path_to_doc = os.path.abspath(path_to_doc)
        raw_text = Annotation.to_dict(Document.get_annotations(_type="raw_text")[0])['value']
        text = "Valeur extraite : " + regexp + "\n" + "Texte du compte-rendu annoté probleme :\n" + raw_text

        doccano_dict_pb[text] = [path_to_doc, regexp]

        return doccano_dict_pb


    def toDoccanoDrWH(Document, type, segment):
        """Specific method for DrWH evaluation
        Selects the drwh annotation and their value and creat a dict with syntagm/sentence as key and class value of the syntagm/sentence as value.

        Ex : Extract of a pymedextDocument

        "
        ...
        {
            "type": "drwh_syntagms",
            "value": " Le patient présente un diabète de type II",
            "span": [
                47,
                91
            ],
            "source": "DRWH_syntagms.v1",
            "source_ID": "74633e84-80a3-11ea-a7f6-180f76073bf2",
            "isEntity": false,
            "attributes": null,
            "id": "74633e89-80a3-11ea-a7f6-180f76073bf2"
        }
        ...

        {
            "type": "drwh_negation",
            "value": "non negatif",
            "span": [
                47,
                91
            ],
            "source": "DRWH_negation.v1",
            "source_ID": "74633e89-80a3-11ea-a7f6-180f76073bf2",
            "isEntity": false,
            "attributes": null,
            "id": "74633e95-80a3-11ea-a7f6-180f76073bf2"
        }
        ...

        An extract of pymedextDocument.toDoccanoDrWH(type=dwh_negation, segment=dwh_syntagm) return will be:

        {...,"Le patient présente un diabète de type II"="non negatif"...,}

        :param type: dwh type of class ("dwh_negation" or "dwh_hypothesis" or "dwh_family")
        :param segment: syntagm or sentence ("dwh_sentence" or "dwh_syntagm")
        :return: a dict with syntagm or sentence as key and class as value
        :rtype: dict
        """

        objects_list = Document.get_annotations(_type=type)
        dict_source_ID = {}
        dict_doccano = {}

        for el in objects_list:
            dict_el = Annotation.to_dict(el)
            source_ID = dict_el["source_ID"]
            value = dict_el["value"]
            dict_source_ID[source_ID] = value  # negatif ou non negatif

        for source_ID in dict_source_ID:
            list_uniq_result = Document.get_annotations(_type=segment, target_id=source_ID)
            for el in list_uniq_result:
                text = Annotation.to_dict(el)["value"]
                dict_doccano[text] = dict_source_ID[source_ID]

        return dict_doccano


    def docForDoccano(dict_doccano):
        """Creats a DoccanoDoc object with dict in input

        :return: DoccanoDocument object
        :rtype : DoccanoDocument
        """
        thisDoccanoDoc = DoccanoDocument
        thisDoccanoDoc.annotationsDoccano = []
        for text in dict_doccano:
            labels = [dict_doccano[text]]
            meta = {"pymedext_name": dict_doccano[text][0]}
            thisDoccanoDoc.doccanoAnnotation.append(DoccanoAnnotation(text=text,
                                                                       labels=labels,
                                                                       meta=meta))
        return thisDoccanoDoc


    def DoccanoEvalRappel(DoccanoDocument, dict_doccano, path_to_doc):
        """Adds DoccanoAnnotation objects to a DoccanoDocument object, with a dict created with toDoccanoImaRappel

        :param dict_doccano: a dict created with toDoccanoImaRappel method
        :param path_to_doc: the path of the pymedext doc that was used to create dict_doccano
        :return: DoccanoDocument object
        :rtype: DoccanoDocument
        """

        path_to_doc = os.path.abspath(path_to_doc)

        for text in dict_doccano:
            labels = dict_doccano[text]
            meta = {"pymedext_name": path_to_doc}
            DoccanoDocument.doccanoAnnotation.append(DoccanoAnnotation(text=text,
                                                     labels=labels,
                                                     meta=meta
                                                             ))
        return DoccanoDocument

    def DoccanoEvalN(DoccanoDocument, dict_doccano, number_annoted, number_eval, path_to_doc):
        """
        Adds DoccanoAnnotation objects to DoccaDocument until a specified number of evaluations.

        :param dict_doccano: A doccano dict that will be filled until it reachs the desired number of annotations.
        :param number_annoted: the number of evaluations desired.
        :param number_eval: the current number of annotation.
        :return: A list with the modified DoccanoDocument object, and the number of annotations
        :rtype: list
        """

        for text in dict_doccano:
            if number_annoted < number_eval:
                number_annoted += 1
                path_to_doc = os.path.abspath(path_to_doc)
                # print("inside DoccanoEvalN", number_annoted)
                DoccanoDocument.doccanoAnnotation.append(DoccanoAnnotation(text=text,
                                                                 labels=["x" + dict_doccano[text]],
                                                                 meta={"pymedext_name": path_to_doc}))
        return [DoccanoDocument, number_annoted]

    def DoccanoEvalClass(DoccanoDocument, dict_doccano, dictClasses, number_eval, path_to_doc):
        """Adds doccano annotations to DoccanoDocument object until a specified number of evaluations for both classes.

        :param dict_doccano: A doccano dict that will be filled until the two classes reach the desired number of annotations
        :param dictClasses: A dict of doccano classes (ex : negatif vs non negatif) with their current occurences.
        :param number_eval: the number of evaluations desired
        :return: A list with the modified Doccano Object, and a dict of annotations classes, with their number
        :rtype: list
        """

        for text in dict_doccano:
            path_to_doc = os.path.abspath(path_to_doc)

            if dict_doccano[text] not in dictClasses:  # on ne sait pas quelles sont les étiquettes
                dictClasses[dict_doccano[text]] = 1
                DoccanoDocument.doccanoAnnotation.append(DoccanoAnnotation(text=text,
                                                                 labels=[dict_doccano[text]],
                                                                           meta={"pymedext_name": path_to_doc}))
            elif dictClasses[
                dict_doccano[text]] < number_eval:  # si l'étiquette n'a pas le nombre désiré d'évaluation, on l'ajoute
                dictClasses[dict_doccano[text]] += 1

                DoccanoDocument.doccanoAnnotation.append(DoccanoAnnotation(text=text,
                                                                 labels=[dict_doccano[text]],
                                                                            meta={"pymedext_name": path_to_doc}))

        return [DoccanoDocument, dictClasses]
