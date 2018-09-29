# Sunday

## Low privilege
Eerst begin ik met een Nmap scan:
``` nmap -sV -p- -T5 -oN 10.10.10.64.nmap```
<img src="https://github.com/lilgio/hackthebox/blob/master/images/sunday/1.PNG" />

Eerlijk gezegd heb ik geen idee wat dit allemaal is / kan zijn. `RPCbind` zal wel iets met shares zijn. Dit is een rabbit hole. Wat is `finger` tho?  Google zegt letterlijk dat het een user enumeration protocol is, dus ff kijken of Metasploit iets hiervoor heeft.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/sunday/2.PNG" />

Op basis van logica pak ik de tweede en vul ik alle info van Sunday in.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/sunday/3.PNG" />

Normaal gesproken zou er nog een user bij moeten staan genaam `sunny` maar om een of andere staat hij er op dit moment niet bij. Na eindeloos enumeraten en creatief na te hebben gedacht doe ik mn laatste red middel: Bruteforcen. En blijkbaar werkt dit, want sunny zijn wachtwoord is gewoon sunday.. 
Dit is de commando dat ik heb gebruikt: `hydra -l sunny -P ~/rockyou.txt sunday.htb ssh -V -I`

<img src="https://github.com/lilgio/hackthebox/blob/master/images/sunday/4.PNG" />

Eenmaal ingelogd als Sunny run ik altijd als eerst `sudo -l`. Hierin staat dat ik `/root/troll` als root mag uitvoeren zonder wachtwoord. Het enige dat hier gebeurt is dat de commando `id` wordt uitvevoerd.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/sunday/5.PNG" />

Hier heb ik niet veel aan dus kijk ik verder. Na een tijdje te hebben rond gesnuffeld kwam ik iets moois tegen een `/backup`namelijk een backup van de shadow file.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/sunday/6.PNG" />

Het hash algoritme dat Unix gebruikt is sha256-crypt (so naar hash-identifier). Eens kijken of `john` het wachtwoord van `sammy` misschien kan kraken.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/sunday/7.PNG" />

Fijn. Nu kan ik inloggen als sammy met het wachtwoord `cooldude!`.

## Privesc

Wanneer ik `sudo -l ` uitvoer kan ik zien dat ik wget mag uitvoeren als root zonder wachtwoord. Ik ben er nog niet helemaal achter hoe ik dit kan gebruiken om het systeem te exploiten, maar ben ervan bewust dat ik dit moet gebruiken om te privescen. Wanneer ik `ps aux` uitvoer zie ik iets opvallends.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/sunday/8.PNG" />

Op dit moment had ik een manier gevonden om root te worden. Ik wilde `/root/troll` (die ik mag uitvoeren als root als sunny) overschrijven met een shell doormiddel van wget. Eerst eens kijken of dit werkt en daarna kijk ik verder naar de output van ps aux. Ik maak een simpel Bash scriptje met daarin `whoami`, als ik nu als sunny `/root/troll` uitvoer zou ik als output `root` moeten zien en niets anders.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/sunday/9.PNG" />

Als ik nu inlog als Sunny en `/root/troll`uitvoer zou ik root moeten zien.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/sunday/10.PNG" />

Dit is vreemd aangezien ik dit als root uitvoer en root mag /root/troll overschrijven. Dit is dan ook de reden waarom ik denk dat ik weet wat `/root/overwrite` doet in combinatie met `/usr/gnu/bin/sleep 5`. Ik denk namelijk dat /root/troll elke 5 seconden weer wordt restored. 5 seconden is traag voor een computer :).  Eerst weer met de user `sammy` /root/troll overschrijven doormiddel van wget. Ik ga nu hetzelfde proberen alleen laat ik de user `sunny` /root/troll elke seconde utivoeren om te kijken of ik gelijk heb.

<img src="https://github.com/lilgio/hackthebox/blob/master/images/sunday/11.PNG" />

Dit is dus inderdaad wat er precies gebeurd. Het enige dat ik nu moet doen is een python shell in het bash scriptje doen (nc is niet geïnstalleerd).

<img src="https://github.com/lilgio/hackthebox/blob/master/images/sunday/12.PNG" />

Hierdoor is het mogelijk om python uit te voeren in een Bash omgeving. Als ik nu hetzelfde trucje doe als net moet ik nu wel een root shell krijgen.
