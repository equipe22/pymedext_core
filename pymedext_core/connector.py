#!/usr/bin/env python3

import logging
import psycopg2

logger = logging.getLogger(__name__)


class Connector:
    """
    TODO : make this an abstract class for other connector
    """
    pass

class DatabaseConnector:
    """ Abstract class specialize in database connection
    """
    def __init__(self, DB_host, DB_name, DB_port, DB_user, DB_password):
        """initialize some basic variable to connect into a database

        :param DB_host: host name
        :param DB_name:  database name
        :param DB_port: connection port
        :param DB_user:  user name
        :param DB_password: user password
        :returns: abstract databse connector
        :rtype: DatabaseConnect

        """
        self.DB_host =  DB_host
        self.DB_name = DB_name
        self.DB_port = DB_port
        self.DB_user = DB_user
        self.DB_password = DB_password
        logger.info("Initialize Database Connection")
    def startConnection(self):
        """
        Abstract function where each DatabaseConnector should implement the
        Database connection
        """
        pass


class APIConnector:
    """ Abstact connector to an API
    TODO : discuss with @Alice how to implement it for Doccano
    """
    pass

class cxORacleConnector(DatabaseConnector):
    """ Abstact connector to an Oracle database using cxOracle
    """
    pass

class PostGresConnector(DatabaseConnector):
    """
    Abstract Connector to a Postgres Database
    """
    def __init__(self, DB_host, DB_name, DB_port, DB_user, DB_password):
        """Initialize a postGre connector


        :param DB_host: host name
        :param DB_name:  database name
        :param DB_port: connection port
        :param DB_user:  user name
        :param DB_password: user password
        :returns: A PostregesConnector
        :rtype: POstGresConnector

        """
        super().__init__( DB_host, DB_name, DB_port, DB_user, DB_password)
        logger.info("Initialize Database Connection")
        self.cur = None
        self.conn = None
        self.startConnection()
    def startConnection(self):
        """Initialize the connection to the POstGresConnector
        :returns: 0
        :rtype: 0

        """
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

#######################                         DAVID                                           ########################
class SSHConnector:
    """
    TODO: implement a connection to a server with
    paramiko, should also extend Connector @David?
    """

    def __init__(self, scp_host, scp_user, scp_password):
        import paramiko

        self.scp_host = scp_host
        self.scp_user = scp_user
        self.scp_password = scp_password
        self.sshConnection = paramiko.SSHClient()
        self.sshConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def transfert_brat_file(self, brat_file, scp_repertory):
        from scp import SCPClient

        self.sshConnection.connect(self.scp_host, username=self.scp_user,
                              password=self.scp_password)
        scp_cursor = SCPClient(self.sshConnection.get_transport())
        if scp_repertory[-1] != '/':
            scp_repertory = scp_repertory +'/'
        scp_cursor.put(brat_file, scp_repertory + brat_file)


