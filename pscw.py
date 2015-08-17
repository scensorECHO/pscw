import sys
import os
import subprocess
import time

# Set process link to PsExec
pse = "C:\\Users\\Carrio\\Documents\\PsTools\\PsExec.exe"

with open('computerlist', 'r') as computerlist:
    pcs = computerlist.read().split('\n')

def searchRegistry(pc="skip"):
    if 'skip' in pc:
        return 0

    search_root = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\"
    # example command: REG Query HLKM lists everything under HKEY_LOCAL_MACHINE
    uninst_list = subprocess.check_output([pse,"\\\\"+pc,"-s","cmd","/c","REG",
        "Query",search_root])

    to_search = []

    for line in uninst_list.split('\n'):
        if '{' in line:
            if '}' in line:
                to_search.append(line[len(search_root):])

    for s in to_search:
        info = subprocess.check_output([pse,"\\\\"+pc,"-s","cmd",
            "/c","REG","Query",search_root+s])
        if 'Symantec Endpoint Protection' in info:
            killMsiExec(pc)
            subprocess.call([pse,"\\\\"+pc,"-s","cmd","/c","msiexec","/X",s,
                "/quiet"]) # "/quiet" to autoremove
            return 1 # MSI uninstall key found and executed

    return 0 # Symantec uninstall key not found

def killMsiExec(pc="skip"):
    if pc == "skip":
        return 0
    status = subprocess.check_output([pse,"\\\\"+pc,"taskkill","/IM",
        "MsiExec.exe","/F"])
    if "SUCCESS" in status:
        return 1
    else:
        return 0

# execute script on all PCs
for e in pcs:
    if searchRegistry("W2UA4391VL9"):
         print("hooray")

print "Success"
time.sleep(5)
