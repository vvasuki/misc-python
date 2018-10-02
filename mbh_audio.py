import subprocess
import logging

# Reference - https://internetarchive.readthedocs.io/en/latest/api.html
import internetarchive
import os
import glob

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s %(message)s"
)

archive_item = internetarchive.get_item("mahAbhArata-mUla-paThanam-GP")
logging.info(archive_item.identifier)

local_repo_path = "/home/vvasuki/mahabharata-audio-2018/"
local_mp3_file_paths = sorted(glob.glob(os.path.join(local_repo_path, "parva*", "mp3", "*.mp3")))
local_mp3_file_basename = list(map(os.path.basename, local_mp3_file_paths))
upload_locus_to_local_file_map = dict(zip(local_mp3_file_basename, local_mp3_file_paths))
logging.debug(upload_locus_to_local_file_map)

original_item_files = list(filter(lambda x: x["source"] == "original" and not x["name"].startswith(archive_item.identifier), archive_item.files))
obsolete_original_item_files = list(filter(lambda x: x["name"] not in local_mp3_file_basename, original_item_files))
obsolete_original_item_file_names = sorted(map(lambda x: x["name"], obsolete_original_item_files)) 
logging.info("************************* Deleting the below unaccounted for files: \n" + "\n".join(obsolete_original_item_file_names))
internetarchive.delete(archive_item.identifier, files=obsolete_original_item_file_names, cascade_delete=True)

logging.info("************************* Now uploading")
responses = archive_item.upload(upload_locus_to_local_file_map, verbose=False, checksum=True, verify=False)
logging.info(responses)


def clear_all():
    internetarchive.delete(archive_item.identifier, glob_pattern="*", verbose=True)
    # logging.info(str(subprocess.check_output(
    #     "ia delete %s --all -H x-archive-keep-old-version:0" % (archive_item.identifier),
    #     stderr=subprocess.STDOUT, shell=True), 'utf-8'))

