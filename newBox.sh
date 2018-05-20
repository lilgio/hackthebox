#!/bin/bash

boxName=$1;
IP=$2;
dir=$1-$2;
rootdir="/root/hackthebox";

function empty {
	if [[ $(echo $1 | wc -m) == 1 ]]; then
		echo "Usage: ./newHTB.sh [boxname] [IP address]";
		exit;
	fi
}

function dirCheck {
	if [ -d $1 ]; then
		mkdir -p $rootdir;
	fi
}

empty "$boxName";
empty "$IP";
dirCheck "$rootdir";

echo "[+] Doing this manually would probably more efficient, but if you just want to scan and watch some Netflix this is your thang";

echo "[+] Building new directory";

cd $rootdir;
mkdir $dir;
echo "[+] Navigating to $dir";
cd $dir;
touch logs;
echo "[+] Adding $boxName.htb to /etc/hosts";
echo "$IP $boxName.htb" >> /etc/hosts;
echo "[+] Starting Nmap scan..";
nmap -sV -p- -T5  -v $IP -oN $IP.nmap;
echo "[+] Testing if a webserver is running on port 80";

if [[ $(curl -Is http://$boxName.htb | grep HTTP/1.1 | awk {'print $2'}) == 200 ]]; then
	echo "[+] Starting simple dirb scan";
	dirb http://$boxName.htb > dirb.out;
else
	echo "[+] $IP doesn't seem to have a webserver on port 80";
fi

