import xlrd
from configuration.format_xl_conf import *


def read_excel_sheet(file_path):
    xl_workbook = xlrd.open_workbook(file_path)
    xl_sheet = xl_workbook.sheet_by_index(0)
    return xl_sheet


def get_meta_data(xl_sheet):
    name = xl_sheet.cell(NAME_ROW, NAME_COL).value
    link_to_src = xl_sheet.cell(SRC_LINK_ROW, SRC_LINK_COL).value
    language = xl_sheet.cell(LANGUAGE_ROW, LANGUAGE_COL).value
    sagah = xl_sheet.cell(SAGAH_ROW, SAGAH_COL).value
    return name, link_to_src, language, sagah


def create_jsons_from_tags(xl_sheet):
    tags_list = []
    tgt = ' '
    idx = FIRST_ROW_TAG_STARTS
    name, link_to_src, language, sagah = get_meta_data(xl_sheet)
    while tgt != '':
        tag = create_tag_from_sheet(idx, xl_sheet, name, link_to_src, language, sagah)
        tags_list.append(tag)
        idx += 1
    return tags_list


def create_tag_from_sheet(idx, xl_sheet, name, link_to_src, language, sagah):
    sentence_id = xl_sheet.cell(idx, SENTENCE_ID_COL).value
    src = xl_sheet.cell(idx, SRC_COL).value
    tgt = xl_sheet.cell(idx, TGT_COL).value
    tag = {'id': sentence_id,
           'src': src,
           'tgt': tgt,
           'tagger_name': name,
           'link_to_src': link_to_src,
           'language': language,
           'sagah': sagah
           }
    return tag
