# -*- coding: utf-8 -*-

from __future__ import print_function

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import os
import httplib2
import configparser


class Spreadsheet(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        # QUESTION: It looks like bad practice. How can we make it different?
        self.config.read('../resources/config.ini')
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
            flow = client.flow_from_clientsecrets(self.config['google']['secret_file'], self.config['google']['scopes'])
            flow.user_agent = self.config['google']['app_name']
            credentials = tools.run(flow, store)
            # TODO: Vadim, let's send it to logger?
            print('[INFO] Storing credentials to ' + credential_path)
        return credentials

    def get_service(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discovery_url = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
        return discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)

    def insert(self, topic, theme, status, points, cycles):
        value_input_option = 'RAW'
        insert_data_option = 'INSERT_ROWS'

        value_range_body = {
            "values": [
                [topic, theme, status, points, cycles],
            ]
        }

        request = self.service.spreadsheets().values().append(spreadsheetId=self.config['google']['spreadsheet_id'],
                                                              # TODO: we don't use A1 column
                                                              range='B1',
                                                              valueInputOption=value_input_option,
                                                              insertDataOption=insert_data_option,
                                                              body=value_range_body)
        response = request.execute()

        # TODO: Vadim, let's send it to logger? [2]
        print(response)
