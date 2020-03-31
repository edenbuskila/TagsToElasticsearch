from drive_handler import get_files
from conf import *
from xls_to_json import create_jsons_from_tags , read_excel_sheet

stt_arabic = {'folder_id' : STT_ARABIC_FOLDER_ID , 'tgt_path' : STT_ARABIC_TGT_PATH}
stt_farsi  = {'folder_id' : STT_FARSI_FOLDER_ID , 'tgt_path' : STT_FARSI_TGT_PATH}
literary_arabic = {'folder_id' : LITERARY_ARABIC_FOLDER_ID , 'tgt_path' : LITERARY_ARABIC_TGT_PATH}
literary_farsi = {'folder_id' : LITERARY_FARSI_FOLDER_ID , 'tgt_path' : LITERARY_FARSI_TGT_PATH}

def main():
    sagah_list = [stt_arabic, stt_farsi, literary_arabic, literary_farsi]
    tags_jsons = []
    for sagah in sagah_list:
        files_ids = get_files(sagah)
        for file_id in files_ids:
            xl_sheet = read_excel_sheet(sagah['tgt_path']+file_id+'.xlsx')
            tags_jsons = create_jsons_from_tags(xl_sheet)
    for tag_json in tags_jsons:
        

if __name__ == '__main__':
    main()