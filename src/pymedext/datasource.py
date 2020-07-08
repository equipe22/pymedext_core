#!/usr/bin/env python3
#
from .connector import *
import logging
import psycopg2
logger = logging.getLogger(__name__)
import psycopg2.extras
from typing import Iterator, Dict, Any, Optional
import io
#source from https://hakibenita.com/fast-load-data-python-postgresql




def clean_csv_value(value: Optional[Any]) -> str:
    if value is None:
        return r'\N'
    return str(value).replace('\n', '\\n')


class StringIteratorIO(io.TextIOBase):
    def __init__(self, iter: Iterator[str]):
        self._iter = iter
        self._buff = ''

    def readable(self) -> bool:
        return True

    def _read1(self, n: Optional[int] = None) -> str:
        while not self._buff:
            try:
                self._buff = next(self._iter)
            except StopIteration:
                break
        ret = self._buff[:n]
        self._buff = self._buff[len(ret):]
        return ret

    def read(self, n: Optional[int] = None) -> str:
        line = []
        if n is None or n < 0:
            while True:
                m = self._read1()
                if not m:
                    break
                line.append(m)
        else:
            while n > 0:
                m = self._read1(n)
                if not m:
                    break
                n -= len(m)
                line.append(m)
        return ''.join(line)




class Source:
    # def __new__(self,Document):
    #     self.Document=Document
    #
    # Document save as
    @staticmethod
    def saveToSource():
        pass

    #Document load from and return a Document
    @staticmethod
    def loadFromSource():
        pass


