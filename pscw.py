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
    removed = 0
    if pc == 'skip':
        return removed

    search_root = "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    # example command: REG Query HLKM lists everything under HKEY_LOCAL_MACHINE
    uninst_list = subprocess.check_output(["PsExec.exe","\\\\+"pc,"-s","cmd",
        "/c","REG","Query",search_root])

    to_search = []

    for line in uninst_list.split('\n'):
        if '{' in line:
            if '}' in line:
                to_search.add(line[len(search_root):])

    removed = 1

    for s in to_search:
        info = subprocess.check_output(["PsExec.exe","\\\\+"pc,"-s","cmd",
            "/c","REG","Query",search_root+s])
        if 'Symantec Endpoint Protection' in info:
            subprocess.call(["msiexec","/X",s]) # "/quiet" to autoremove
            removed = 1
            break

    return removed
