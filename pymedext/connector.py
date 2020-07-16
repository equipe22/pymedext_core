#!/usr/bin/env python3

import logging
import psycopg2

logger = logging.getLogger(__name__)


class Connector:
    pass

class DatabaseConnector:
    def __init__(self, DB_host, DB_name, DB_port, DB_user, DB_password):
        self.DB_host =  DB_host
        self.DB_name = DB_name
        self.DB_port = DB_port
        self.DB_user = DB_user
        self.DB_password = DB_password
        logger.info("Initialize Database Connection")
    def startConnection(self):
        pass


class APIConnector:
    pass

class cxORacleConnector:
    pass

class PostGresConnector(DatabaseConnector):
    def __init__(self, DB_host, DB_name, DB_port, DB_user, DB_password):
        super().__init__( DB_host, DB_name, DB_port, DB_user, DB_password)
        logger.info("Initialize Database Connection")
        self.cur = None
        self.conn = None
        self.startConnection()
    def startConnection(self):
        self.conn = psycopg2.connect(
            host=self.DB_host,
            database = self.DB_name,
            port = self.DB_port,
            user = self.DB_user,
            password = self.DB_password
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        return(0)


class SSHConnector:
    pass


