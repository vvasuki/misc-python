import logging
import subprocess


# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s")

github_io_repos = [
    "~/sanskrit/groups",
    "~/sanskrit/projects",
    "~/sanskrit/people",
    "~/sanskrit-coders/site",
    "~/sanskrit-coders/sanskrit-data",
    "~/vvasuki-git/notes",
    "~/vvasuki-git/site",
    "~/xetram/rekhaa-catering",
    "~/hindutva/site",
]

for repo in github_io_repos:
    logging.info(str(subprocess.check_output(
        "cd %s; %s" % (repo, 'git commit --allow-empty -m "Force rebuild of site"'),
        stderr=subprocess.STDOUT, shell=True), 'utf-8'))