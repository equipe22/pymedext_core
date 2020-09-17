#!/usr/bin/env python3

import base64
import xml.etree.ElementTree as ET
from .datatransform import DataTransform
from .document import Document
from .annotators import Annotation
import uuid
import logging
logger = logging.getLogger(__name__)

class FHIR(DataTransform):
    def __parse_xml__(root,getResources= ["{http://hl7.org/fhir}DocumentReference","{http://hl7.org/fhir}Binary" ]):
        fhir_list=[]
        for entry in root:
            for resources in entry:
                for resource in resources:
                    if (resource.tag) in getResources:
                        logger.debug(resource.tag, resource.attrib, resource.text)
                        logger.debug("###########")
                        resourceDict=dict()
                        for attributes in resource:
                            # logger.debug("##",attributes.attrib)
                            # logger.debug("##tag",attributes.tag)
                            # logger.debug(attributes.tag, attributes.attrib, attributes.text)
                            attrDict=dict()
                            for attribute in attributes:
                                if attribute.attrib:
                                    # logger.debug(attribute.attrib["value"])
                                    attrDict[attribute.tag.replace("{http://hl7.org/fhir}", "")]=attribute.attrib
                                else:
                                    attrDict[attribute.tag.replace("{http://hl7.org/fhir}", "")]={"value":""}
                                if attribute.text:
                                    attrDict[attribute.tag.replace("{http://hl7.org/fhir}", "")].update({"text":attribute.text} )
                                else:
                                    attrDict[attribute.tag.replace("{http://hl7.org/fhir}", "")].update({"text":""} )
                                # logger.debug("####TAG",attribute.tag.replace("{http://hl7.org/fhir}", ""))
                                # logger.debug("####A", attribute.attrib)
                                # logger.debug("####Y", attribute.text)
                                if len(attribute)!= 0:
                                    # logger.debug("baby")
                                    elementDict=dict()
                                    for element in attribute:
                                        if element.attrib:
                                            # logger.debug(element.attrib["value"])
                                            elementDict[element.tag.replace("{http://hl7.org/fhir}", "")]=element.attrib
                                        else:
                                            elementDict[element.tag.replace("{http://hl7.org/fhir}", "")]={"value":""}
                                        if element.text:
                                            elementDict[element.tag.replace("{http://hl7.org/fhir}", "")].update({"text": element.text})
                                        else:
                                            elementDict[element.tag.replace("{http://hl7.org/fhir}", "")].update({"text": "" })
                                        attrDict[attribute.tag.replace("{http://hl7.org/fhir}", "")].update({"element":elementDict} )
                            resourceKey=attributes.tag.replace("{http://hl7.org/fhir}", "")
                            if attributes.attrib:
                                # logger.debug(attributes.attrib["value"])
                                resourceDict[resourceKey]=attributes.attrib
                            else:
                                resourceDict[resourceKey]={"value":""}
                            if attributes.text:
                                resourceDict[resourceKey].update({"text":attributes.text} )
                            else:
                                resourceDict[resourceKey].update({"text":""} )
                            resourceDict[resourceKey].update({"attributes":attrDict} )
                        fhir_list.append({resource.tag.replace("{http://hl7.org/fhir}", ""):resourceDict })
        return(fhir_list)

    def __orderDocument__(fhir_list):
        fhir_dict= dict()
        for data in fhir_list:
            if "Binary" in data.keys():
                logger.debug(data["Binary"]["contentType"])
                tmpKey= data["Binary"]["id"]["value"]
                if data["Binary"]["contentType"]["value"] in ["text/plain"] : #'image/jpeg'; 'application/pdf';'application/dicom'
                    if tmpKey in fhir_dict.keys():
                        fhir_dict[tmpKey].update({"raw_text": base64.b64decode(data["Binary"]["content"]["value"]).decode("utf-8")})
                    else:
                        fhir_dict[tmpKey]={"raw_text": base64.b64decode(data["Binary"]["content"]["value"]).decode("utf-8")}
            if "DocumentReference" in data.keys():
                subject= data["DocumentReference"]["subject"]["attributes"]["reference"]["value"]
                thisDate= data["DocumentReference"]["created"]["value"]
                tmpKey= data["DocumentReference"]["content"]["attributes"]["attachment"]["element"]["url"]["value"].replace("/Binary/","")
                if tmpKey in fhir_dict.keys():
                    fhir_dict[tmpKey].update({"subject":subject, "date":thisDate})
                else:
                    fhir_dict[tmpKey]={"subject":subject, "date":thisDate}
        return(fhir_dict)

    def load_xml(fhir_input):
        tree = ET.parse(fhir_input)
        root = tree.getroot()
        fhir_dict=FHIR.__orderDocument__(FHIR.__parse_xml__(root))
        documents_collection=[]
        for key in fhir_dict.keys():
            raw_text_ID=str(uuid.uuid1())
            thisDocument= Document(raw_text =fhir_dict[key]["raw_text"],ID =raw_text_ID, source = "FHIR/"+fhir_dict[key]["subject"]+"/"+key, documentDate =fhir_dict[key]["date"])
            documents_collection.append(thisDocument)
        return(documents_collection)
