import itertools
import logging
import os.path
import shutil
import subprocess

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
  logging.root.removeHandler(handler)
logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s")

website_repos = {
  "hindutva": ["hindutva.github.io", "mantra-manuals", ],
  "become-hindu": ["become-hindu.github.io",  ],
  "sanskrit": ["sanskrit.github.io", ],
  "sanskrit-coders": ["sanskrit-coders.github.io"] ,
  "vishvAsa": ["notes", "vishvAsa.github.io", "AgamaH", "jyotiSham", "mImAMsA", "rahaShTippanyaH", "vedAH_Rk", "bhAShAntaram", "kalpAntaram", "notes", "sanskrit", "vedAH_sAma", "devaH", "kannaDa", "pALi", "tipiTaka", "vedAH_yajuH", "vishvAsa.github.io"],
  "vvasuki-git": ["vvasuki.github.io"]
}

reg_repos = {
  "sanskrit-coders": ["sanskrit_data", "autokey-scripts_sa", "db-interface", "chandas", "audio_utils", 
                      "sanskrit_data", "video_curation", "audio_curation", 
                      "curation_utils", "autokey-scripts_sa", 
                      "rss-feeds", "doc_curation", ],
  "sanskrit": ["ashtadhyayi_com_transforms", "raw_etexts_private", "telugu-texts",  "raw_etexts", "sanskrit-documents-dump",  "raw_etexts_english" ],
  "indic-dict": ["stardict-sanskrit", "stardict-tibetan", "stardict-test", "stardict-index", "stardict-english", "stardict-sanskrit-vyAkaraNa", "stardict-sanskrit-kAvya", "stardict-hindi", "stardict-dictionary-updater", "stardict-sanskrit-student", "stardict-telugu", "stardict-malayalam", "stardict-pali", "stardict-ayurveda", "stardict-marathi", "stardict-tamil", "stardict-gujarati", "stardict-oriya", "stardict-bengali", "stardict-assamese", "stardict-panjabi", "stardict-sinhala", "stardict-prakrit", "stardict-kashmiri", "stardict-kannada", "stardict-divehi", "stardict-nepali", "stardict-urdu", "stardict-indic-update-aur", "StarDict-1", "SanskritDictionariesInstaller", "stardict", "jstardict", "sanDict", "pystardict", "dict-tools", "dict-curation", "indic-dict.github.io", "dsal-scraper", "osx-sanskrit", ],
  "indic-transliteration": ["indic_transliteration_py", "m17n-db-indic",  "sanskrit-fonts", "indic_transliteration_scala",  "sanscript.js"],
  "vvasuki-git": ["buildings", "jananANu", "misc-scala", "sysconf", 
                  "furniture", "misc-c", "rahah", "vlc-addons", 
                  "health", "misc-perl", "rahah-rare", 
                  "html-to-markdown", "misc-python", "step-install-packages", ]
}

GIT_BASE = "/home/vvasuki/gitland"


def force_site_rebuild():
  for group, repos in website_repos.items():
    for repo in repos:
      repo_path = os.path.join(GIT_BASE, group, repo)
      logging.info(str(subprocess.check_output(
        f'cd {repo_path} git commit --allow-empty -m "Force rebuild of site"',
        stderr=subprocess.STDOUT, shell=True), 'utf-8'))


def run_command_in_submodule_repos(command, sub_dirs=None):
  for dir in os.listdir(GIT_BASE):
    full_path = os.path.join(GIT_BASE, dir)
    for sub_dir in os.listdir(full_path):
      if sub_dirs is not None and sub_dir not in sub_dirs:
        continue
      logging.info(f"Processing {full_path}")
      # if sub_dir in ["tipiTaka"]:
      #   logging.info(f"Skipping {sub_dir}")
      #   continue
      full_path = os.path.join(GIT_BASE, dir, sub_dir)
      if not os.path.exists(os.path.join(full_path, ".gitmodules")):
        continue
      logging.info(str(subprocess.check_output(
        f"cd {full_path}; {command}",
        stderr=subprocess.STDOUT, shell=True), 'utf-8'))


