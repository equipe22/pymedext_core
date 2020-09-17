import uuid
import json
import os
from .doccanoannotator import DoccanoAnnotation


class DoccanoDocument:
    """
    DoccanoDocument is used to build an evaluation document, that will be sent to Doccano interface.
    DoccanoDocument contains a set of specific DoccanoAnnotation objects that a user want to evaluate.
    """


    def __init__(self):
        """Initialize a DoccanoDocument object.
        :return: DoccanoDocument
        :rtype: DoccanoDocument
        """
        self.doccanoAnnotation = []

    def toJsonDoccano(self):
        """Tranform a DoccanoDocument object to a json.
        :return: a json
        :rtype: json
        """
        return json.dump(self.toDictDoccano())

    def toDictDoccano(self):
        """Transform a DoccanoDocument object to a list of doccanoAnnotation dict

        :return: a list of doccanoAnnotation dict
        :rtype: dict
        """
        return [x.to_dict() for x in self.doccanoAnnotation]

    def writeJsonDoccano(self, pathToOutput):
        """write a json file in pathToOuput path with a DoccanoDument object

        :param pathToOutput: output path of the file
        :return: a doccano file
        """
        with open(pathToOutput, 'w', encoding='utf-8') as f:
            for el in self.toDictDoccano():
                json.dump(el, f, ensure_ascii=False, indent=None)
                f.write("\n")



