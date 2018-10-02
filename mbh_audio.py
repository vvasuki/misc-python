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
mp3_file_paths = sorted(glob.glob(os.path.join(local_repo_path, "parva*", "mp3", "*.mp3")))
mp3_file_basename = list(map(os.path.basename, mp3_file_paths))
upload_locus_to_local_file_map = dict(zip(mp3_file_basename, mp3_file_paths))
logging.debug(upload_locus_to_local_file_map)

def clear_all():
    internetarchive.delete(archive_item.identifier, glob_pattern="*", verbose=True)
    # logging.info(str(subprocess.check_output(
    #     "ia delete %s --all -H x-archive-keep-old-version:0" % (archive_item.identifier),
    #     stderr=subprocess.STDOUT, shell=True), 'utf-8'))

responses = archive_item.upload(upload_locus_to_local_file_map, verbose=False, checksum=True, verify=False)
logging.info(responses)
