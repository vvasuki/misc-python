import subprocess
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s %(message)s"
)
github_io_repos = [
    "~/sanskrit/groups",
    "~/sanskrit/projects",
    "~/sanskrit/people",
    "~/sanskrit-coders/site",
    "~/vvasuki-git/notes",
    "~/vvasuki-git/site",
    "~/xetram/rekhaa-catering",
    "~/sanskrit/people",
    "~/hindutva/site",
]

for repo in github_io_repos:
    logging.info(str(subprocess.check_output(
        "cd %s; %s" % (repo, 'git commit --allow-empty -m "Force rebuild of site"'),
        stderr=subprocess.STDOUT, shell=True), 'utf-8'))