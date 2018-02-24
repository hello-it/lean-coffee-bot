# -*- coding: utf-8 -*-

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'resources'))
from config import *


class Spreadsheet(object):
    def __init__(self):
        self.service = self.get_service()

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'credentials.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(secret_file, scopes)
            flow.user_agent = app_name
            credentials = tools.run_flow(flow, store)
            print '[INFO] Storing credentials to ' + credential_path
        return credentials

    def get_service(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        return discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)

    def insert(self, topic, theme, status, points, cycles):
        insert_range = 'B1'
        value_input_option = 'RAW'
        insert_data_option = 'INSERT_ROWS'
        value_range_body = {
            "values": [
                [topic, theme, status, points, cycles],
            ]
        }

        self.service.spreadsheets().values().append(spreadsheetId=spreadsheet_id,
                                                    range=insert_range,
                                                    valueInputOption=value_input_option,
                                                    insertDataOption=insert_data_option,
                                                    body=value_range_body).execute()
