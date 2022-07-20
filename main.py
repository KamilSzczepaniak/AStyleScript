import subprocess
import json

astyle_cmd_path = "./AStyle/AStyle.exe"
astyle_cmd_options = ""
repo_path = "C:/Users/kamil.szczepaniak/source/repos/security"
results_filtered = []
file_paths = []


results = subprocess.check_output("git status", cwd=repo_path).decode().replace(" ", "").split()
results = [i for i in results if 'modified' in i]

for i in results:
    if ".h" in i:
        results_filtered.append(i.replace("modified:", "/"))
    if '.cpp' in i:
        results_filtered.append(i.replace("modified:", "/"))

for i in results_filtered:
    file_paths.append(repo_path + i)

f = open('settings.json')
data = json.load(f)

for i in data['astyle.cmd_options']:
    astyle_cmd_options += " " + i

for i in file_paths:
    subprocess.run(astyle_cmd_path + astyle_cmd_options + " " + i)