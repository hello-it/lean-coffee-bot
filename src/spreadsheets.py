# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# QUESTION: Should we create a config file for this? I have got implementation.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = './client_secret_470248873483-3ji1549qchib3cmj85j1lf9ma5hphgta.apps.googleusercontent.com.json'
APPLICATION_NAME = 'Lean Coffee'
API_KEY = 'XXX'
SPREADSHEET_ID = 'YYY'


try:
    import argparse
    FLAGS = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    FLAGS = None


def get_credentials():
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
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if FLAGS:
            credentials = tools.run_flow(flow, store, FLAGS)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        # TODO: Vadim, we can change this message if you want
        print('[INFO] Storing credentials to ' + credential_path)
    return credentials


def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    return discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)


def insert():
    value_input_option = 'RAW'
    insert_data_option = 'INSERT_ROWS'

    value_range_body = {
        "values": [
            # TODO: change this list
            ["dev", "python vs go", "OPEN", "0", "0", "0"],
        ]
    }

    request = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID,
                                                     # TODO: we don't use A1 column
                                                     range='B1',
                                                     valueInputOption=value_input_option,
                                                     insertDataOption=insert_data_option,
                                                     body=value_range_body)
    response = request.execute()

    # TODO: it is very well for debug or logging
    print(response)


# TODO: It just example. Delete it after implementing write function
service = get_service()
insert()
