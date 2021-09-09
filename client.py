# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 10:22:38 2021

@author: kostis mavrogiorgos
"""

from struct import *
import socket 
import binascii

#Host IP to send to.
serverIP = 'localhost'
#Port to send to
serverPort = 12345

#Create the client socker
#socket.AF_INET == IPv4
#socket.SOCK_STREAM == TCP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect. The server socket should be listening.
clientSocket.connect((serverIP, serverPort))
terminate_connection = False
#Create the data for the subscription header
msg_am = input("Enter AM:")
msg_type = 0
i=0

#while loop for getting responses from server and sending requested info
while(terminate_connection == False):
    #send the subscription message only once
    if(i==0):
        #Total message length
        msg_length = 4
        #Pack the message
        message = pack('HH', msg_type, int(msg_am))
        print(message)
        
        #Send the message through the socket
        clientSocket.sendall(message)
        
        #Wait for a response (we know we'll receive 4 bytes)
        modifiedMessage = clientSocket.recv(4)
        
        #Unpack the message
        msg_type, msg_information_type  = unpack('HH', modifiedMessage)
        #Print it as hex just for the fun of it
        print(binascii.hexlify(modifiedMessage))
        i = 1
    
    #Process the response
    if(msg_type==1):
        if(msg_information_type==0):
            print("Need full name")
            first_name = input("Enter first name:")
            last_name = input("Enter last name:")
            msg_type = 2
            
            msg_firstname = first_name
            msg_lastname = last_name
            
            msg_firstname_length = len(msg_firstname)
            msg_lastname_length = len(msg_lastname)
            
            padding1 = 0
            #Total message length
            msg_length = 3*4+len(msg_firstname)+len(msg_lastname)
            #Encode the first name and last name as bytes with encoding utf-8
            nb_fisrtname = bytes(msg_firstname, 'utf-8')
            nb_lastname = bytes(msg_lastname, 'utf-8')
            
            msg_pad2Size=(4 - len(msg_firstname) % 4) % 4
            msg_pad3Size=(4 - len(msg_lastname) % 4) % 4
            print(msg_pad2Size)
            print(msg_pad3Size)
            #Create a packing string
            if(msg_pad2Size==0 and msg_pad3Size==0):
                packString = 'HHHHH'+str(len(msg_firstname))+'s'+'H'+str(len(msg_lastname))+'s'
            elif(msg_pad2Size==0 and msg_pad3Size!=0):
                packString = 'HHHHH'+str(len(msg_firstname))+'s'+'H'+str(len(msg_lastname))+'s'+str(msg_pad3Size)+'x'
            elif(msg_pad2Size!=0 and msg_pad3Size==0):
                packString = 'HHHHH'+str(len(msg_firstname))+'s'+str(msg_pad2Size)+'x'+'H'+str(len(msg_lastname))+'s'
            else:
                packString = 'HHHHH'+str(len(msg_firstname))+'s'+str(msg_pad2Size)+'x'+'H'+str(len(msg_lastname))+'s'+str(msg_pad3Size)+'x'
            #Pack the message
            #this is for debugging purposes
            
            print(packString)
            print(str(msg_type)+str(msg_length)+
                  str(msg_am)+str(padding1)+str(len(msg_firstname))+str(nb_fisrtname)+str(len(msg_lastname))+ 
                  str(nb_lastname))
            '''
            print(type(packString))
            print(type(msg_type))
            print(type(msg_length))
            print(type(int(msg_am)))
            print(type(msg_pad1Size))
            print(type(nb_fisrtname))
            print(type(nb_lastname))
            '''
            
            message = pack(packString, msg_type, msg_length, int(msg_am),padding1,int(len(msg_firstname)),nb_fisrtname,int(len(msg_lastname)),nb_lastname)
            #Send the message through the socket
            print(message)
            clientSocket.sendall(message)
            
            #Wait for a response (we know we'll receive 4 bytes)
            modifiedMessage = clientSocket.recv(4)
            
            #Unpack the message
            msg_type, msg_information_type  = unpack('HH', modifiedMessage)
            #Print it as hex just for the fun of it
            print(binascii.hexlify(modifiedMessage))
        if(msg_information_type==1):
            print("Need phone number")
            phone_number = input("Enter phone number:")
            msg_type = 3
            
            padding = 0
            #Total message length
            msg_length = 12
            
            packString = 'HHHHI'
            
            message = pack(packString, msg_type, msg_length, int(msg_am),padding,int(phone_number))
            #Send the message through the socket
            print(message)
            clientSocket.sendall(message)
            
            #Wait for a response (we know we'll receive 4 bytes)
            modifiedMessage = clientSocket.recv(4)
            
            #Unpack the message
            msg_type, msg_information_type  = unpack('HH', modifiedMessage)
            
            
            
            
        if(msg_information_type==2):
            print("Need address")
            zip_code = input("Enter zip code:")
            street = input("Enter street:")
            city = input("Enter city:")
            msg_type = 4
            
            street_length = len(street)
            city_length = len(city)
            
            
            #Total message length
            msg_length = 4*4+len(street)+len(city)
            #Encode the street and city as bytes with encoding utf-8
            nb_street = bytes(street, 'utf-8')
            nb_city = bytes(city, 'utf-8')
            
            msg_pad2Size=(4 - len(street) % 4) % 4
            msg_pad3Size=(4 - len(city) % 4) % 4
            print(msg_pad2Size)
            print(msg_pad3Size)
            #Create a packing string
            if(msg_pad2Size==0 and msg_pad3Size==0):
                packString = 'HHHHH'+str(len(street))+'s'+'H'+str(len(city))+'s'
            elif(msg_pad2Size==0 and msg_pad3Size!=0):
                packString = 'HHHHH'+str(len(street))+'s'+'H'+str(len(city))+'s'+str(msg_pad3Size)+'x'
            elif(msg_pad2Size!=0 and msg_pad3Size==0):
                packString = 'HHHHH'+str(len(street))+'s'+str(msg_pad2Size)+'x'+'H'+str(len(city))+'s'
            else:
                packString = 'HHHHH'+str(len(street))+'s'+str(msg_pad2Size)+'x'+'H'+str(len(city))+'s'+str(msg_pad3Size)+'x'
            #Pack the message
            #this is for debugging purposes
            
            print(packString)
            print(str(msg_type)+str(msg_length)+
                  str(msg_am)+str(zip_code)+str(len(street))+str(nb_street)+str(len(city))+ 
                  str(nb_city))
            '''
            print(type(packString))
            print(type(msg_type))
            print(type(msg_length))
            print(type(int(msg_am)))
            print(type(msg_pad1Size))
            print(type(nb_fisrtname))
            print(type(nb_lastname))
            '''
            
            message = pack(packString, msg_type, msg_length, int(msg_am),int(zip_code),int(len(street)),nb_street,int(len(city)),nb_city)
            #Send the message through the socket
            print(message)
            clientSocket.sendall(message)
            
            #Wait for a response (we know we'll receive 4 bytes)
            modifiedMessage = clientSocket.recv(4)
            
            #Unpack the message
            msg_type, msg_information_type  = unpack('HH', modifiedMessage)
            
            
            
            
            
    if(msg_type==5):
        if(msg_information_type==0):
            print("All went well")
            #set terminate_connetcion to True to exit the loop
            terminate_connection == True
            break
        if(msg_information_type==1):
            print("Inconsistent AM")
            #set terminate_connetcion to True to exit the loop
            terminate_connection == True
            break
        if(msg_information_type==2):
            print("Unknown info type")
            #set terminate_connetcion to True to exit the loop
            terminate_connection == True
            break
        if(msg_information_type==3):
            print("Wrong phone number")
            #set terminate_connetcion to True to exit the loop
            terminate_connection == True
            break
        if(msg_information_type==4):
            print("Invalid firstname")
            #set terminate_connetcion to True to exit the loop
            terminate_connection == True
            break
        if(msg_information_type==5):
            print("Invalid last name")
            #set terminate_connetcion to True to exit the loop
            terminate_connection == True
            break
        if(msg_information_type==6):
            print("Invalid first name and last name")
            #set terminate_connetcion to True to exit the loop
            terminate_connection == True
            break
    

