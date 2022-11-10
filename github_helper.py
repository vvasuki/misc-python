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

github_io_repos = [
  "sanskrit/groups",
  "sanskrit/projects",
  "sanskrit/people",
  "sanskrit-coders/site",
  "sanskrit-coders/sanskrit-data",
  "xetram/rekhaa-catering",
  "hindutva/site",
]

github_io_repos_vishvaasa = ["note", "site", "AgamaH", "jyotiSham", "mImAMsA", "rahaShTippanyaH", "vedAH_Rk", "bhAShAntaram", "kalpAntaram", "notes", "sanskrit", "vedAH_sAma", "devaH", "kannaDa", "pALi", "tipiTaka", "vedAH_yajuH", "vvasuki.github.io"]


GIT_BASE = "/home/vvasuki/gitland"


def force_site_rebuild():
  for repo in github_io_repos:
    repo_path = os.path.join(GIT_BASE, repo)
    logging.info(str(subprocess.check_output(
      f'cd {repo_path} git commit --allow-empty -m "Force rebuild of site"',
      stderr=subprocess.STDOUT, shell=True), 'utf-8'))


def run_command_in_submodule_repos(command):
  for dir in os.listdir(GIT_BASE):
    full_path = os.path.join(GIT_BASE, dir)
    for sub_dir in os.listdir(full_path):
      logging.info(f"Processing {full_path}")
      if sub_dir in ["rahaShTippanyaH"]:
        logging.info(f"Skipping {sub_dir}")
        continue
      full_path = os.path.join(GIT_BASE, dir, sub_dir)
      if not os.path.exists(os.path.join(full_path, ".gitmodules")):
        continue
      logging.info(str(subprocess.check_output(
        f"cd {full_path}; {command}",
        stderr=subprocess.STDOUT, shell=True), 'utf-8'))


def pull_all():
  command = "git pull --recurse-submodules"
  run_command_in_submodule_repos(command=command)

def unshallow_all():
  command = "git submodule foreach -q --recursive 'git fetch --unshallow'"
  run_command_in_submodule_repos(command=command)

def set_submodule_branches():
  command = "git submodule foreach -q --recursive 'git checkout -b $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master) || git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master)'"
  run_command_in_submodule_repos(command=command)
  command = "git submodule foreach -q --recursive 'git branch --set-upstream-to=origin/$(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master) || git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master)'"
  run_command_in_submodule_repos(command=command)


def reclone_all_with_submods():
  for dir in os.listdir(GIT_BASE):
    full_path = os.path.join(GIT_BASE, dir)
    if not dir in ["vishvAsa"]:
      logging.info(f"Skipping {full_path}")
      continue
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
      command = f"git clone --recurse-submodules {origin_url} {os.path.basename(full_path_tmp)}"
      logging.info(str(subprocess.check_output(
        command,
        stderr=subprocess.STDOUT, shell=True), 'utf-8'))
      for f in os.listdir(full_path):
        if str(f).split(".")[-1] in ["ipr", "iml", "iws"]:
          shutil.copy(os.path.join(full_path, f), full_path_tmp)
      logging.info(str(subprocess.check_output(
        f"rm -rf {full_path}; mv {full_path_tmp} {full_path}",
        stderr=subprocess.STDOUT, shell=True), 'utf-8'))


if __name__ == '__main__':
  set_submodule_branches()
  # pull_all()
  # reclone_all_with_submods()
  # unshallow_all()
  # reclone_all()