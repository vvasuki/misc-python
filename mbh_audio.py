import logging

# This should be at the top of the file to preempt earlier imports from resetting the level. 
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s %(filename)s:%(lineno)d %(message)s"
)

import pprint
# Reference - https://internetarchive.readthedocs.io/en/latest/api.html
import internetarchive
import os
import glob
import eyed3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas

logging.warning("Logging.warning functional!")
logging.info("Logging.info functional!")

ARCHIVE_ITEM_NAME = "mahAbhArata-mUla-paThanam-GP"
LOCAL_REPO_PATH = "/home/vvasuki/mahabharata-audio-2018/"
SPREADSHEET_ID = "1sNH1AWhhoa5VATqMdLbF652s7srTG0Raa6K-sCwDR-8"
SPREADSHEET_RANGE_KARYAAVALII = "कार्यावली!A1:G10"
# SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
# SPREADSHEET_RANGE_KARYAAVALII = 'Class Data!A2:E'
local_mp3_file_paths = sorted(glob.glob(os.path.join(LOCAL_REPO_PATH, "parva*", "mp3", "*.mp3")))

logging.info("Got %d files" % (len(local_mp3_file_paths)))

def update_archive_item(overwrite_all=False):
    archive_item = internetarchive.get_item(ARCHIVE_ITEM_NAME)
    logging.info(archive_item.identifier)
    local_mp3_file_basenames = list(map(os.path.basename, local_mp3_file_paths))
    original_item_files = list(filter(lambda x: x["source"] == "original" and not x["name"].startswith(archive_item.identifier) and not x["name"].startswith("_"), archive_item.files))
    original_item_file_names = sorted(map(lambda x: x["name"], original_item_files))
    obsolete_original_item_file_names = list(filter(lambda x: x not in local_mp3_file_basenames, original_item_file_names))
    
    logging.info("************************* Deleting the below unaccounted for files: \n" + pprint.pformat(obsolete_original_item_file_names))
    internetarchive.delete(archive_item.identifier, files=obsolete_original_item_file_names, cascade_delete=True)
    
    logging.info("************************* Now uploading")
    upload_locus_to_local_file_map = dict(zip(local_mp3_file_basenames, local_mp3_file_paths))
    filtered_upload_locus_to_local_file_map = dict(filter(lambda item: item[0] not in original_item_file_names, upload_locus_to_local_file_map.items()))
    logging.info(pprint.pformat(filtered_upload_locus_to_local_file_map.items()))
    # checksum=True seems to not avoid frequent reuploads. Archive item mp3 checksum end up varying because of metadata changes? 
    if (overwrite_all):
        responses = archive_item.upload(upload_locus_to_local_file_map, verbose=False, checksum=False, verify=False)
        logging.info(pprint.pformat(zip(upload_locus_to_local_file_map.keys(), responses)))
    else:
        if (len(filtered_upload_locus_to_local_file_map) > 0):
            responses = archive_item.upload(filtered_upload_locus_to_local_file_map, verbose=False, checksum=False,
verify=False)
            logging.info(pprint.pformat(zip(filtered_upload_locus_to_local_file_map.keys(), responses)))
        else:
            logging.warning("Found nothing to update!")
    

def fix_metadata(adhyaaya_df, update_archive=False):
    archive_item = internetarchive.get_item(ARCHIVE_ITEM_NAME)
    logging.info(archive_item.identifier)
    local_mp3_file_basenames = list(map(os.path.basename, local_mp3_file_paths))
    original_item_files = list(filter(lambda x: x["source"] == "original" and not x["name"].startswith(archive_item.identifier), archive_item.files))
    original_item_file_names = sorted(map(lambda x: x["name"], original_item_files))
    for mp3_path in local_mp3_file_paths:
        basename = os.path.basename(mp3_path)
        parva_adhyaaya_part_id = os.path.splitext(basename)[0]
        parva_adhyaaya_id = parva_adhyaaya_part_id[0:7]
        logging.info("Updating metadata for %s" % (basename))
        audiofile = eyed3.load(mp3_path)
        parva_id = basename.split("-")[0]
        audiofile.initTag()
        audiofile.tag.artist = adhyaaya_df.loc[parva_adhyaaya_id, "पठिता"]
        audiofile.tag.title = "%s - %s" % (parva_adhyaaya_part_id, audiofile.tag.artist)
        audiofile.tag.album = "महाभारतम् mahAbhAratam - parva %s" % (parva_id)
        audiofile.tag.album_artist = "वेदव्यासः vedavyAsa"
        audiofile.tag.save()
        if update_archive and (basename in original_item_file_names):
            r = internetarchive.modify_metadata(ARCHIVE_ITEM_NAME, metadata=dict(title=audiofile.tag.title, album=audiofile.tag.album, album_artist = audiofile.tag.album_artist, artist = audiofile.tag.artist, creator=audiofile.tag.artist), target=basename)

def get_adhyaaya_data():
    # Obtained from https://console.developers.google.com/apis/credentials?project=sanskritnlp
    GOOGLE_KEY = '/home/vvasuki/sysconf/kunchikA/google_service_account_key_sanskritnlp.json'
    SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_KEY, SCOPES)

    client = gspread.authorize(creds)
    logging.debug(pprint.pformat(client.list_spreadsheet_files()))
    sheet_book = client.open_by_key(SPREADSHEET_ID)
    logging.debug(sheet_book.worksheets())
    # print(sheet_book.worksheets())
    kaaryaavalii_sheet_values = sheet_book.worksheet("कार्यावली").get_all_values()
    adhyaaya_data = pandas.DataFrame(kaaryaavalii_sheet_values[1:], columns=kaaryaavalii_sheet_values.pop(0))
    adhyaaya_data = adhyaaya_data.set_index("पर्व-अध्यायः")
    logging.debug(adhyaaya_data.loc["001-001", "पठिता"])
    return adhyaaya_data

# fix_metadata(get_adhyaaya_data())
update_archive_item(overwrite_all=False)