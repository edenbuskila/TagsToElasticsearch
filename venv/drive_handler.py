from __future__ import print_function
import pickle
import os.path
from logger import write_log
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from conf import *

SCOPES = ['https://www.googleapis.com/auth/drive']

def load_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service

def get_files(sagah):
    service = load_service()
    results = service.files().list(
        q="'"+sagah['folder_id']+"' in parents and mimeType !='application/vnd.google-apps.folder'",
        spaces='drive',
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    files_ids = []
    if not items:
        write_log('No files found', True)
    else:
        for item in items:
            if is_new_file(item['id']):
                download_file(service, item['id'], sagah)
                update_new_file(item['id'])
                files_ids.append(item['id'])
    return files_ids
                

def download_file(service, file_id, sagah):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(sagah['tgt_path'] + file_id +'.xlsx', 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    write_log('download_file ' + file_id + ' finished successfully', False)
    
def is_new_file(file_id):
    with open('data/metadata.txt', 'r+') as metadata:
        files_ids = metadata.readlines()
        if file_id in files_ids:
            return False
        return True
    
def update_new_file(file_id):
    with open('data/metadata.txt', 'a+') as metadata:
        metadata.write(file_id + '\n')
        