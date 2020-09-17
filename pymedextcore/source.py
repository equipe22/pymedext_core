#!/usr/bin/env python3
#

class Source:
    """Abstract Class to extend to implement a specific source connector.
    see Omop Source example
    """
    # def __new__(self,Document):
    #     self.Document=Document
    #
    # Document save as
    @staticmethod
    def saveToSource():
        """Generic method to save data to a specific source
        :returns:
        :rtype:

        """
        pass

    #Document load from and return a Document
    @staticmethod
    def loadFromSource():
        """Generic method to download Data from a source
        :returns:
        :rtype:

        """
        pass


