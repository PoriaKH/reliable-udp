import logging
import random
import re
import socket
import threading
import time

localIP = "127.0.0.1"
localPort = 11111

# serverIP = "127.0.0.1"
# serverPort = 54321

lossyIP = "127.0.0.1"
lossyPort = 12345

bufferSize = 1024

firstTimeFlag = 1

all_data = b''
index = 0

ack = []

print("UDP client up and listening")

class UDP_Client():

    def __init__(self):
        logging.info('Initializing Broker')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((localIP, localPort))
        self.clients_list = []


    def listen_clients(self):
        global firstTimeFlag

        while True:
            talk_to_client_flag = 1
            msg, client = self.sock.recvfrom(1024)
            #print("msg = ", msg)
            logging.info('Received data from client %s: %s', client, msg)
            if firstTimeFlag == 1:
                #print("Here1")
                if self.server_talking(msg) == 1:
                    #print("Here2")
                    talk_to_client_flag = 0
                    firstTimeFlag = 0
                    t = threading.Thread(target=self.handle_server, args= (msg,client))
                    t.start()
                    #print("after this !")
                    #self.handle_server(msg,client)
            elif firstTimeFlag == 0:
                if self.server_talking(msg) == 1:
                    #print("Here3")
                    talk_to_client_flag = 0
                    self.update_ack(msg)
            #t = threading.Thread(target=self.talk_to_client, args=(msg,client))
            #t.start()
            #t.join()
            if talk_to_client_flag == 1:
                #print("Here4")
                self.talk_to_client(msg, client)
    def update_ack(self,message):
        global ack
        #TODO update ack

        decoded_string = message.decode("utf-8")

        substr_to_remove = "SERVERTALKING "
        result = decoded_string.strip(substr_to_remove)
        int_val = int(result)

        #print("int value = ", int_val)
        ack.append(int_val)
        #print("ack = ", ack)
    def handle_server(self,message,client):
        self.update_ack(message)
        while True:
            time.sleep(0.1)
            #print("server said : ", message)
            need_list = []
            flag = []
            for x in range (0, index):
                need_list.append(x)
                flag.append(1)

            ack_len = len(ack)
            #print("len(ack) = ", ack_len)
            #print("need_list before = ", need_list)


            for i in need_list:
                for j in ack:
                    if i == j:
                        flag[i] = 0
                        break


            #print("flag_list = ", flag)
            for x in range(0, len(flag)):
                if flag[x] == 1:
                    self.send_packet(x)

            #time.sleep(1000000)
            #print("after sleep")
    def send_packet(self,num):
        look_for = b'CRLF'
        str_val = str(num)
        byte_val = str_val.encode()

        look_for += byte_val
        look_for += b' '

        #print("look for = ", look_for)

        phrase_index = all_data.find(look_for)
        #print("phrase_index = ", phrase_index)

        data = b''
        if num == 0:
            #TODO
            data = all_data[:phrase_index + 4 + len(str(num))]
        else:
            new_str_val = str(num - 1)
            new_byte_val = new_str_val.encode()
            new_look = b'CRLF'
            new_look += new_byte_val
            new_look += b' '
            space_index = all_data.find(new_look)
            space_index += 3
            space_index += len(new_str_val)
            space_index += 1

            #print("space_index(after_space) = ", space_index)
            data = all_data[space_index + 1 : phrase_index + 4 + len(str(num)) + 1]
            #print("data = ", data)
        self.sock.sendto(data,(lossyIP,lossyPort))

    def server_talking(self,message):
        #check if message starts with : b'LOSSYTALKING '
        #if yes return 1, if no return 0
        #print("in server_talking message = ", message)
        decoded_string = message.decode("utf-8")
        #print("in server_talking decoded_string = ", decoded_string)
        if decoded_string.startswith('SERVERTALKING '):
            #print("Here 7")
            return 1
        #print("Here 8")
        return 0

    def talk_to_client(self, message, address):
        global all_data
        global index

        #print("bytesAddressPair = ", message)

        #clientMsg = "Message from Client:{}".format(message)
        #clientIP = "Client IP Address:{}".format(address)

        #print("clientMsg = ", clientMsg)
        #print("clientIP = ", clientIP)

        # Sending a reply to client
        str_val = str(index)
        byte_val = str_val.encode()

        message += b'CRLF' #end of the packet
        message += byte_val #packet index comes after end of the packet
        message += b' '

        #print("message = ", message)



        all_data += message
        #print("all_data = ",all_data)
        #print("")

        #final_answer = message
        self.sock.sendto(message, (lossyIP,lossyPort))
        index += 1
