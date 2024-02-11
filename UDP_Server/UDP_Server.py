import logging
import random
import re
import socket
import threading
import time

localIP = "127.0.0.1"
localPort = 54321

# clientIP = "127.0.0.1"
# clientPort = 11111

lossyIP = "127.0.0.1"

ncatServerPort = 10101
ncatServerIP = "127.0.0.1"

bufferSize = 1024


all_data = []
pointer = 0  #points to last element of all_data that has been sent to the ncat server

print("UDP server up and listening")

class UDP_Server():

    def __init__(self):
        logging.info('Initializing Broker')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((localIP, localPort))
        self.declare_list()
        self.clients_list = []

    def declare_list(self):
        for i in range(0 , 50):
            all_data.append(b'NULL')
    def listen_clients(self):
        while True:
            msg, client = self.sock.recvfrom(1024)
            logging.info('Received data from client %s: %s', client, msg)
            #t = threading.Thread(target=self.talk_to_client, args=(msg,client))
            #t.start()
            #t.join()
            self.talk_to_client(msg, client)

    def talk_to_client(self, message, address):
        if(message == b''):
            return
        # print("bytesAddressPair = ", message)


        #print("address = ", address)

        decoded_string = message.decode("utf-8")

        phrase_index = decoded_string.find("CRLF")
        #print("phrase_index = ", phrase_index)
        result = message[phrase_index + 4:]
        if result[len(result) - 1] == b' ':
            result = result[:-1]

        #print("message = ", message)
        #print("after mess result = ", result)
        final_answer = b'SERVERTALKING '
        final_answer += result
        int_result = int(result)
        #print("int_result = ", int_result)


        # lossy_address = (clientIP, clientPort)
        #final_answer = message
        #print("final_answer = ", final_answer)
        self.sock.sendto(final_answer, (address[0], address[1]))
        self.send_to_server(int_result, message)
    def send_to_server(self, result, message):
        global pointer
        if result > len(all_data) - 1 :
            for j in range (len(all_data),result + 10):
                all_data.append(b'NULL')
        all_data[result] = message
        number_to_sent = 0
        counter = pointer


        while all_data[counter] != b'NULL':
            counter += 1
            number_to_sent += 1
            if counter > len(all_data) - 1:
                all_data.append(b'NULL')
        # send packets from pointer -> counter - 1
        for i in range (pointer, counter):
            message_to_send = all_data[i]
            index = message_to_send.find(b'CRLF')
            message_to_send = message_to_send[:index]
            #print("message_to_send = " , message_to_send)
            self.sock.sendto(message_to_send,(ncatServerIP, ncatServerPort))

        pointer = counter


        #print("all_data = ", all_data)