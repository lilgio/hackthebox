# Stratosphere

## Low privilege

Eerst begin ik met een Nmap scan

``` nmap -sV -p- -T5 -oN 10.10.10.64.nmap```

<img src="https://github.com/lilgio/hackthebox/blob/master/images/stratosphere/1.PNG" />

<ul>
	<li>sV: Probeer versie namen te vinden</li>
	<li>-p-: Scan alle TCP poorten </li>
	<li>-T5: Scan snel en aggresief</li>
	<li>-oN: Save output als Nmap formaat </li>
</ul>

