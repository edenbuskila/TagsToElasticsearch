from drive_handler import get_files
from conf import *
from xls_to_json import create_jsons_from_tags , read_excel_sheet
import json
from elasticsearch import Elasticsearch
import uuid
import schedule
import time

stt_arabic = {'folder_id' : STT_ARABIC_FOLDER_ID , 'tgt_path' : STT_ARABIC_TGT_PATH, 'name' : 'stt_arabic'}
stt_farsi  = {'folder_id' : STT_FARSI_FOLDER_ID , 'tgt_path' : STT_FARSI_TGT_PATH, 'name' : 'stt_farsi'}
literary_arabic = {'folder_id' : LITERARY_ARABIC_FOLDER_ID , 'tgt_path' : LITERARY_ARABIC_TGT_PATH, 'name' : 'literary_arabic'}
literary_farsi = {'folder_id' : LITERARY_FARSI_FOLDER_ID , 'tgt_path' : LITERARY_FARSI_TGT_PATH, 'name' : 'literary_farsi'}
schedule.every().day.at("11:00").do(job)

def job():
    sagah_list = [stt_arabic, stt_farsi, literary_arabic, literary_farsi]
    tags_jsons = []
    for sagah in sagah_list:
        files_ids = get_files(sagah)
        sagah_tags_jsons = []
        for file_id in files_ids:
            xl_sheet = read_excel_sheet(sagah['tgt_path']+file_id+'.xlsx')
            tags = create_jsons_from_tags(xl_sheet, sagah['tgt_path']+file_id+'.xlsx')
            sagah_tags_jsons.append({'file_id': file_id, 'tags': tags})
        tags_jsons.append({'sagah': sagah['name'], 'data': sagah_tags_jsons})

    with open('data/arabic-tags.json', 'w+', encoding='utf-8') as all_jsons:
        all_jsons.write((json.dumps(tags_jsons, ensure_ascii=False).encode('utf8').decode()))
    es = Elasticsearch(['http://tags-master-node1.eastus.cloudapp.azure.com'], http_auth=('elastic', 'CacheMemory321'),
                       port=9200)
    for tag_json in tags_jsons:
        sagah = tag_json['sagah']
        for data in tag_json['data']:
            for tag in data['tags']:
                es.index(index=sagah, id=uuid.uuid4(), body=tag)
                
def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()