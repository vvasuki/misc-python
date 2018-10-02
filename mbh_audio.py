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
SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SPREADSHEET_RANGE_KARYAAVALII = 'Class Data!A2:E'
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
    from googleapiclient.discovery import build
    from oauth2client import file, client, tools
    from httplib2 import Http
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    store = file.Storage('local_token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/home/vvasuki/sysconf/kunchikA/google_sheets_credentials_sanskritnlp.json', SCOPES)
        creds = tools.run_flow(flow, store)
    # Added cache_discovery=False following online tip to resolve some error. But this leads to an empty result.
    service = build('sheets', 'v4', http=creds.authorize(Http()), cache_discovery=False)

    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=SPREADSHEET_RANGE_KARYAAVALII).execute()
    logging.info(str(result))
    kaaryaavalii_values = result.get('values', [])
    logging.info(kaaryaavalii_values)
    logging.info(pprint.pformat(kaaryaavalii_values))

get_author_data()
# update_archive_item()