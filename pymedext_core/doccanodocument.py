import uuid
import json
import os
from .doccanoannotator import AnnotationDoccano


class DoccanoDocument:
    def __init__(self):
        self.annotationsDoccano = []

    def toJsonDoccano(self):
        return json.dump(self.toDictDoccano())

    def toDictDoccano(self):
        return [x.to_dict() for x in self.annotationsDoccano]

    def writeJsonDoccano(self, pathToOutput):
        with open(pathToOutput, 'w', encoding='utf-8') as f:
            for el in self.toDictDoccano():
                json.dump(el, f, ensure_ascii=False, indent=None)
                f.write("\n")



