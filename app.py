from __future__ import print_function
import pickle
import os.path
import os
import io
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload

file_types = {
    'image': 'image/jpeg',
    'json': 'application/json'
}


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
        self.main_folder_id = self.create_main_folder()

    def create_folder(self, name):
        folder_id = self.main_folder_id
        file_metadata = {
            'name': name,
            'parents': [folder_id],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.service.files().create(body=file_metadata,
                                           fields='id, name').execute()
        file_name = file.get('name')
        file_id = file.get('id')
        return file_name

    def create_main_folder(self):
        if check := self.check_main_folder():
            return check
        file_metadata = {
            'name': 'db',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.service.files().create(body=file_metadata,
                                           fields='id').execute()
        return file.get('id')

    def check_main_folder(self, name='db'):
        page_token = None
        while True:
            response = self.service.files().list(q=f"fullText contains '{name}'",
                                                 spaces='drive',
                                                 fields='nextPageToken, files(id, name)',
                                                 pageToken=page_token).execute()
            for file in response.get('files', []):
                if file.get('name') == name:
                    return file.get('id')
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return False

    def check_folder(self, name):
        page_token = None
        while True:
            response = self.service.files().list(
                q=f"fullText contains '{name}' and '{self.main_folder_id}' in parents",
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType)',
                pageToken=page_token
            ).execute()

            for file in response.get('files', []):
                if file.get('name') == name:
                    return file.get('id')
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return False

    def get_file(self, file_id):
        '''Read Json obj'''
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        fh.seek(0)
        file = fh

        return file

    def get_json(self, file_id):
        json_obj = self.get_file(file_id)
        return json.load(json_obj)

    def create_file(self, file):
        file_metadata = {'name': 'photo.jpg'}
        # media = MediaFileUpload(file, mimetype='image/jpeg')
        media = MediaIoBaseUpload(file, mimetype='image/jpeg')
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        return file

    def list_folder(self, folder_id, page_size=10):
        # Call the Drive v3 API
        results = self.service.files().list(
            q = f"'{folder_id}' in parents",
            pageSize=page_size, 
            fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])
        obj = []

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                obj.append({'type': item['mimeType'], 'id': item['id']})
                print(u'{0} {1}'.format(item['mimeType'], item['id'])) 
        return obj


class DriveApi(MyDrive):
    def get_all(self, folder_name):
        parent = self.check_folder(folder_name)
        self.list_folder(parent)

    def get(self, id):
        obj = {
            'json': '',
            'image': ''
        }
        files = self.list_folder(id)
        print(files)
        for file in files:
            file_id = file['id']
            if file['type'] == file_types['json']:
                json = self.get_json(file_id)
                obj['json'] = json
            if file['type'] == file_types['image']:
                obj['image'] = file_id
        print(obj)
        return obj

    def update(self, id):
        pass

    def delete(self, id):
        pass


def main():
    my_drive = DriveApi()
    # print(my_drive.get_file('1YUNp3m-VEm0IcOJJ8-2EbZI0YWVS3UXd'))
    # file = io.BytesIO(b'asdasd')
    # my_drive.create_file(file)
    my_drive.get_all('projects')
    my_drive.get('1x-B_D8MyZEEVr8qLbHUx8fpmcvE2eNiI')
    

if __name__ == '__main__':
    main()
