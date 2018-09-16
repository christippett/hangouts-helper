import json
import os

import google.auth
import google_auth_httplib2
from google.oauth2 import service_account
from googleapiclient import discovery


class HangoutsChatAPI:
    GOOGLE_CHAT_SCOPES = ['https://www.googleapis.com/auth/chat.bot']

    def __init__(self, service_account_info=None, service_account_file=None):
        self.api = self._initialize_api(
            service_account_info, service_account_file)

    def _initialize_api(self, service_account_info=None, service_account_file=None):
        if service_account_info is not None:
            creds = service_account.Credentials.from_service_account_info(
                service_account_info, scopes=self.GOOGLE_CHAT_SCOPES)
        elif service_account_file is not None:
            creds = service_account.Credentials.from_service_account_file(
                service_account_info, scopes=self.GOOGLE_CHAT_SCOPES)
        else:
            creds, _ = google.auth.default(scopes=self.GOOGLE_CHAT_SCOPES)
        http = google_auth_httplib2.AuthorizedHttp(creds)
        return discovery.build('chat', 'v1', http=http)

    def list_spaces(self, page_size=100):
        spaces_list = list()
        spaces = self.api.spaces()
        request = spaces.list(pageSize=page_size)
        while request is not None:
            response = request.execute()
            spaces_list += response.get('spaces', [])
            request = spaces.list_next(request, response)
        return spaces_list

    def get_space(self, name):
        return self.api.spaces().get(name=name).execute()

    def list_memberships(self, space_name, page_size=100):
        memberships = list()
        members = self.api.spaces().members()
        request = members.list(parent=space_name, pageSize=page_size)
        while request is not None:
            response = request.execute()
            memberships += response.get('memberships', [])
            request = members.list_next(request, response)
        return memberships

    def get_membership(self, name):
        return self.api.spaces().members().get(name=name).execute()

    def create_message(self, message, space_name, thread_id=None, thread_key=None):
        """ Sends an asynchronous message to Hangouts Chat. """
        # Update thread (will send as new message if thread_id is None)
        if thread_id is not None:
            message['thread'] = thread_id
        return self.api.spaces().messages().create(
            parent=space_name, body=message, threadKey=thread_key).execute()

    def get_message(self, name):
        return self.api.spaces().messages().get(name=name).execute()

    def delete_message(self, name):
        return self.api.spaces().messages().delete(name=name).execute()

    def update_message(self, name, message):
        update_kwargs = {
            'name': name,
            'body': message,
            'updateMask': 'text,cards'
        }
        return self.api.spaces().messages().update(**update_kwargs).execute()
