import uuid
import json
import os

from .document import Document

from .doccanodocument import DoccanoDocument

from .annotators import Annotator, Annotation
from .doccanoannotator import DoccanoAnnotation

from .datatransform import DataTransform

class DoccanoTransform(DataTransform, Document, DoccanoDocument):

    def load(DoccanoDocument):
        return Document

    def save(Docment, type=None, attribute= None, value=None, span=None, dict_regex_type = None, path_to_pb_doc = None, regex = None, which_kind_of_doccano = None ):
        """

        :param type:
        :param attribute:
        :param value:
        :param span:
        :param which_kind_of_doccano:
        :return:
        """
        if which_kind_of_doccano == "ima_precision" :
            dict_doccano = toDoccanoImaPrecision(Document, type=type, attribute=attribute)

        elif which_kind_of_doccano == "ima_rappel":
            dict_doccano = toDoccanoImaRappel(Document, dict_regex_type=dict_regex_type, value=value, span=span)

        elif which_kind_of_doccano == "ima_pb":
            dict_doccano = toDoccanoPb(Document, path_to_doc=path_to_pb_doc, regexp = regex)

        else :
            print("Please enter the doccano eval you which to do.")

        DoccanoDocument = docForDoccano(dict_doccano)

        return DoccanoDocument


    def toDoccanoImaPrecision(Document, type, attribute=None):
        """

        :param type:
        :param attribute:
        :return:
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
        """

        :param dict_regexp_type:
        :param value:
        :return:
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

        doccano_dict_pb = {}
        path_to_doc = os.path.abspath(path_to_doc)
        raw_text = Annotation.to_dict(Document.get_annotations(_type="raw_text")[0])['value']
        text = "Valeur extraite : " + regexp + "\n" + "Texte du compte-rendu annoté probleme :\n" + raw_text

        doccano_dict_pb[text] = [path_to_doc, regexp]

        return doccano_dict_pb


    def toDoccanoDrWH(Document, type, segment):

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
        """
        Creats a DoccanoDoc object with dict in input
        :return: Doccano Object
        """
        thisDoccanoDoc = DoccanoDocument
        thisDoccanoDoc.annotationsDoccano = []
        for text in dict_doccano:
            labels = [dict_doccano[text]]
            meta = {"pymedext_name": dict_doccano[text][0]}
            thisDoccanoDoc.annotationsDoccano.append(DoccanoAnnotation(text=text,
                                                                       labels=labels,
                                                                       meta=meta))
        return thisDoccanoDoc


    def DoccanoEvalRappel(DoccanoDocument, dict_doccano, path_to_doc):
        """
        Creats a DoccanoDoc object with dict in input
        :return: Doccano Object
        """

        path_to_doc = os.path.abspath(path_to_doc)

        for text in dict_doccano:
            labels = dict_doccano[text]
            meta = {"pymedext_name": path_to_doc}
            DoccanoDocument.append(DoccanoAnnotation(text=text,
                                                     labels=labels,
                                                     meta=meta
                                                             ))
        return DoccanoDocument

    def DoccanoEvalN(DoccanoDocument, dict_doccano, number_annoted, number_eval, path_to_doc):
        """
        Adds doccano annotations to DoccaDocument until a specified number of evaluations.
        :param dict_doccano:A doccano dict that will be filled until it reachs the desired number of annotations.
        {"text": "Great price.", "labels": ["positive"], "meta": {"wikiPageID": 3}}
        :param number_annoted: the number of evaluations desired.
        :param number_eval: the current number of annotation.
        :return:
        """

        for text in dict_doccano:
            if number_annoted < number_eval:
                number_annoted += 1
                path_to_doc = os.path.abspath(path_to_doc)
                # print("inside DoccanoEvalN", number_annoted)
                DoccanoDocument.append(DoccanoAnnotation(text=text,
                                                                 labels=["x" + dict_doccano[text]],
                                                                 meta={"pymedext_name": path_to_doc}))
        return [DoccanoDocument, number_annoted]

    def DoccanoEvalClass(DoccanoDocument, dict_doccano, dictClasses, number_eval):
        """
        Adds doccano annotations to DoccanoDocument object until a specified number of evaluations for both classes.
        :param dict_doccano: A doccano dict that will be filled until the two classes reach the desired number of annotations
        :param dictClasses: A dict of doccano classes (ex : negatif vs non negatif) with their current occurences.
        :param number_eval: the number of evaluations desired
        :return: A list with the modified Doccano Object, and a dict of annotations classes, with their number
        """

        for text in dict_doccano:

            if dict_doccano[text] not in dictClasses:  # on ne sait pas quelles sont les étiquettes
                dictClasses[dict_doccano[text]] = 1
                DoccanoDocument.annotationsDoccano.append(DoccanoAnnotation(text=text,
                                                                 labels=[dict_doccano[text]]))
            elif dictClasses[
                dict_doccano[text]] < number_eval:  # si l'étiquette n'a pas le nombre désiré d'évaluation, on l'ajoute
                dictClasses[dict_doccano[text]] += 1
                DoccanoDocument.annotationsDoccano.append(DoccanoAnnotation(text=text,
                                                                 labels=[dict_doccano[text]]))

        return [DoccanoDocument, dictClasses]
