#!/usr/bin/env python3
import pandas
class DataTransform:
    # def __new__(self,Document):
    #     self.Document=Document
    #
    # Document save as
    @staticmethod
    def save():
        pass

    #Document load from and return a Document
    @staticmethod
    def load():
        pass


class omop(DataTransform):

    def load(Document, server):
        print(Document.annotations[0])
        print("load from "+server)

    # def generateNoteNLPEntity(dict_omop, to_omop_nlp, to_date,
    #                           note_nlp_id = "nlp_id", note_id = "note_id",
    #                           section_concept_id="section_concept_id",
    #                           note_nlp_concept_id="note_nlp_concept_id",
    #                           note_nlp_source_concept_id="note_nlp_source_concept_id",
    #                           nlp_workflow="nlp_workflow",
    #                           term_exist="T", entity="entity"):
      #                    note_nlp_id = "nlp_id", note_id = "note_id",
        #                       section_concept_id="section_concept_id",
        #                       note_nlp_concept_id="note_nlp_concept_id",
        #                       note_nlp_source_concept_id="note_nlp_source_concept_id",
        #                       nlp_workflow="nlp_workflow",
        #                       term_exist="T", entity="entity"):
        # note_nlp_id = "nlp_id"
        # note_id = "note_id"
        # section_concept_id="section_concept_id"
        # note_nlp_concept_id="note_nlp_concept_id"
        # note_nlp_source_concept_id="note_nlp_source_concept_id"
        # nlp_workflow="nlp_workflow"
        # term_exist="T"
        # entity="entity"

    def generateNoteNLP(dict_omop, to_omop_nlp, to_date,
                              note_nlp_id, note_id,
                              section_concept_id,
                              note_nlp_concept_id,
                              note_nlp_source_concept_id,
                              nlp_workflow,
                              term_exist, entity):

        # print(note_nlp_id)
        if len(dict_omop.keys()) ==0:
            dict_omop={
                "note_nlp_id":[note_nlp_id], #different for each note
                "note_id": [note_id], #get from note
                "section_concept_id": [section_concept_id], ##a voir avec les informations de la table concepte par example le terme normalisé par le cui ou autres
                "snippet":[to_omop_nlp["drwh_sentences"]],
                "offset": [to_omop_nlp["value"]], #the normalized term extract
                "lexical_variant":[to_omop_nlp["ngram"]], # raw ngram of the extracted texts
                "note_nlp_concept_id": [note_nlp_concept_id], #voir table concept
                "note_nlp_source_concept_id": [note_nlp_source_concept_id], #table vocabularies
                "nlp_system": [to_omop_nlp["type"]], #annotations_type from pymedext
                "nlp_workflow": [nlp_workflow],  #the workflow id which generate the annotations
                "nlp_date":[to_date.strftime('%Y-%m-%d')], # date of process
                "nlp_datetime": [to_date.strftime('%Y-%m-%d %H:%M:%S')], #date of process and time
                "term_exists":[term_exist], #not set
                "term_modifiers": [",".join([x.replace("drwh_","")+"="+to_omop_nlp[x] for x in ["drwh_negation","drwh_family", "hypothesis"]])], #lexical variants + all terms negation=no,experiencer=patient,hypothesis=false +
                "term_temporal": [to_omop_nlp["temporality"]], #normalized date extract from heideltime
                "term_negation": [to_omop_nlp["drwh_negation"]], # just negation state
                "term_experiencer":[to_omop_nlp["drwh_family"]], #experiencer state
                "term_hypothesis":[to_omop_nlp["hypothesis"]], # hypo state
                "term_type":[entity],
                "offset_start":[int(to_omop_nlp["span"][0])],
                "offset_end":[int(to_omop_nlp["span"][1])]
                }
        else:
            dict_omop["note_nlp_id"].append(
                note_nlp_id) #different for each note
            dict_omop["note_id"].append(
                note_id) #get from note
            dict_omop["section_concept_id"].append(
                section_concept_id) ##a voir avec les informations de la table concepte par example le terme normalisé par le cui ou autres
            dict_omop["snippet"].append(
                to_omop_nlp["drwh_sentences"])
            dict_omop["offset"].append(
                to_omop_nlp["value"]) #the normalized term extract
            dict_omop["lexical_variant"].append(
                to_omop_nlp["ngram"]) # raw ngram of the extracted texts
            dict_omop["note_nlp_concept_id"].append(
                note_nlp_concept_id) #voir table concept
            dict_omop["note_nlp_source_concept_id"].append(
                note_nlp_source_concept_id) #table vocabularies
            dict_omop["nlp_system"].append(
                to_omop_nlp["type"]) #annotations_type from pymedext
            dict_omop["nlp_workflow"].append(
                nlp_workflow)  #the workflow id which generate the annotations
            dict_omop["nlp_date"].append(
                to_date.strftime('%Y-%m-%d')) # date of process
            dict_omop["nlp_datetime"].append(
                to_date.strftime('%Y-%m-%d %H:%M:%S')) #date of process and time
            dict_omop["term_exists"].append(
                term_exist) #not set
            dict_omop["term_modifiers"].append(
                ",".join([x.replace("drwh_","")+"="+to_omop_nlp[x] for x in ["drwh_negation","drwh_family", "hypothesis"]])) #lexical variants + all terms negation=no,experiencer=patient,hypothesis=false +
            dict_omop["term_temporal"].append(
                to_omop_nlp["temporality"]) #normalized date extract from heideltime
            dict_omop["term_negation"].append(
                to_omop_nlp["drwh_negation"]) # just negation state
            dict_omop["term_experiencer"].append(
                to_omop_nlp["drwh_family"]) #experiencer state
            dict_omop["term_hypothesis"].append(
                to_omop_nlp["hypothesis"]) # hypo state
            dict_omop["term_type"].append(
                entity)
            dict_omop["offset_start"].append(
                int(to_omop_nlp["span"][0]))
            dict_omop["offset_end"].append(
                int(to_omop_nlp["span"][1]))
        return(dict_omop)


    def generateNote(dict_note, to_omop_note, to_date,
                     note_event_id,
                     note_event_field_concept_id,
                     note_type_concept_id,
                     note_class_concept_id,
                     note_title,
                     encoding_concept_id,
                     language_concept_id,
                     provider_id,
                     visit_detail_id,
                     note_source_value):

        if len(dict_note.keys()) ==0:
            dict_note = {
                "note_id":[to_omop_note["note_id"]],#	A unique identifier for each note.
                "person_id": [to_omop_note["person_id"]],#[]	A foreign key identifier to the Person about whom the Note was recorded. The demographic details of that Person are stored in the PERSON table.
                "note_event_id":[note_event_id],#A foreign key identifier to the event (e.g. Measurement, Procedure, Visit, Drug Exposure, etc) record during which the note was recorded.
                "note_event_field_concept_id":[note_event_field_concept_id], #A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the field to which the note_event_id is referring.
                "note_date":[to_date.strftime('%Y-%m-%d')], #The date the note was recorded.
                "note_datetime":[to_date.strftime('%Y-%m-%d %H:%M:%S')], #The date and time the note was recorded.
                "note_type_concept_id":[note_type_concept_id], #	A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the type, origin or provenance of the Note. These belong to the 'Note Type' vocabulary
                "note_class_concept_id":[note_class_concept_id], #	A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the HL7 LOINC Document Type Vocabulary classification of the note.
                "note_title":[note_title], #	The title of the Note as it appears in the source.
                "note_text": [to_omop_note["note_text"]],#  The content of the Note.
                "encoding_concept_id":[encoding_concept_id],#	A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the note character encoding type
                "language_concept_id": [language_concept_id],# A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the language of the note
                "provider_id": [provider_id],# A foreign key to the Provider in the PROVIDER table who took the Note.
                "visit_occurrence_id": [to_omop_note["visit_occurrence_id"]],#    A foreign key to the Visit in the VISIT_OCCURRENCE table when the Note was taken.
                "visit_detail_id" : [visit_detail_id],#    A foreign key to the Visit in the VISIT_DETAIL table when the Note was taken.
                "note_source_value":[note_source_value] #	The source value associated with the origin of the Note
                }
        else:
            dict_note["note_id"].append(to_omop_note["note_id"])#	A unique identifier for each note.
            dict_note["person_id"].append(to_omop_note["person_id"])#[]	A foreign key identifier to the Person about whom the Note was recorded. The demographic details of that Person are stored in the PERSON table.
            dict_note["note_event_id"].append(note_event_id)#A foreign key identifier to the event (e.g. Measurement) Procedure) Visit) Drug Exposure) etc) record during which the note was recorded.
            dict_note["note_event_field_concept_id"].append(note_event_field_concept_id) #A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the field to which the note_event_id is referring.
            dict_note["note_date"].append(to_date.strftime('%Y-%m-%d')) #The date the note was recorded.
            dict_note["note_datetime"].append(to_date.strftime('%Y-%m-%d %H:%M:%S')) #The date and time the note was recorded.
            dict_note["note_type_concept_id"].append(note_type_concept_id) #	A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the type) origin or provenance of the Note. These belong to the 'Note Type' vocabulary
            dict_note["note_class_concept_id"].append(note_class_concept_id) #	A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the HL7 LOINC Document Type Vocabulary classification of the note.
            dict_note["note_title"].append(note_title) #	The title of the Note as it appears in the source.
            dict_note["note_text"].append(to_omop_note["note_text"])#  The content of the Note.
            dict_note["encoding_concept_id"].append(encoding_concept_id)#	A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the note character encoding type
            dict_note["language_concept_id"].append(language_concept_id)# A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the language of the note
            dict_note["provider_id"].append(provider_id)# A foreign key to the Provider in the PROVIDER table who took the Note.
            dict_note["visit_occurrence_id"].append(to_omop_note["visit_occurrence_id"])#    A foreign key to the Visit in the VISIT_OCCURRENCE table when the Note was taken.
            dict_note["visit_detail_id" ].append(visit_detail_id)#    A foreign key to the Visit in the VISIT_DETAIL table when the Note was taken.
            dict_note["note_source_value"].append(note_source_value) #	The source value associated with the origin of the Note

        return(dict_note)

    def generatePerson(dict_person, to_omop_person,
                       gender_concept_id,
                       year_of_birth,
                       month_of_birth,
                       day_of_birth,
                       birth_datetime,
                       death_datetime,
                       race_concept_id,
                       ethnicity_concept_id,
                       location_id,
                       provider_id,
                       care_site_id,
                       person_source_value,
                       gender_source_value,
                       gender_source_concept_id,
                       race_source_value,
                       race_source_concept_id,
                       ethnicity_source_value,
                       ethnicity_source_concept_id):
        if len(dict_person.keys()) ==0:
            dict_person = {
                "person_id":[to_omop_person["person_id"]], #	A unique identifier for each person.
                "gender_concept_id":[gender_concept_id],#	A foreign key that refers to an identifier in the CONCEPT table for the unique gender of the person.
                "year_of_birth":[year_of_birth],#	The year of birth of the person. For data sources with date of birth, the year is extracted. For data sources where the year of birth is not available, the approximate year of birth is derived based on any age group categorization available.
                "month_of_birth"	:[month_of_birth],#	The month of birth of the person. For data sources that provide the precise date of birth, the month is extracted and stored in this field.
                "day_of_birth":[day_of_birth],	#The day of the month of birth of the person. For data sources that provide the precise date of birth, the day is extracted and stored in this field.
                "birth_datetime"	:	[birth_datetime],#	The date and time of birth of the person.
                "death_datetime"	:	[death_datetime],#	The date and time of death of the person.
                "race_concept_id"	:	[race_concept_id],#	A foreign key that refers to an identifier in the CONCEPT table for the unique race of the person, belonging to the 'Race' vocabulary.
                "ethnicity_concept_id"	:	[ethnicity_concept_id],#	A foreign key that refers to the standard concept identifier in the Standardized Vocabularies for the ethnicity of the person, belonging to the 'Ethnicity' vocabulary.
                "location_id"	:	[location_id],#	A foreign key to the place of residency for the person in the location table, where the detailed address information is stored.
                "provider_id"	:	[provider_id],#	A foreign key to the primary care provider the person is seeing in the provider table.
                "care_site_id"	:	[care_site_id],#	A foreign key to the site of primary care in the care_site table, where the details of the care site are stored.
                "person_source_value"	:	[person_source_value],#	An (encrypted) key derived from the person identifier in the source data. This is necessary when a use case requires a link back to the person data at the source dataset.
                "gender_source_value"	:	[gender_source_value],#	The source code for the gender of the person as it appears in the source data. The person’s gender is mapped to a standard gender concept in the Standardized Vocabularies; the original value is stored here for reference.
                "gender_source_concept_id"	:	[gender_source_concept_id],#	A foreign key to the gender concept that refers to the code used in the source.
                "race_source_value" :	[race_source_value],#	The source code for the race of the person as it appears in the source data. The person race is mapped to a standard race concept in the Standardized Vocabularies and the original value is stored here for reference.
                "race_source_concept_id"	:	[race_source_concept_id],#	A foreign key to the race concept that refers to the code used in the source.
                "ethnicity_source_value"	:	[ethnicity_source_value],#	The source code for the ethnicity of the person as it appears in the source data. The person ethnicity is mapped to a standard ethnicity concept in the Standardized Vocabularies and the original code is, stored here for reference.
                "ethnicity_source_concept_id"	:	[ethnicity_source_concept_id]#	A foreign key to the ethnicity concept that refers to the code used in the source.
                    }
        else:
            dict_person["person_id"].append(to_omop_person["person_id"]) #A unique identifier for each person.
            dict_person["gender_concept_id"].append(gender_concept_id)#A foreign key that refers to an identifier in the CONCEPT table for the unique gender of the person.
            dict_person["year_of_birth"].append(year_of_birth)#The year of birth of the person. For data sources with date of birth, the year is extracted. For data sources where the year of birth is not available, the approximate year of birth is derived based on any age group categorization available.
            dict_person["month_of_birth"].append(month_of_birth)#The month of birth of the person. For data sources that provide the precise date of birth, the month is extracted and stored in this field.
            dict_person["day_of_birth"].append(day_of_birth)#The day of the month of birth of the person. For data sources that provide the precise date of birth, the day is extracted and stored in this field.
            dict_person["birth_datetime"].append(birth_datetime)#The date and time of birth of the person.
            dict_person["death_datetime"].append(death_datetime)#The date and time of death of the person.
            dict_person["race_concept_id"].append(race_concept_id)#A foreign key that refers to an identifier in the CONCEPT table for the unique race of the person, belonging to the 'Race' vocabulary.
            dict_person["ethnicity_concept_id"].append(ethnicity_concept_id)#A foreign key that refers to the standard concept identifier in the Standardized Vocabularies for the ethnicity of the person, belonging to the 'Ethnicity' vocabulary.
            dict_person["location_id"].append(location_id)#A foreign key to the place of residency for the person in the location table, where the detailed address information is stored.
            dict_person["provider_id"].append(provider_id)#A foreign key to the primary care provider the person is seeing in the provider table.
            dict_person["care_site_id"].append(care_site_id)#A foreign key to the site of primary care in the care_site table, where the details of the care site are stored.
            dict_person["person_source_value"].append(person_source_value)#An (encrypted) key derived from the person identifier in the source data. This is necessary when a use case requires a link back to the person data at the source dataset.
            dict_person["gender_source_value"].append(gender_source_value)#The source code for the gender of the person as it appears in the source data. The person’s gender is mapped to a standard gender concept in the Standardized Vocabularies; the original value is stored here for reference.
            dict_person["gender_source_concept_id"].append(gender_source_concept_id)#A foreign key to the gender concept that refers to the code used in the source.
            dict_person["race_source_value"].append(race_source_value)#The source code for the race of the person as it appears in the source data. The person race is mapped to a standard race concept in the Standardized Vocabularies and the original value is stored here for reference.
            dict_person["race_source_concept_id"].append(race_source_concept_id)#A foreign key to the race concept that refers to the code used in the source.
            dict_person["ethnicity_source_value"].append(ethnicity_source_value)#The source code for the ethnicity of the person as it appears in the source data. The person ethnicity is mapped to a standard ethnicity concept in the Standardized Vocabularies and the original code is, stored here for reference
            dict_person["ethnicity_source_concept_id"].append(ethnicity_source_concept_id)#	A foreign key to the ethnicity concept that refers to the code used in the source.
        return(dict_person)

    def buildNoteNlP(thisRoot, dict_note, note_id,note_nlp_id, nlp_workflow,thisTime,  filterType, dataframe=False):
        #table Note initial value
        note_event_id=None # "note_event_id"
        note_event_field_concept_id=0# "note_event_field_concept_id"
        note_type_concept_id=0# "note_type_concept_id"
        note_class_concept_id=0#"note_class_concept_id"
        note_title=None# "note_title"
        encoding_concept_id=0#"encoding_concept_id"
        language_concept_id=0#"language_concept_id"
        provider_id=None##"provider_id"
        visit_detail_id=None#"visit_occurrence_id"
        note_source_value=None #"note_source_value"

        #table Person initial value
        gender_concept_id=0 #"gender_concept_id"
        year_of_birth=0 # "year_of_birth"
        month_of_birth=None #"month_of_birth"
        day_of_birth=None# "day_of_birth"
        birth_datetime=None  # "birth_datetime"
        death_datetime=None #"death_datetime"
        race_concept_id=0 #"race_concept_id"
        ethnicity_concept_id=0 # "ethnicity_concept_id"
        location_id=None # "location_id"
        provider_id=None # "provider_id"
        care_site_id=None #"care_site_id"
        person_source_value=None# "person_source_value"
        gender_source_value=None#"gender_source_value"
        gender_source_concept_id=0#"gender_source_concept_id"
        race_source_value=None# "race_source_value"
        race_source_concept_id=0 #"race_source_concept_id"
        ethnicity_source_value=None#"ethnicity_source_value"
        ethnicity_source_concept_id=0#"ethnicity_source_concept_id"

        # Table Note_NLP
        #"note_annotate":json.dumps("'''"+json.dumps(grou.to_dict())+"'''"),
        annotations=dict()
        # note_nlp_id = 0#"nlp_id"
        section_concept_id=0#"section_concept_id"
        note_nlp_concept_id=0#"note_nlp_concept_id"
        note_nlp_source_concept_id=0#"note_nlp_source_concept_id"
        allchildren = thisRoot.getEntitiesChildren()
        negation={0:"affirmation", 1:"negation", "Null":"Null"}
        family={0:"family", 1:"patient", "Null":"Null"}
        for thisChild in allchildren:
            childProperties= thisChild.getParentsProperties(filterType)
            # print(childProperties)
            if not childProperties:
                dict_sentence = {"type":"Null" ,
                                 "value":"Null",
                                  "span":(0,0),
                                  "ngram":"Null",
                                  "hypothesis":"Null",
                                  "drwh_negation":"Null",
                                  "drwh_family":"Null",
                                  "drwh_sentences":"Null",
                                  "temporality":"document_date"}
            else:
                dict_sentence = {"type":childProperties[0]["type"] ,
                                 "value":"Null",
                                  "span":childProperties[0]["span"],
                                  "ngram":childProperties[0]["value"],
                                  "hypothesis":"Null",
                                  "drwh_negation":"Null",
                                  "drwh_family":"Null",
                                  "drwh_sentences":"Null",
                                  "temporality":"document_date"}
            dict_nlp={"type":thisChild.type ,
                      "value":thisChild.value,
                      "span":thisChild.span,
                      "ngram":thisChild.getNgram(),
                      "hypothesis":"Null",
                      "drwh_negation":"Null",
                      "drwh_family":"Null",
                      "drwh_sentences":"Null",
                      "temporality":"document_date"}
           
            if childProperties:
                for element in childProperties[0]["attributes"] ["properties"]:
                    dict_nlp[element["type"]]=element["value"]
                    dict_sentence[element["type"]]=element["value"]

            if dict_nlp["drwh_negation"] != "Null":
                dict_nlp["drwh_negation"]=negation[int(dict_nlp["drwh_negation"])]
                dict_sentence["drwh_negation"]=negation[int(dict_sentence["drwh_negation"])]

            if dict_nlp["drwh_family"] != "Null":
                dict_nlp["drwh_family"]=family[int(dict_nlp["drwh_family"])]
                dict_sentence["drwh_family"]=family[int(dict_sentence["drwh_family"])]

            term_exist="T"
            entity="entity"
            # print("#########dict nlp############")
            # print(dict_nlp)
            # print(annotations)
            annotations = omop.generateNoteNLP(annotations, dict_nlp,thisTime,
                                                              note_nlp_id, note_id,
                                                              section_concept_id,
                                                              note_nlp_concept_id,
                                                              note_nlp_source_concept_id,
                                                              nlp_workflow,
                                                              term_exist, entity)
            # term_exist="F"
            # entity="segment"
            note_nlp_id+=1
            annotations = omop.generateNoteNLP(annotations, dict_sentence,thisTime,
                                                              note_nlp_id, note_id,
                                                              section_concept_id,
                                                              note_nlp_concept_id,
                                                              note_nlp_source_concept_id,
                                                              nlp_workflow,
                                                              term_exist, entity)
            # print("annotation")
            # print(annotations)
            note_nlp_id+=1
        table_note =omop.generateNote(dict(), dict_note, thisTime,
                             note_event_id,
                             note_event_field_concept_id,
                             note_type_concept_id,
                             note_class_concept_id,
                             note_title,
                             encoding_concept_id,
                             language_concept_id,
                             provider_id,
                             visit_detail_id,
                             note_source_value)
        table_person = omop.generatePerson(dict(), {"person_id":dict_note["person_id"]},
                               gender_concept_id,
                               year_of_birth,
                               month_of_birth,
                               day_of_birth,
                               birth_datetime,
                               death_datetime,
                               race_concept_id,
                               ethnicity_concept_id,
                               location_id,
                               provider_id,
                               care_site_id,
                               person_source_value,
                               gender_source_value,
                               gender_source_concept_id,
                               race_source_value,
                               race_source_concept_id,
                               ethnicity_source_value,
                               ethnicity_source_concept_id)
        if dataframe:
            return(pandas.DataFrame(annotations), pandas.DataFrame(table_note),pandas.DataFrame(table_person) )
        else:
            return(annotations, table_note, table_person)
