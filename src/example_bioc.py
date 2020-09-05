#!/usr/bin/env python3

from pymedextcore import pymedext
# def loadbiocJson():
pathTofile_json="../data/biocformat.json"
pathTofile_xml="../data/7382743.xml"

pymedext_xml = pymedext.BioC.load_collection(pathTofile_xml)
pymedext_json = pymedext.BioC.load_collection(pathTofile_json,1)


pathTojson= "faux_CRdrwh_extdata.json"

grou = pymedext.Document("load",ID="grou",pathToconfig=[pathTojson])

pymedext.brat.save(grou,"grou.ann",["raw_text","drwh_cleantext"])
