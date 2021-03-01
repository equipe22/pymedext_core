#!/usr/bin/env python3

from .document import Document
from intervaltree import Interval,IntervalTree
# from .annotationGraph import AnnotationGraph
import logging
logger = logging.getLogger(__name__)


class normalize:

    def __setSentencesAndRawText(Document,rootNode):
        """Build an intervalTree of Annotations from a Document

        :param Document: a Document
        :param rootNode: type to filter Document
        :returns: tree,sentencepose,raw_textpos,annotGraph
        :rtype: intervalTree,dict,dict,dict

        """
        __raw_textpos=dict()
        __sentencepos=dict()
        __tree=IntervalTree()
        annotsGraph=dict()
        for thisAnnotation in Document.annotations:
            thisSpan =str(thisAnnotation.span[0])+"_"+str(thisAnnotation.span[1])
            if thisAnnotation.type =="raw_text" and "id" not in __raw_textpos.keys():
                __raw_textpos={"source_ID":thisAnnotation.source_ID,"id":thisAnnotation.ID,"type":thisAnnotation.type}
                logger.debug(__raw_textpos)
            if thisAnnotation.type == rootNode:
                if thisSpan not in __sentencepos.keys():
                    thisAnnotation.source_ID=__raw_textpos["id"]
                    __tree[thisAnnotation.span[0]:thisAnnotation.span[1]]={
                        "annotation":[{"type":thisAnnotation.type,"value":thisAnnotation}]}
                    __sentencepos[thisSpan]=thisAnnotation.ID
                    annotsGraph[thisSpan]=[thisAnnotation]
        return(__tree,__sentencepos,__raw_textpos,annotsGraph)
    #filtrer les fonctions en fonction du syntagmes
    #
    def __buildTree(Document,__tree, __sentencepos, __raw_textpos, annotsGraph, otherSegments, rootNode):
        """Build tree from Document

        :param Document:
        :param __tree:
        :param __sentencepos:
        :param __raw_textpos:
        :param annotsGraph:
        :param otherSegments:
        :param rootNode:
        :returns:
        :rtype:

        """
        for thisAnnotation in Document.annotations:
            start = thisAnnotation.span[0]
            end   = thisAnnotation.span[1]
            thisSpan=str(start)+"_"+str(end)
            if thisAnnotation.type in otherSegments:
               thisAnnotation.source_ID=__sentencepos[thisSpan]
               findSentence=__tree[start+1:end-1]
               __tree[start:end]={"annotation":[{"type":thisAnnotation.type,"value":thisAnnotation}]}
            if thisAnnotation.type not in otherSegments and thisAnnotation.type not in [rootNode,"raw_text"] :
                 thisAnnotation.source_ID=__raw_textpos["id"]
                 __tree[start:end]={"annotation":[{"type":thisAnnotation.type,"value":thisAnnotation}]}
        return(Document, __tree, __sentencepos)

    #filterEntities stay until i resolve the entity declaration issue
    def __buildGraph(Document, __tree, __sentencepos, thisGraph,filterEntities):
        """Build Graph from intervaltree and Doc

        :param Document:
        :param __tree:
        :param __sentencepos:
        :param thisGraph:
        :param filterEntities:
        :returns:
        :rtype:

        """
        lenentities=[]
        grousentences=[]
        typeliste=[]
        if len(__sentencepos.keys()) >0:
            for thisAnnotation in __sentencepos.keys():
                thisSpan = thisAnnotation.split("_")
                start = int(thisSpan[0])
                end   = int(thisSpan[1])
                thisMatch=__tree.overlap(start,end)
                entities=[]
                for interval in thisMatch:
                    for annot in interval.data["annotation"]:
                        # print(annot["value"].to_dict())
                        annot["value"].set_root(Document.annotations[0])
                        if annot["value"].span[0] == start and annot["value"].span[1] == end:
                            # print("add properties")
                            thisGraph[thisAnnotation][0].add_property(annot["value"])
                        elif annot["value"].isEntity == True and annot["value"].span[0] > start and  annot["value"].span[1] < end:
                            thisGraph[thisAnnotation][0].add_child(annot["value"])
                # lenentities.append(len(entities))
                Document.annotations[0].add_child(thisGraph[thisAnnotation][0])
        else:
            for interval in __tree:
                for annot in interval.data["annotation"]:
                    # print(annot["value"].to_dict())
                    annot.set_root(Document.annotations[0])
                    Document.annotations[0].add_child(annot)
        return(Document)

    @staticmethod
    def uri(Document,otherSegments=["drwh_family","hypothesis"],rootNode="drwh_sentences", filterEntities=['drugs_fast', 'cui']):
        """uri Normalization

        :param Document:
        :param otherSegments:
        :param "hypothesis"]:
        :param rootNode:
        :param filterEntities:
        :param 'cui']:
        :returns:
        :rtype:

        """
        # __raw_textpos=dict()
        # normalize.__sentencepos=dict()
        # normalize.__tree=IntervalTree()
        __tree, __sentencepos, __raw_textpos, thisGraph=normalize.__setSentencesAndRawText(Document,rootNode)
        Document, __tree, __sentencepos = normalize.__buildTree(Document,__tree, __sentencepos, __raw_textpos,thisGraph, otherSegments, rootNode)
        Document = normalize.__buildGraph(Document, __tree, __sentencepos, thisGraph,filterEntities)
        return(Document,__tree, __sentencepos)
