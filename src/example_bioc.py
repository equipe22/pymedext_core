#!/usr/bin/env python3

from pymedext_core import pymedext
# def loadbiocJson():
pathTofile_json="../data/biocformat.json"
pathTofile_xml="../data/7382743.xml"

pymedext_xml = pymedext.BioC.load_collection(pathTofile_xml)
pymedext_json = pymedext.BioC.load_collection(pathTofile_json,1)
