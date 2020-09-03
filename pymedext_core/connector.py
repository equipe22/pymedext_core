#!/usr/bin/env python3

import logging
import psycopg2

###
import os
import requests
from urllib.parse import urljoin
import random
import re
from scp import SCPClient

import paramiko



proxies = {
  "http": None,
  "https": None,
}
###

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


#### Alice
#### Pour les API copy de la classe Router dont hérite la classe DoccanoClient dans doccanp_api_client
#### Cette classe définit les méthodes post et get
#### À voir si ce sera commun à toutes les API...
# ------------------------------------------------------------------------
# ROUTER
# ------------------------------------------------------------------------
class _Router:
    """
    Largely inspired of https://github.com/doccano/doccano-client.git work

    Provides generic `get` and `post` methods. Implemented by DoccanoClient.
    """

    def get(
            self,
            endpoint: str,
    ) -> requests.models.Response:
        """
        Args:
            endpoint (str): An API endpoint to query.

        Returns:
            requests.models.Response: The request response.
        """
        request_url = urljoin(self.baseurl, endpoint)
        return self.session.get(request_url)

    def post(
            self,
            endpoint: str,
            data: dict = {},
            files: dict = {},
    ) -> requests.models.Response:
        """
        """
        request_url = urljoin(self.baseurl, endpoint)
        return self.session.post(request_url, data=data, files=files)

    def build_url_parameter(
            self,
            url_parameter: dict
    ) -> str:
        """
        Format url_parameters.

        Args:
            url_parameter (dict): Every value must be a list.

        Returns:
            A URL parameter string. Ex: `?key1=u1&key1=u2&key2=v1&...`
        """
        return ''.join(['?', '&'.join(
            ['&'.join(['='.join([tup[0], str(value)]) for value in tup[1]]) for tup in url_parameter.items()])])


# ------------------------------------------------------------------------
# CLIENT
# ------------------------------------------------------------------------

class APIConnector(_Router):
    """
    Largely inspired of https://github.com/doccano/doccano-client.git work

    Pour l'instant copy de la classe DoccanoClient dans doccano_api_client.py :

    TODO: investigate alternatives to plaintext login

    Args:
        baseurl (str): The baseurl of a Doccano instance.
        username (str): The Doccano username to use for the client session.
        password (str): The respective username's password.

    Returns:
        An authorized client instance.
    """
    def __init__(self, baseurl: str, username: str, password: str):
        self.baseurl = baseurl if baseurl[-1] == '/' else baseurl+'/'
        self.session = requests.Session()
        self._login(username, password)

    def _login(
        self,
        username: str,
        password: str
    ) -> requests.models.Response:
        """
        Authorizes the DoccanoClient instance.

        Args:


        Returns:
            requests.models.Response: The authorization request response.
        """
        url = 'v1/auth-token'
        auth = {'username': username, 'password': password}
        response = self.post(url, auth)
        print(response)
        token = response.json()['token']
        self.session.headers.update(
            {
                'Authorization': 'Token {token}'.format(token=token),
                'Accept': 'application/json'
            }
        )
        return response


#####
#### Alice

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

class SimpleAPIConnector:
    """
    TODO: implement a connection to a server with
    paramiko, should also extend Connector @David?
    """

    def __init__(self, host):

        self.host = host
        self.session = None
        self.startConnection()


    def startConnection(self):
        """Initialize  a requests object
        :returns: 0
        :rtype: 0

        """
        self.session =  requests.Session()
        return(0)

#######################                         DAVID                                           ########################
class SSHConnector:
    """
    TODO: implement a connection to a server with
    paramiko, should also extend Connector @David?
    """

    def __init__(self, scp_host, scp_user, scp_password):

        self.scp_host = scp_host
        self.scp_user = scp_user
        self.scp_password = scp_password
        self.sshConnection = paramiko.SSHClient()
        self.sshConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def transfert_brat_file(self, brat_file, scp_repertory):
        self.sshConnection.connect(self.scp_host, username=self.scp_user,
                              password=self.scp_password)
        scp_cursor = SCPClient(self.sshConnection.get_transport())
        if scp_repertory[-1] != '/':
            scp_repertory = scp_repertory +'/'
        scp_cursor.put(brat_file, scp_repertory + brat_file)


