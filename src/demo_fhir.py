#!/usr/bin/env python3
import base64
import xml.etree.ElementTree as ET
# tree = ET.parse('patient-2169591.fhir-bundle.xml')
tree = ET.parse('patient-99912345.fhir-bundle.xml')
root = tree.getroot()

for entry in root:
    # print(entry.tag, entry.attrib)
    for resources in entry:
        # print(resources.tag, resources.attrib)
        for resource in resources:
            # print(resource.tag, resource.attrib, resource.text)
            # print(len(resource))
            for element in resource:
                print(element)
                print(element.tag, element.attrib, element.text)

                if len(element)!= 0:
                    for child in element:
                        print(child.tag, child.attrib, child.text)



demo_Data=[]

for entry in root:
    # print(entry.tag, entry.attrib)
    for resources in entry:
        # print(resources.tag, resources.attrib)
        for resource in resources:
            if (resource.tag) in ["{http://hl7.org/fhir}DocumentReference","{http://hl7.org/fhir}Binary" ]:
                print(resource.tag, resource.attrib, resource.text)
                # if resource.tag=="DocumentReference-2-note":
                print("###########")
                resourceDict=dict()
                for attributes in resource:
                    # print("##",attributes.attrib)
                    # print("##tag",attributes.tag)
                    # print(attributes.tag, attributes.attrib, attributes.text)
                    # if len(attributes)!= 0:
                    attrDict=dict()
                    for attribute in attributes:
                        if attribute.attrib:
                            # print(attribute.attrib["value"])
                            attrDict[attribute.tag.replace("{http://hl7.org/fhir}", "")]=attribute.attrib
                        else:
                            attrDict[attribute.tag.replace("{http://hl7.org/fhir}", "")]={"value":""}
                        if attribute.text:
                            attrDict[attribute.tag.replace("{http://hl7.org/fhir}", "")].update({"text":attribute.text} )
                        else:
                            attrDict[attribute.tag.replace("{http://hl7.org/fhir}", "")].update({"text":""} )
                        # print("####TAG",attribute.tag.replace("{http://hl7.org/fhir}", ""))
                        # print("####A", attribute.attrib)
                        # print("####Y", attribute.text)
                        if len(attribute)!= 0:
                            # print("baby")
                            elementDict=dict()
                            for element in attribute:
                                if element.attrib:
                                    # print(element.attrib["value"])
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
                        # print(attributes.attrib["value"])
                        resourceDict[resourceKey]=attributes.attrib
                    else:
                        resourceDict[resourceKey]={"value":""}
                    if attributes.text:
                        resourceDict[resourceKey].update({"text":attributes.text} )
                    else:
                        resourceDict[resourceKey].update({"text":""} )
                    resourceDict[resourceKey].update({"attributes":attrDict} )
                demo_Data.append({resource.tag.replace("{http://hl7.org/fhir}", ""):resourceDict })


parseBinary= dict()
for data in demo_Data:
    if "Binary" in data.keys():
        print(data["Binary"]["contentType"])
        tmpKey= data["Binary"]["id"]["value"]
        if data["Binary"]["contentType"]["value"] in ["text/plain"] :
            if tmpKey in parseBinary.keys():
                parseBinary[tmpKey].update({"raw_text": base64.b64decode(data["Binary"]["content"]["value"]).decode("utf-8")})
            else:
                parseBinary[tmpKey]={"raw_text": base64.b64decode(data["Binary"]["content"]["value"]).decode("utf-8")}
    if "DocumentReference"  in data.keys():
        # pprint(data)
        subject= data["DocumentReference"]["subject"]["attributes"]["reference"]["value"]
        thisDate= data["DocumentReference"]["created"]["value"]
        tmpKey= data["DocumentReference"]["content"]["attributes"]["attachment"]["element"]["url"]["value"].replace("/Binary/","")
        if tmpKey in parseBinary.keys():
            parseBinary[tmpKey].update({"subject":subject, "date":thisDate})
        else:
            parseBinary[tmpKey]={"subject":subject, "date":thisDate}
