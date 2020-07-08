#!/usr/bin/env python3

from .document import Document
from intervaltree import Interval,IntervalTree
from .annotationGraph import AnnotationGraph
import logging
logger = logging.getLogger(__name__)


class normalize:

    def __setSentencesAndRawText(Document,rootNode):
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
                    thisNode = AnnotationGraph(thisAnnotation.value,
                                               thisAnnotation.type,
                                               thisAnnotation.span,
                                               thisAnnotation.attributes,
                                               thisAnnotation.isEntity)
                    annotsGraph[thisSpan]=[thisNode]
        return(__tree,__sentencepos,__raw_textpos,annotsGraph)
    #filtrer les fonctions en fonction du syntagmes
    #
    def __buildTree(Document,__tree, __sentencepos, __raw_textpos, annotsGraph, otherSegments, rootNode):
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
        lenentities=[]
        grousentences=[]
        typeliste=[]
        thisRoot = AnnotationGraph(Document.annotations[0].value,
                                           Document.annotations[0].type,
                                           Document.annotations[0].span,
                                           Document.annotations[0].attributes,
                                           Document.annotations[0].isEntity)
        if len(__sentencepos.keys()) >0:
            for thisAnnotation in __sentencepos.keys():
                thisSpan = thisAnnotation.split("_")
                start = int(thisSpan[0])
                end   = int(thisSpan[1])
                thisMatch=__tree.overlap(start,end)
                entities=[]
                # #TEST
                # if len(thisGraph[thisAnnotation]) ==1:
                #     grousentences.append(True)
                #     thisGraph[thisAnnotation][0].setRoot(thisRoot)
                # else:
                #     grousentences.append(False)
                for interval in thisMatch:
                    for annot in interval.data["annotation"]:
                        # print(annot["value"].to_dict())
                        thisNode = AnnotationGraph(annot["value"].value,
                                                   annot["value"].type,
                                                   annot["value"].span,
                                                   annot["value"].attributes,
                                                   annot["value"].isEntity)
                        thisNode.setRoot(thisRoot)
                        # if thisNode.type in ['drugs_fast', 'cui']:
                        #     print(thisNode.isEntity)
                        #     thisNode.isEntity=True
                        # # typeliste.append(annot["value"].type)
                        if annot["value"].span[0] == start and annot["value"].span[1] == end:
                            # print("add properties")
                            thisGraph[thisAnnotation][0].addProperty(thisNode)
                        elif thisNode.isEntity == True and annot["value"].span[0] > start and  annot["value"].span[1] < end:
                            thisGraph[thisAnnotation][0].addChild(thisNode)
                # print(len(entities))
                # lenentities.append(len(entities))
                thisRoot.addChild(thisGraph[thisAnnotation][0])
        else:
            for interval in __tree:
                for annot in interval.data["annotation"]:
                    # print(annot["value"].to_dict())
                    thisNode = AnnotationGraph(annot["value"].value,
                                               annot["value"].type,
                                               annot["value"].span,
                                               annot["value"].attributes,
                                               annot["value"].isEntity)
                    thisNode.setRoot(thisRoot)
                    thisRoot.addChild(thisNode)
        return(thisRoot)

    @staticmethod
    def uri(Document,otherSegments=["drwh_family","hypothesis"],rootNode="drwh_sentences", filterEntities=['drugs_fast', 'cui']):
        # __raw_textpos=dict()
        # normalize.__sentencepos=dict()
        # normalize.__tree=IntervalTree()
        __tree, __sentencepos, __raw_textpos, thisGraph=normalize.__setSentencesAndRawText(Document,rootNode)
        Document, __tree, __sentencepos = normalize.__buildTree(Document,__tree, __sentencepos, __raw_textpos,thisGraph, otherSegments, rootNode)
        thisRoot = normalize.__buildGraph(Document, __tree, __sentencepos, thisGraph,filterEntities)
        return(Document,__tree, __sentencepos, thisRoot)