def pull_all(sub_dirs=None):
  command = "git pull --recurse-submodules"
  run_command_in_submodule_repos(command=command, sub_dirs=sub_dirs)

def fsck_all(sub_dirs=None):
  command = "git fsck"
  run_command_in_submodule_repos(command=command, sub_dirs=sub_dirs)

def unshallow_all(sub_dirs=None):
  command = "git submodule foreach -q --recursive 'git fetch --unshallow'"
  run_command_in_submodule_repos(command=command, sub_dirs=sub_dirs)

def set_submodule_branches(sub_dirs=None):
  command = "git submodule foreach -q --recursive 'git checkout -b $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master) || git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master)'"
  run_command_in_submodule_repos(command=command, sub_dirs=sub_dirs)
  command = "git submodule foreach -q --recursive 'git branch --set-upstream-to=origin/$(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master) || git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master)'"
  run_command_in_submodule_repos(command=command, sub_dirs=sub_dirs)


def reclone_all_with_submods():
  for dir in os.listdir(GIT_BASE):
    full_path = os.path.join(GIT_BASE, dir)
    if dir in ["vishvAsa", "sanskrit-coders"]:
      logging.info(f"Skipping {full_path}")
      continue
    # if not dir in []:
    #   logging.info(f"Skipping {full_path}")
    #   continue
    sub_dirs = list(os.listdir(full_path))
    if dir in ["vishvAsa"]:
      sub_dirs = list(itertools.dropwhile(lambda x: x!="vedAH_Rk", sub_dirs))
    for sub_dir in sub_dirs:
      full_path = os.path.join(GIT_BASE, dir, sub_dir)
      if sub_dir in ["rahaShTippanyaH", "raw_etexts"] or not os.path.exists(os.path.join(full_path, ".gitmodules")):
        logging.info(f"Skipping {full_path}")
        continue
      logging.info(f"Processing {full_path}")
      os.chdir(full_path)
      origin_url = subprocess.run("git config --get remote.origin.url", capture_output=True, text=True, shell=True).stdout.strip()
      os.chdir(os.path.dirname(full_path))
      full_path_tmp = os.path.join(GIT_BASE, dir, sub_dir + "_tmp")
      shutil.rmtree(full_path_tmp, ignore_errors=True)
      clone_repo(origin_url, os.path.basename(full_path_tmp))
      for f in os.listdir(full_path):
        if str(f).split(".")[-1] in ["ipr", "iml", "iws"]:
          shutil.copy(os.path.join(full_path, f), full_path_tmp)
      logging.info(str(subprocess.check_output(
        f"rm -rf {full_path}; mv {full_path_tmp} {full_path}",
        stderr=subprocess.STDOUT, shell=True), 'utf-8'))


def clone_repo(origin_url, dest_path):
  command = f"git clone --recurse-submodules -b master {origin_url} {dest_path}"
  logging.info(str(subprocess.check_output(
    command,
    stderr=subprocess.STDOUT, shell=True), 'utf-8'))


def clone_all_with_submods(groups=None, repos=None):
  def _clone_all_in_dict(repo_dict):
    for group, repos in repo_dict.items():
      if groups is not None and group not in groups:
        continue
      for repo in repos:
        if repos is not None and repo not in repos:
          continue
        full_path = os.path.join(GIT_BASE, group, repo)
        origin_url = f"https://github.com/{group}/{repo}.git"
        if group == "vvasuki-git":
          full_path = full_path.replace("gitland/vvasuki/", "gitlandl/vvasuki-git/")
          origin_url = origin_url.replace("-git", "")
        if os.path.exists(full_path):
          logging.info("Skipping " + full_path)
          continue
        clone_repo(origin_url=origin_url, dest_path=full_path)
  _clone_all_in_dict(repo_dict=website_repos)
  _clone_all_in_dict(repo_dict=reg_repos)


if __name__ == '__main__':
  pass
  # set_submodule_branches(sub_dirs=["raw_etexts"])
  # set_submodule_branches()
  clone_all_with_submods()
  # fsck_all()
  # pull_all()
  # reclone_all_with_submods()
  # unshallow_all()
  # reclone_all()