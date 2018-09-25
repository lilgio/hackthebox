# Aragog

## Low privilege
Eerst begin ik met een Nmap scan:
``` nmap -sV -p- -T5 -oN 10.10.10.64.nmap```
<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/1.PNG">

Er draait FTP. Misschien is het mogelijk om in te loggen als de anonymous gebruiker, dit kan door de gebruikersnaam anonymous in combinatie met een willekeurige wachtwoord te gebruiken.

<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/2.PNG">
Dit ziet er XML-ish uit. Tot nu toe heb ik er niks aan, maar deze houd ik mijn achterhoofd.

Er draait ook een webserver en de index is een standaard Apache2 pagina. Eens kijken of Dirbuster misschien iets meer kan vinden (Dirsearch deed het raar genoeg niet):
<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/3.PNG">
Eens kijken wat hosts.php te bieden heeft: 

<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/4.PNG">
Heel wazig; er zijn 4294967294 hosts voor.. niks? Als ik de request zie ik eigenlijk ook niets dat misschien verborgen had kunnen zijn. Misschien kan ik de XML-ish spul van net gebruiken om te kijken of dat iets doet:
<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/5.PNG">
Alles tussen de ``subnet`` tags wordt geparsed, eens kijken wat er gebeurt als ik een XXE payload gebruik:
<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/6.PNG">

Vet. Kijken of ik hiermee code execution kan krijgen:
<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/7.PNG">
Oké, dat kan niet. Ik zag toevallig toen ik ``/etc/passwd`` bekeek dat er 2 unieke gebruikers zijn genaamd ``Cliff`` en ``Florian``. Als ik toegang heb tot hun home folders is het misschien wel mogelijk om hun SSH keys weg te plukken.

<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/8.PNG">

Nice, ik heb nu zijn private key. Om deze te gebruiken moet het bestand eerst de goede permissisies hebben, dit kan met de commando ``chmod 600 florian_id_rsa`` en daarna kan ik inloggen als florian met 
``ssh -i florian_id_rsa florian@10.10.10.78``.

<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/9.PNG">

Boom, ez lyfe.

## Privilege escalation

Eerst kijken wat ik allemaal mag uitvoeren als andere gebruikers met de commando ``sudo -l``, maar dan krijg ik een prompt waar ik Florian zijn wachtwoord moet invullen (dat ik niet weet). Dus geen ez root. Als ik naar `/var/www/html` navigeer zie ik een directory die ik eerder niet zag tijdens de Dirbuster scan, deze directory heet `dev_wiki` en bevat een Wordpress website. Wordpress = database credentials.
<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/10.PNG">

Nu kan ik de gehele database bekijken en/of aanpassen. 
<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/11.PNG">
Nu is het een kwestie van de goede database en table kiezen en data om sappige wachtwoorden uit te lezen. Het enige dat ik echter tegen kom is het wachtwoord van de wp-admin. Nu kan ik heel moeilijk doen en deze proberen te bruteforcen, maar ik ben ingelogd als root, dus gewoon lekker aanpassen.
##### Note: Wordpress accepteert ook raw MD5 hashes als wachtwoord.
<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/12.PNG">

Nu is het mogelijk om als administrator in te loggen met het wachtwoord `a`. 
Op de Wordpress website staat er een post met daarin een bericht van Cliff voor Florian:

```
Hi Florian,

Thought we could use a wiki.  Feel free to log in and have a poke around – but as I’m messing about with a lot of changes I’ll probably be restoring the site from backup fairly frequently!

I’ll be logging in regularly and will email the wider team when I need some more testers 😉

Cliff
```
Op dit moment kwam ik erachter dat ik helemaal hoef in te loggen als administrator aangezien ik al een shell heb maar misschien wordt Apache als Cliff gerunned, aangezien hij ook de eigenaar is van alle bestanden in de dev_wiki directory. Om een shell te kunnen uploaden moet ik inloggen als de administrator, dat werkt, en vervolgens een plugin of dergelijke installeren waarmee het mogelijk is om PHP code in pagina's te gebruiken. Dit is in dit geval niet mogelijk omdat ik hiervoor FTP crendentials nodig heb om wijzigingen aan te brengen aan de website.

<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/13.PNG">

Dit gaat dus niet werken. Als ik even niet weet wat ik moet doen doe ik meestal random dingen die nooit gaan werken zoals comments invullen op de blog... 5 minuten later was deze ineens weg. Niemand had de machine gereset... Cronjobs. Om even een goed beeld te krijgen wat er precies gebeurt met de processen op het systeem gebruik ik ``procmon.sh`` dat Ippsec een keer had gebruikt in één van zijn video's.

<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/14.PNG">

`` cp -R /var/www/html/zz_backup/ /var/www/html/dev_wiki/ `` 
Dit is heel interessant, want als ik in /var/www/html kan schrijven is het vast mogelijk om de inhoud van Cliff zijn home folder te bekijken doormiddel van symlinks, aangezien ik denk dat de cronjob wordt gerunned als Cliff. 

<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/15.PNG">
Ik mag de directory aanpassen. De map zz_backup moet nu een symlink naar `/home/cliff` worden, en als de cronjob word gerunned moet alle content van cliff zijn home folder in `dev_wiki` zitten. 

##### Voor de ongeduldige mensen: for i in {1..300}; do echo $i; ls dev_wiki; sleep 1; done

<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/16.PNG">

Heel nice nu kan ik eindelijk zien wat `wp-login.py` doet:

<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/17.PNG">

Oké.. Hij logt even en.. That's it :/. Op dit moment ga ik weer random dingen doen (nog steeds met de gedachte dat de cronjob als Cliff wordt gerunned). Ook al wist ik dat het niet mogelijk was liet ik de symlink verwijzen naar  ` /root/` om vervolgens te kijken wat er zal gebeuren.

<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/20.PNG">

Tot mn verbazing zie ik root.txt en is de box klaar ¯\_(ツ)_/¯. 

<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/18.PNG">

Blijkbaar ben ik slecht in verbanden trekken aangezien de file letterlijk `restore.sh` heet en zich bevindt in `/root`  (zoals je kon zien in procmon.sh). Werd op een dwaalspoor gebracht omdat de file owner Cliff was en had er niet aan gedacht dat root dat ook kan doen.
 
<img src="https://raw.githubusercontent.com/lilgio/hackthebox/master/images/aragog/19.PNG">
