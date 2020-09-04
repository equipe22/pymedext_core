# -*- coding: utf-8 -*-

"""
Created 2020/04/14

@author: David BAUDOIN

fonction : creation ou update  d'un fichier BRAT a partir d'un dic pymedext

"""
from .datatransform import DataTransform
import logging
logger = logging.getLogger(__name__)
import uuid
from .brat_parser import read_file_annotations
from .annotators import Annotation
from .document import Document


class brat(DataTransform):
    def savetobrat(dic_pymedext, bratFilePath_ann, exclusion=["raw_text"]):
        f_brat = open(bratFilePath_ann, 'w')
        instance_brat = 0
        for annotation in dic_pymedext.annotations:
            if annotation.type not in exclusion:
                bratline = 'T' + str(instance_brat) + '	' + annotation.type + ' ' + str(annotation.span[0]) \
                           + ' ' + str(annotation.span[1]) + '	' + str(annotation.value)
                instance_brat += 1
                f_brat.write(bratline)
                f_brat.write('\n')
        f_brat.close()

    def load_from_brat(ann_file):

        entities, relations, attributes=read_file_annotations(ann_file)
        annotations_list=[]
        raw_text = open(ann_file.replace(".ann",".txt"), 'r').read()
        raw_text_ID=str(uuid.uuid1())
        for entity in entities:
            for span in entity.span:
                thisID = str(uuid.uuid1())
                annotations_list.append(
                            Annotation(type=entity.type,
                                      value=entity.text,
                                      ngram = entity.text,
                                      source_ID=raw_text_ID,
                                      ID=thisID,
                                      source="BratFile",
                                      span=(span[0],span[1])
                            )
                    )

        thisDocument = Document(raw_text =raw_text,ID =raw_text_ID, source = ann_file)
        thisDocument.annotations.extend(annotations_list)
        return(thisDocument)




    # def update(dic_pymedext, bratFilePath_ann):
    #     f_brat = open(bratFilePath_ann, 'r')
    #     lastline = ''
    #     for line in f_brat:
    #         lastline = line
    #     f_brat.close()
    #     try:
    #         instance_brat = int(lastline.split('   ')[0][1:])
    #         f_brat = open(bratFilePath_ann, 'a')
    #         for element in dic_pymedext['annotations']:
    #             bratline = 'T' + str(instance_brat) + '	' + dic_pymedext['annotations']['type'] + ' ' + str(dic_pymedext['annotations']['span'][0]) \
    #                        + ' ' + str(dic_pymedext['annotations']['span'][0]) + '	' + str(dic_pymedext['annotations']['value'])
    #             instance_brat += 1
    #             f_brat.write(bratline)
    #             f_brat.write('\n')
    #         f_brat.close()
    #     except:
    #         logger.info('cannot turn into int the value : ' + str(lastline.split('   ')[0]))
