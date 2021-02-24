from __future__ import print_function
import pickle
import os.path
import os
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload


class MyDrive:
    def __init__(self):
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive']
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)
        self.main_folder_id = self.cratate_main_folder()

    def create_folder(self, name):
        folder_id = self.main_folder_id
        file_metadata = {
            'name': name,
            'parents': [folder_id],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.service.files().create(body=file_metadata,
                                           fields='id, name').execute()
        return file.get('name')

    def cratate_main_folder(self):
        if check := self.check_if_main_folder():
            return check
        file_metadata = {
            'name': 'db',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.service.files().create(body=file_metadata,
                                           fields='id').execute()
        return file.get('id')

    def check_if_main_folder(self):
        page_token = None
        while True:
            response = self.service.files().list(q="fullText contains 'db'",
                                                 spaces='drive',
                                                 fields='nextPageToken, files(id, name)',
                                                 pageToken=page_token).execute()
            for file in response.get('files', []):
                if file.get('name') == 'db':
                    return file.get('id')
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return False


def main():
    my_drive = MyDrive()
    print(my_drive.create_folder('adwasdd'))
    

if __name__ == '__main__':
    main()
