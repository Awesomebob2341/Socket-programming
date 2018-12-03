import socket 
import select 
import time 
import sys 
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print "Correct usage: script, IP address, port number"
    exit()

IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port))

def main():
  
	while True:
		sockets_list = [sys.stdin, server]
		read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
		for socks in read_sockets: 
			if socks == server: 
				message = socks.recv(2048) 
				print message 
			else:
				message = sys.stdin.readline()
				argument = message.split(' ', 1)[0].rstrip()
				
				checkArgument(argument, message)
				
				sys.stdout.flush()
	server.close()


def checkArgument(argument, message):
	validArguments = [
		'login',
		'list',
		'sendto',
		'logout',
		'exit'
	]
	
	if argument == validArguments[0]:
		login(message)
		
	elif argument == validArguments[1]:
		list(message)
		
	elif argument == validArguments[2]:
		sendto(message)
		
	elif argument == validArguments[3]:
		logout(message)
		
	elif argument == validArguments[4]:
		exit(message)
	
	else:
		argument = 'Invalid command'
		print argument


def login(message):
	name = message.split(' ', 1)[1].rstrip()
	if ' ' in name:
		print 'Bad username'
	elif len(name) > 20:
		print 'Bad username'
	else:
		server.send(message)


def list(message):
	cmd = message.split(' ', 1)
	if len(cmd) > 1:
		print 'Invalid command'
	else:
		server.send(message)


def sendto(message):
	cmd = message.split(' ', 2)
	if len(cmd) != 3 or len(cmd[1]) > 20:
		print 'Bad username'
	elif len(cmd[2]) > 65535:
		print 'Bad message'
	else:
		server.send(message)


def logout(message):
	cmd = message.split(' ', 1)
	if len(cmd) > 1:
		print 'Invalid command'
	else:
		server.send(message)


def exit(message):
	cmd = message.split(' ', 1)
	if len(cmd) > 1:
		print 'Invalid command'
	else:
		server.send(message)


main()
