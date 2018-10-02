import logging
import pprint
# Reference - https://internetarchive.readthedocs.io/en/latest/api.html
import internetarchive
import os
import glob
import eyed3

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s %(message)s"
)

ARCHIVE_ITEM_NAME = "mahAbhArata-mUla-paThanam-GP"
LOCAL_REPO_PATH = "/home/vvasuki/mahabharata-audio-2018/"
SPREADSHEET_ID = "1sNH1AWhhoa5VATqMdLbF652s7srTG0Raa6K-sCwDR-8"
SPREADSHEET_RANGE_KARYAAVALII = "कार्यावली!A1:G10"
# SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
# SPREADSHEET_RANGE_KARYAAVALII = 'Class Data!A2:E'
local_mp3_file_paths = sorted(glob.glob(os.path.join(LOCAL_REPO_PATH, "parva*", "mp3", "*.mp3")))

def update_archive_item():
    archive_item = internetarchive.get_item(ARCHIVE_ITEM_NAME)
    logging.info(archive_item.identifier)
    
    local_mp3_file_basename = list(map(os.path.basename, local_mp3_file_paths))
    
    original_item_files = list(filter(lambda x: x["source"] == "original" and not x["name"].startswith(archive_item.identifier), archive_item.files))
    original_item_file_names = sorted(map(lambda x: x["name"], original_item_files))
    obsolete_original_item_file_names = list(filter(lambda x: x not in local_mp3_file_basename, original_item_file_names))
    logging.info("************************* Deleting the below unaccounted for files: \n" + pprint.pformat(obsolete_original_item_file_names))
    internetarchive.delete(archive_item.identifier, files=obsolete_original_item_file_names, cascade_delete=True)
    
    logging.info("************************* Now uploading")
    upload_locus_to_local_file_map = dict(zip(local_mp3_file_basename, local_mp3_file_paths))
    filtered_upload_locus_to_local_file_map = dict(filter(lambda item: item[0] not in original_item_file_names, upload_locus_to_local_file_map.items()))
    logging.info(pprint.pformat(filtered_upload_locus_to_local_file_map.items()))
    # checksum=True seems to not avoid frequent reuploads. Archive item mp3 checksum end up varying because of metadata changes? 
    responses = archive_item.upload(filtered_upload_locus_to_local_file_map, verbose=False, checksum=False, verify=False)
    logging.info(zip(local_mp3_file_basename, responses))
    

def fix_metadata():
    for mp3_path in local_mp3_file_paths:
        audiofile = eyed3.load(mp3_path)
        audiofile.tag.artist = ""
        audiofile.tag.album = "महाभारतम् mahAbhAratam"
        audiofile.tag.album_artist = "संस्कृत-स्वयंसेवकाः व्योमसंस्था च"
        audiofile.tag.title = os.path.basename(mp3_path)
        audiofile.tag.save()

def get_author_data():
    import gspread
    # Obtained from https://console.developers.google.com/apis/credentials?project=sanskritnlp
    GOOGLE_KEY = '/home/vvasuki/sysconf/kunchikA/google_service_account_key_sanskritnlp.json'
    SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    from oauth2client.service_account import ServiceAccountCredentials
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_KEY, SCOPES)

    client = gspread.authorize(creds)
    sheet_book = client.open_by_key(SPREADSHEET_ID)
    # Log statements don't seem to work in this function!
    logging.info(sheet_book.worksheets())
    # print(sheet_book.worksheets())
    kaaryaavalii_sheet = sheet_book.worksheet("कार्यावली")
    print(sheet_book.worksheets())
    print(kaaryaavalii_sheet.col_values(col=1))
    print(kaaryaavalii_sheet)
    # logging.info(str(kaaryaavalii_sheet))

get_author_data()
# update_archive_item()