class OmopSource(Source,PostGresConnector):
    def __init__(self, DB_host, DB_name, DB_port, DB_user, DB_password):
        super().__init__( DB_host, DB_name, DB_port, DB_user, DB_password)
        logger.info("Initialize Omop connection")

    def __insert_execute_values_iterator_person(self, dict_person_local: Iterator[Dict[str, Any]]) -> None:
        with self.conn.cursor() as cursor:
            psycopg2.extras.execute_values(cursor, """
                INSERT INTO person VALUES %s;
            """, ((
                dict_person_local["person_id"][position],
                dict_person_local["gender_concept_id"][position],
                dict_person_local["year_of_birth"][position],
                dict_person_local["month_of_birth"][position],
                dict_person_local["day_of_birth"][position],
                dict_person_local["birth_datetime"][position],
                dict_person_local["death_datetime"][position],
                dict_person_local["race_concept_id"][position],
                dict_person_local["ethnicity_concept_id"][position],
                dict_person_local["location_id"][position],
                dict_person_local["provider_id"][position],
                dict_person_local["care_site_id"][position],
                dict_person_local["person_source_value"][position],
                dict_person_local["gender_source_value"][position],
                dict_person_local["gender_source_concept_id"][position],
                dict_person_local["race_source_value"][position],
                dict_person_local["race_source_concept_id"][position],
                dict_person_local["ethnicity_source_value"][position],
                dict_person_local["ethnicity_source_concept_id"][position],
            ) for position in range (0,len(dict_person_local["person_id"]) ) ))

    def __insert_execute_values_iterator_note(self, dict_note: Iterator[Dict[str, Any]]) -> None:
        with self.conn.cursor() as cursor:
            psycopg2.extras.execute_values(cursor, """
                INSERT INTO note VALUES %s;
            """, ((
                dict_note["note_id"][position],
                dict_note["person_id"][position],
                dict_note["note_event_id"][position],
                dict_note["note_event_field_concept_id"][position],
                dict_note["note_date"][position],
                dict_note["note_datetime"][position],
                dict_note["note_type_concept_id"][position],
                dict_note["note_class_concept_id"][position],
                dict_note["note_title"][position],
                dict_note["note_text"][position],
                dict_note["encoding_concept_id"][position],
                dict_note["language_concept_id"][position],
                dict_note["provider_id"][position],
                dict_note["visit_occurrence_id"][position],
                dict_note["visit_detail_id"][position],
                dict_note["note_source_value"][position],
            ) for position in range (0,len(dict_note["note_id"])) ))

    def __insert_execute_values_iterator_note_nlp(self, dict_nlp: Iterator[Dict[str, Any]]) -> None:
        with self.conn.cursor() as cursor:
            psycopg2.extras.execute_values(cursor, """
                INSERT INTO note VALUES %s;
            """, ((
                dict_nlp["note_nlp_id"][position],
                dict_nlp["note_id"][position],
                dict_nlp["section_concept_id"][position],
                dict_nlp["snippet"][position].replace("|","##"),
                dict_nlp["offset"][position].replace("|","##"),
                dict_nlp["lexical_variant"][position].replace("|","##"),
                dict_nlp["note_nlp_concept_id"][position],
                dict_nlp["nlp_system"][position],
                dict_nlp["nlp_date"][position],
                dict_nlp["nlp_datetime"][position],
                dict_nlp["term_exists"][position].replace("|","##"),
                dict_nlp["term_temporal"][position].replace("|","##"),
                dict_nlp["term_modifiers"][position].replace("|","##"),
                dict_nlp["note_nlp_source_concept_id"][position],
                dict_nlp["term_negation"][position].replace("|","##"),
                dict_nlp["term_experiencer"][position].replace("|","##"),
                dict_nlp["term_hypothesis"][position].replace("|","##"),
                dict_nlp["term_type"][position].replace("|","##"),
                dict_nlp["nlp_workflow"][position],
                dict_nlp["offset_start"][position],
                dict_nlp["offset_end"][position],
            ) for position in range (0,len(dict_nlp["note_id"])) ))

    def __copy_string_iterator_note_nlp(self, dict_nlp_local: Iterator[Dict[str, Any]], size: int = 8192) -> None:
        with self.conn.cursor() as cursor:
            note_nlp_string_iterator = StringIteratorIO((
                '|'.join(map(clean_csv_value, (
                dict_nlp_local["note_nlp_id"][position],
                dict_nlp_local["note_id"][position],
                dict_nlp_local["section_concept_id"][position],
                dict_nlp_local["snippet"][position].replace("|","##").replace("\ ","\\" ),
                dict_nlp_local["offset"][position].replace("|","##").replace("\ ","\\"),
                dict_nlp_local["lexical_variant"][position].replace("|","##").replace("\ ","\\"),
                dict_nlp_local["note_nlp_concept_id"][position],
                dict_nlp_local["nlp_system"][position],
                dict_nlp_local["nlp_date"][position],
                dict_nlp_local["nlp_datetime"][position],
                dict_nlp_local["term_exists"][position],
                dict_nlp_local["term_temporal"][position],
                '"""'+dict_nlp_local["term_modifiers"][position]+'"""',
                dict_nlp_local["note_nlp_source_concept_id"][position],
                dict_nlp_local["term_negation"][position],
                dict_nlp_local["term_experiencer"][position],
                dict_nlp_local["term_hypothesis"][position],
                dict_nlp_local["term_type"][position],
                dict_nlp_local["nlp_workflow"][position],
                dict_nlp_local["offset_start"][position],
                dict_nlp_local["offset_end"][position],
                ))) + '\n'
                for position in range (0,len(dict_nlp_local["note_id"]) )
            ))
            cursor.copy_from(note_nlp_string_iterator, 'note_nlp', sep='|', size=size)

    def __getInfo(self,getcolumn, fromTable):
        self.cur.execute("select "+getcolumn+" from "+fromTable)
        rows = self.cur.fetchall()
        theColumn=[]
        for this_id in rows:
            # print(this_id)
            theColumn.append(this_id[0])
        return(theColumn)


    # @staticmethod
    def getLastNotenlpid(self):
        self.cur.execute("select note_nlp_id from note_nlp order by note_nlp_id desc limit 1")
        rows = self.cur.fetchall()
        lastIDs=[]
        for this_ids in rows:
            lastIDs.append(this_ids[0])
        return(lastIDs[-1])


    def saveToSource(self, table_person, table_note, table_note_nlp):
        patient_ids = self.__getInfo("person_id","person")
        print(patient_ids)
        if table_person["person_id"][0] not in patient_ids:
            self.__insert_execute_values_iterator_person(table_person)
        else:
            print("patient already exist")
        note_ids = self.__getInfo("note_id","note")
        if table_note["note_id"][0] not in note_ids:
            self.__insert_execute_values_iterator_note(table_note)
            self.__copy_string_iterator_note_nlp(table_note_nlp) #faster but data note cleaned so difficult to load it easily
            # self.__insert_execute_values_iterator_note_nlp(table_note_nlp)
        else:
            print("note already exist, skip it")
        return(0)
