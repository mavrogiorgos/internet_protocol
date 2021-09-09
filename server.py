# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 10:23:48 2021

@author: kostis mavrogiorgos
"""

#Import the socket library
from struct import *
import socket
import binascii
import random

#Host IP to listen to. If '' then all IPs in this interface
serverIP = ''
#Port to listen to
serverPort = 12345
#Flag to close the socket. Normally we don't close the socket. We keep on listening. 
#This flag is used to simply terminate the program and close the socket as we don't need it after
#the message exchange
close = False

#create list of information type that the server needs.
#this list is created so that the server can request random info
#and also know what the client has sent to it.
info_list = [0, 1, 2]

#in this list are saved all the information received by the client
info_received = {}

#Create the server socker
#socket.AF_INET == IPv4
#socket.SOCK_STREAM == TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    #Bind the socket
    serverSocket.bind((serverIP, serverPort))
    print ("The server is ready to receive at port", str(serverPort))
    #Listen for connections
    #If we don't specify in the listen a number e.g. serverSocket.listen(5), it goes to the system default
    serverSocket.listen()
    #Listen and wait for connection
    #Once a connection is made it returns two values, the conn will have the connection socket and the addr will have the address
    conn, addr = serverSocket.accept()
    #In a normal server, there are three ways to handle incoming requests:
    #1. Create a new thread to handle this request and the program would keep on listening 
    #2. Create a new process to handle this request
    #3. Use non-blocking sockets and multiplex using selectors.
            
    #Print info: Connected address, Server IP & Port, Client IP & Port
    print("Connected by:", addr)
    print("Server Socket port: ", conn.getsockname())
    print("Client Socket port: ", conn.getpeername())
    while not close:
        

        #Handle the request
        #Receive the 4st four bytes
        msg = conn.recv(4)
        msg_type,msg_am = unpack('HH', msg)
        if(msg_type==0):
            #Now we know the total message and the type
            print('AM received is: '+str(msg_am))
            #check if AM is valid and if yes request full name
            if(len(str(msg_am))== 5 and str(msg_am).isnumeric()):
                #save AM into info_received
                info_received["AM"]= msg_am
                
                msg_information_type = random.choice(info_list)
                info_list.remove(msg_information_type)
                server_msg_type = 1
                
                #Now it's time to pack our response.
                message = pack('HH', server_msg_type, msg_information_type)
                #Send the message through the same connection
                err = conn.sendall(message)  
            else:
                server_msg_type = 5
                #message type 1 because AM is not consistent
                msg_information_type = 1
                #Now it's time to pack our response.
                message = pack('HH', server_msg_type, msg_information_type)
                #Send the message through the same connection
                err = conn.sendall(message)
                #Signal (with the flag) to close the socket
                close=True
                #And closing
                conn.close()
                serverSocket.close()
            
            
        elif(msg_type==2):
            total_message_length = msg_am
            #Receive the other 6 bytes
            msg = conn.recv(6)
            print(msg)
            am,padding1,firstname_length = unpack('HHH', msg)
            print('AM is: ' +str(am))
            print("Padding1 is: "+str(padding1))
            print('Total message length without pad='+str(total_message_length))
            print('Firstname length without pad='+str(firstname_length))
            #I need to find the firstname padding
            firstname_padSize=(4 - firstname_length % 4) % 4
            #Print the total with padding
            print('Firstname padding size='+str(firstname_padSize))
            #Receive more bytes
            msg = conn.recv(firstname_length + firstname_padSize + 2)
            firstname_full = firstname_length + firstname_padSize
            print(msg)
            firstname, lastname_length = unpack(str(firstname_full)+'s'+'H', msg)
            print("First name received is: "+firstname.decode('utf-8'))
            client_firstname = firstname.decode('utf-8')
            
                
            print('Lastname length without pad='+str(lastname_length))
            #calculate lastname padding size
            lastname_padSize = (4 - lastname_length % 4) % 4
            print('Lastname padding size='+str(lastname_padSize))
            
            #Receive more bytes
            msg = conn.recv(lastname_length + lastname_padSize)
            lastname_full = lastname_length + lastname_padSize
            print("Last name received is: "+msg.decode('utf-8'))
            client_lastname = msg.decode('utf-8')
            
            
            #check if both firstname and lastname are empty
            if not client_lastname and not client_firstname:
                print("Empty first name and last name!")
                #Now it's time to pack our response.
                server_msg_type = 5
                msg_information_type = 6
                message = pack('HH', server_msg_type, msg_information_type)
                #Send the message through the same connection
                err = conn.sendall(message)
                #Signal (with the flag) to close the socket
                close=True
                #And closing
                conn.close()
                serverSocket.close()
            #check if firstname is empty
            if not client_firstname:
                print("Empty first name!")
                #Now it's time to pack our response.
                server_msg_type = 5
                msg_information_type = 4
                message = pack('HH', server_msg_type, msg_information_type)
                #Send the message through the same connection
                err = conn.sendall(message)
                #Signal (with the flag) to close the socket
                close=True
                #And closing
                conn.close()
                serverSocket.close()
            #check if lastname is empty
            if not client_lastname:
                print("Empty last name!")
                #Now it's time to pack our response.
                server_msg_type = 5
                msg_information_type = 5
                message = pack('HH', server_msg_type, msg_information_type)
                #Send the message through the same connection
                err = conn.sendall(message)
                #Signal (with the flag) to close the socket
                close=True
                #And closing
                conn.close()
                serverSocket.close()
            
            
            #save firstname and lastname into info_received
            info_received["First name"]= client_firstname.rstrip('\x00')
            info_received["Last name"]= client_lastname
            #check if info list is empty and if yes terminate connection
            #because server received all the requested information
            if not info_list:
                print("Information received:")
                print(info_received)
                msg_type = 5
                #Initial response code is 0 - all ok.
                msg_information_type = 0
                #Now it's time to pack our response.
                message = pack('HH', msg_type, msg_information_type)
                #Send the message through the same connection
                err = conn.sendall(message)
                #Signal (with the flag) to close the socket
                close=True
                #And closing
                conn.close()
                serverSocket.close()
            else:
                #Now it's time to pack our response.
                msg_information_type = random.choice(info_list)
                info_list.remove(msg_information_type)
                server_msg_type = 1
                message = pack('HH', server_msg_type, msg_information_type)
                #Send the message through the same connection
                err = conn.sendall(message)
        elif(msg_type==3):
            total_message_length = msg_am
            #Receive the other 8 bytes
            msg = conn.recv(8)
            print(msg)
            am,padding,phone_number = unpack('HHI', msg)
            print('AM is: ' +str(am))
            print("Padding is: "+str(padding))
            print('Phone number is: '+str(phone_number))
            #check if phone number is not valid 
            if (len(str(phone_number))!=10 or not str(phone_number).startswith('2')):
                print("Invalid phone number!")
                #Now it's time to pack our response.
                server_msg_type = 5
                msg_information_type = 3
                message = pack('HH', server_msg_type, msg_information_type)
                #Send the message through the same connection
                err = conn.sendall(message)
                #Signal (with the flag) to close the socket
                close=True
                #And closing
                conn.close()
                serverSocket.close()
            else:
                #save phonenumber into info_received
                info_received["Phone number"]= phone_number

                #check if info list is empty and if yes terminate connection
                #because server received all the requested information
                if not info_list:
                    print("Information received:")
                    print(info_received)
                    msg_type = 5
                    #Initial response code is 0 - all ok.
                    msg_information_type = 0
                    #Now it's time to pack our response.
                    message = pack('HH', msg_type, msg_information_type)
                    #Send the message through the same connection
                    err = conn.sendall(message)
                    #Signal (with the flag) to close the socket
                    close=True
                    #And closing
                    conn.close()
                    serverSocket.close()
                else:
                    #Now it's time to pack our response.
                    msg_information_type = random.choice(info_list)
                    info_list.remove(msg_information_type)
                    server_msg_type = 1
                    message = pack('HH', server_msg_type, msg_information_type)
                    #Send the message through the same connection
                    err = conn.sendall(message)
            
        elif(msg_type==4):
            total_message_length = msg_am
            #Receive the other 6 bytes
            msg = conn.recv(6)
            print(msg)
            am,zip_code,street_length = unpack('HHH', msg)
            print('AM is: ' +str(am))
            print("Zip code is: "+str(zip_code))
            print('Total message length without pad='+str(total_message_length))
            print('Street length without pad='+str(street_length))
            #I need to find the street padding
            street_padSize=(4 - street_length % 4) % 4
            #Print the total with padding
            print('Street padding size='+str(street_padSize))
            #Receive more bytes
            msg = conn.recv(street_length + street_padSize + 2)
            street_full = street_length + street_padSize
            print(msg)
            street, city_length = unpack(str(street_full)+'s'+'H', msg)
            print("Street received is: "+street.decode('utf-8'))
            client_street = street.decode('utf-8')
            
                
            print('City length without pad='+str(city_length))
            #calculate city padding size
            city_padSize = (4 - city_length % 4) % 4
            print('City padding size='+str(city_padSize))
            
            #Receive more bytes
            msg = conn.recv(city_length + city_padSize)
            city_full = city_length + city_padSize
            print("City received is: "+msg.decode('utf-8'))
            client_city = msg.decode('utf-8')
            
            
            #save zip code, street and city into info_received
            info_received["Zip code"]= zip_code
            info_received["Street"]= client_street.rstrip('\x00')
            info_received["City"]= client_city.rstrip('\x00')
            
            #check if info list is empty and if yes terminate connection
            #because server received all the requested information
            if not info_list:
                print("Information received:")
                print(info_received)
                msg_type = 5
                #Initial response code is 0 - all ok.
                msg_information_type = 0
                #Now it's time to pack our response.
                message = pack('HH', msg_type, msg_information_type)
                #Send the message through the same connection
                err = conn.sendall(message)
                #Signal (with the flag) to close the socket
                close=True
                #And closing
                conn.close()
                serverSocket.close()
            else:   
                #Now it's time to pack our response.
                msg_information_type = random.choice(info_list)
                info_list.remove(msg_information_type)
                server_msg_type = 1
                message = pack('HH', server_msg_type, msg_information_type)
                #Send the message through the same connection
                err = conn.sendall(message)
        elif(msg_type==5):
            #Signal (with the flag) to close the socket
            close=True
            #And closing
            conn.close()
            serverSocket.close()
        else:
            #Now it's time to pack our response.
            server_msg_type = 5
            msg_information_type = 2
            message = pack('HH', server_msg_type, msg_information_type)
            #Send the message through the same connection
            err = conn.sendall(message)
            #Signal (with the flag) to close the socket
            close=True
            #And closing
            conn.close()
            serverSocket.close()
            
            
