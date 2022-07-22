import subprocess
import json
import argparse
from os.path import exists

def create_settings_json():
    f = open('settings.json', 'w')
    settings_table = [
        "--style=break",
        "--indent=spaces=2",
        "--pad-oper",
        "--pad-paren-in",
        "--pad-header",
        "--pad-excludes=TEXT|_T|RETAILMSG|DEBUGMSG|R_TRACE|D_TRACE|R_ASSERT|D_ASSERT|R_TRACE_METHOD|D_TRACE_METHOD|return",
        "--break-closing-brackets",
        "--add-brackets",
        "--convert-tabs",
        "--align-pointer=type",
        "--align-reference=type",
        "--keep-one-line-blocks",
        "--max-instatement-indent=80"
    ]
    data={"astyle_cmd_options":settings_table}
    json.dump(data, f, indent=4)
    f.close()

def create_path(path_name, path=0):
    if(path == 0):
        if (path_name == "astyle_exe_path"):
            print("Paste path to your AStyle.exe (For example: .\AStyle\AStyle.exe or C:\AStyle\AStyle.exe)")
        elif (path_name == "repo_path"):
            print("Paste path to your local repository")
        else:
            print("Paste path to " + path_name)
        path = input()

    json_string = {path_name:path}

    with open('settings.json') as f:
        json_file = json.load(f)

    json_file.update(json_string)

    with open('settings.json', 'w') as f:
        json.dump(json_file, f, indent=4)
    return(path)

def check_settings(settings, config):
    if ("astyle_exe_path" not in settings.keys()):
        if(config["source"]):
            settings.update( { "astyle_exe_path":create_path("astyle_exe_path", config["source"]) } )
        else:
            settings.update({"astyle_exe_path":create_path("astyle_exe_path")})

    if ("repo_path" not in settings.keys()):
        if(config["destination"]):
            settings.update({"repo_path":create_path("astyle_exe_path", config["destination"])})
        else:
            settings.update({"repo_path":create_path("repo_path")})
    
astyle_cmd_options = ""
git_output_filtered = []
file_paths = []

parser = argparse.ArgumentParser(description="Just an example", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-s", "--source", type=str, help="path to AStyle.exe")
parser.add_argument("-d", "--destination", type=str, help="path to local repository")
args = parser.parse_args()
config = vars(args)

if(not exists('settings.json')):
    create_settings_json()
    
f = open('settings.json')
settings = json.load(f)
f.close()

check_settings(settings, config)

for i in settings['astyle.cmd_options']:
    astyle_cmd_options += " " + i

astyle_exe_path = settings["astyle_exe_path"]
repo_path = settings["repo_path"]

git_output = subprocess.check_output("git status", cwd=repo_path).decode().replace(" ", "").split()
git_output = [i for i in git_output if 'modified' in i]

for i in git_output:
    if ".h" in i:
        git_output_filtered.append(i.replace("modified:", "/"))
    if '.cpp' in i:
        git_output_filtered.append(i.replace("modified:", "/"))
    if '.hpp' in i:
        git_output_filtered.append(i.replace("modified:", "/"))

for i in git_output_filtered:
    file_paths.append(repo_path + i)

for i in file_paths:
    subprocess.run(astyle_exe_path + astyle_cmd_options + " " + i)