#!/usr/bin/env python3

from pymedext_core import pymedext
from intervaltree import Interval,IntervalTree
import argparse
import json
from datetime import datetime
import psycopg2
import psycopg2.extras
from typing import Iterator, Dict, Any, Optional
import io
from os import listdir
from os.path import isfile, join
import pandas
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s -- %(name)s - %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


parser = argparse.ArgumentParser()
parser.add_argument("-i","--inputFolder", help="input annotationsFiles")

args = parser.parse_args()
DB_host =  "stagingdatabase"
DB_name = "omopdb"
DB_port = 5432
#DB_user = "omopuser"
#DB_password ="omopdb"
DB_user = "postgres"
DB_password ="postgres"


logger.info("start connection")
omop_con = pymedext.OmopSource(DB_host, DB_name, DB_port, DB_user, DB_password)

nlp_workflow="nlp_workflow_V1"
filterType = ["sentence"]
mypath = args.inputFolder
if not mypath.endswith("/"):
    mypath = mypath+"/"
logger.info("###2")
allFiles = [mypath+f for f in listdir(mypath) if isfile(join(mypath, f))]
demoDoc=pymedext.Document(raw_text="load",ID="patientID", pathToconfig= allFiles)
demoDoc, __tree, __sentencepos, thisRoot =pymedext.normalize.uri(demoDoc)
info_pat = [1234,1234,1,str(datetime.now().strftime("%Y-%m-%d"))]
logger.info(info_pat)
dict_note={
    "person_id":int(info_pat[0]), # NIP
    "note_text":demoDoc.annotations[0].value,
    "visit_occurrence_id":info_pat[1], # NDA
    "note_id":int(info_pat[2])#"ni_doc"
    }
note_id =int(info_pat[2])#
thisTime = datetime.strptime(info_pat[-1], '%Y-%m-%d')
note_nlp_id = 1#"nlp_id"
logger.info("############")
annotations, dict_table_note, dict_table_person = pymedext.omop.buildNoteNlP(thisRoot, dict_note, note_id,note_nlp_id, nlp_workflow,thisTime,  filterType,False)
logger.info(annotations)
logger.info(dict_table_note)
logger.info(dict_table_person)

if annotations:
    omop_con.saveToSource(dict_table_person, dict_table_note, annotations)
