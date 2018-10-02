import logging
import pprint
# Reference - https://internetarchive.readthedocs.io/en/latest/api.html
import internetarchive
import os
import glob

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s %(message)s"
)

def update_archive_item():
    archive_item = internetarchive.get_item("mahAbhArata-mUla-paThanam-GP")
    logging.info(archive_item.identifier)
    
    local_repo_path = "/home/vvasuki/mahabharata-audio-2018/"
    local_mp3_file_paths = sorted(glob.glob(os.path.join(local_repo_path, "parva*", "mp3", "*.mp3")))
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
    
update_archive_item()