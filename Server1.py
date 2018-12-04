import socket 
import select 
import sys 
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit()

IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2])
server.bind((IP_address, Port))

server.listen(10)
list_of_clients = [] 

print ('Server online')

def clientthread(conn, addr):
	
    	conn.send("Welcome! Please sign in to chat."+
    			"\nExample: login <username>") 
  
    	while True:
        	try:
		            message = conn.recv(2048)
		            if message:
		            	
		            	for clients in list_of_clients:
		            		if clients[0] == conn:
		            			sender = clients
		            			
		            	recipient = sender
		            	command = message.split(' ', 1)[0].rstrip()
		            	
		            	if command == 'login':
		            		name = message.split(' ', 1)[1].rstrip()
		            		
		            		if usernameValid(name) == True:
		            			sender[2] = name
		            			newMessage = 'Welcome to the chat room ' + sender[2] + '.'
		            			             
		            		else:
		            			newMessage = 'Bad username. ' + name + ' is in use.'
		            		conn.send(newMessage)
		            	
		            	elif command == 'list':
		                        if sender[2] == '':
		                            newMessage = 'You need to login to view other users'
		                                        
		                        elif sender[2] != '':
		                            newMessage = 'Online users:\n'
		                            for clients in list_of_clients:
		                                if clients[2] != '':
		                                    newMessage = newMessage + clients[2] + '\n'
		                                else:
		                                    newMessage = newMessage
		                                                        
		                        conn.send(newMessage)

		            	elif command == 'sendto':
		                        if sender[2] == '':
		                            newMessage = 'You need to login to send messages'
		                                        
		                        elif sender[2] != '':
		                            name = message.split(' ', 2)[1].rstrip()
		                            for client in list_of_clients:
		                                if client[2] == name:
		                                                recipient = client
		                            if recipient[2] != sender[2]:
		                                newMessage = sender[2] + ' >> ' + message.split(' ', 2)[2].rstrip()
		                                sendMessage(sender, recipient, newMessage)
		                            elif recipient[2] == sender[2]:
		                                newMessage = 'User not logged in'
		                                conn.send(newMessage)
		                                
		                elif command == 'logout':
		                	newMessage = 'Loggin out'
					try:
						sender[0].send(newMessage) # Notify the user they've logged out
						sender[2] = ''		   # Set the users name to empty 
					except:
						sender[2] = ''
						sender[0].close()
						remove(connection)
		                
		                elif command == 'exit':
		                	newMessage = 'Exiting program'
					
					try:
						sender[0].send(message)
						sender[2] = ''
						sender[0].close()
						remove(connection)
					except:
						sender[2] = ''
						sender[0].close()
						remove(connection)		            		
		            else:
		                remove(conn)
  
        	except: 
                	continue


def usernameValid(name):
	count = 0
	
	for clients in list_of_clients:
            if name == clients[2]:
                    count += 1
			
	if count > 0:
	    return False
	else:
	    return True


def sendMessage(sender, recipient, message):
	if sender[0] != recipient[0]:
		try:
			recipient[0].send(message)
		except:
			recipient.close()
			remove(recipient)


def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection and clients[2] != '': 
            try: 
                clients.send(message) 
            except: 
                clients.close()
                remove(clients) 
  

def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection)
 

while True:
	conn, addr = server.accept()
	list_of_clients.append([conn,addr,''])
	print addr[0] + ' Established connection'
	start_new_thread(clientthread,(conn,addr))

conn.close() 
server.close() 
