#!/usr/bin/env python3

"""
Each class which transform pymedext Document to another format
must herit from the DataTransform

TODO: put some function such as save and load as mandatory to
ease the use of DataTransform object

"""
class DataTransform:
    # def __new__(self,Document):
    #     self.Document=Document
    #
    #
    @staticmethod
    def save():
        """Generic method to transform a PyMedExt Document save as another format

        :returns: not a PyMedExt doc
        """
        pass

    #Document load from and return a Document
    @staticmethod
    def load():
        """Generic method to save another format into a PyMedExt Document

        :returns: PyMedext Document
        """
        pass
