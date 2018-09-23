import subprocess
import logging

github_io_repos = [
    "~/sanskrit/matturu",
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
    logging.info(subprocess.check_output(
        "cd %s; %s" % (repo, 'git commit --allow-empty -m "Force rebuild of site"'),
        stderr=subprocess.STDOUT, shell=True))