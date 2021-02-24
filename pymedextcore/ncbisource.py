#!/usr/bin/env python3

from .source import Source
from .connector import *
from .bioctransform import BioC
import json
import sys
import logging
logger = logging.getLogger(__name__)


class PubTatorSource(Source, SimpleAPIConnector):
    """
    Connection to a POstgres Ommop source
    """
    def __init__(self, host="https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/" ):
        """Initialize a connection to a SimpleAPiCOnnector for PubTator

        :param DB_host:
        :returns:
        :rtype:

        """
        super().__init__( host)
        logger.info("Initialize APi connection")

    def getPubTatorAnnotations(self, pmid_list, Bioconcept="",returnFormat=0):
        # load pmids
        json_pmid = {"pmids": [pmid.strip() for pmid in pmid_list]}

        # load bioconcepts
        # 	[Bioconcept]: Default (leave it blank) includes all bioconcepts. Otherwise, user can choose
        # 	gene, disease, chemical, species, proteinmutation, dnamutation, snp, and cellline.
        if Bioconcept != "":
            json_pmid["concepts"]=Bioconcept.split(",")

        # request
        r = self.session.post(self.host+"biocxml", json = json_pmid)
        if r.status_code != 200 :
            return ("[Error]: HTTP code "+ str(r.status_code))
        else:
            if returnFormat==0: # return a document
                return(BioC.load_collection(r.text,is_file=False ))
            else:
                return(r.text)
