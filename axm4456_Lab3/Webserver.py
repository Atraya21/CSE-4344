# -*- coding: utf-8 -*-
# Leave a comment wherever you see a hashtag in order to explain
# the program’s behavior.  Comments for parsing the requested
# file are left in the program, as that’s tertiary to the basic
# functionality of the program
#Atraya Mukherjee
#1001144456
#CSE 4344
#lab3


# importing the socket library
from socket import * 
import sys # In order to terminate the program

# create a TCP serversocket instance and pass it two parameters ;AF_INET refers to the address protocol ipv4. The SOCK_STREAM means connection oriented TCP protocol
serverSocket = socket(AF_INET, SOCK_STREAM)

# reserving a port
# connect to web server on port 4456(last 4 digits of netID)  ; if not done, it will go to port number 80
serverPort = 4456

# bind to the socket to server address and server port
#the address field is left empty as it makes the server listen to requests coming from other computers on the network
serverSocket.bind(("", serverPort))

# put the socket in listening mode, listen to at most 1 conneciton at a time
serverSocket.listen(1)

while True:
	print('The server is ready to receive')

	# establish connection with client
	connectionSocket, addr = serverSocket.accept()

# try to display the contents of html file if there exists one, otherwise display the error message on the client
# try clause is executed , if exception is caused it is skipped
# if exceptions matched except , except clause is executed
	try:
		# receives the request message from the client
		message = connectionSocket.recv(1024).decode()
		
		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
		filename = message.split()[1]
		
		# Because the extracted path of the HTTP request includes 
		# a character '\', we read the path from the second character 
		f = open(filename[1:])
		
		# reading the file and setting ouputdata(temporary buffer) as the contents read 
		outputdata = f.read()
		
		# send the HTTP response header line to the conneciton socket
		connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode()) 
 
		# send the contents of the requested file to the connection socket
		for i in range(0, len(outputdata)):  
			connectionSocket.send(outputdata[i].encode())
		connectionSocket.send("\r\n".encode()) 
		
		# close the client connection socket
		connectionSocket.close()

	except IOError:
			# send the HTTP response message for file not found
			connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
			connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

			# close the client connection socket
			connectionSocket.close()

#close the server socket
serverSocket.close()  

#Exit form python; raises the SystemExit exception
sys.exit()
