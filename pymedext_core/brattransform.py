# -*- coding: utf-8 -*-

"""
Created 2020/04/14

@author: David BAUDOIN

fonction : creation ou update  d'un fichier BRAT a partir d'un dic pymedext

"""
from .datatransform import DataTransform
import logging
logger = logging.getLogger(__name__)

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
