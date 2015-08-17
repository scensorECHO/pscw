import sys
import os
import subprocess
# import time

# Set working directory to PsTools dir
try:
    os.chdir(open('psloc', 'r').readline().strip())
except IOError:
    sys.exit("PsTools directory was not opened correctly")


with open('computerlist', 'r') as computerlist:
    pcs = computerlist.read().split('\n')

def searchRegistry(pc='skip'):
    if pc == 'skip':
        return 0

    search_root = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\"
    # example command: REG Query HLKM lists everything under HKEY_LOCAL_MACHINE
    uninst_list = subprocess.check_output(["PsExec.exe","\\\\+"pc,"-s","cmd",
        "/c","REG","Query",search_root])

    to_search = []

    for line in uninst_list.split('\n'):
        if '{' in line:
            if '}' in line:
                to_search.append(line[len(search_root):])

    for s in to_search:
        info = subprocess.check_output(["PsExec.exe","\\\\+"pc,"-s","cmd",
            "/c","REG","Query",search_root+s])
        if 'Symantec Endpoint Protection' in info:
            subprocess.call(["msiexec","/X",s,"/quiet"]) # "/quiet" to autoremove
            return 1 # MSI uninstall key found and executed

    return 0 # Symantec uninstall key not found

# execute script on all PCs
# for pc in pcs:
#     searchRegistry(pc)
