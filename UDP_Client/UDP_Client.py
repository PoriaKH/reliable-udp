import logging
import socket
import threading
import time

localIP = "127.0.0.1"
localPort = 11111

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
            logging.info('Received data from client %s: %s', client, msg)
            if firstTimeFlag == 1:
                if self.server_talking(msg) == 1:
                    talk_to_client_flag = 0
                    firstTimeFlag = 0
                    t = threading.Thread(target=self.handle_server, args= (msg,client))
                    t.start()
            elif firstTimeFlag == 0:
                if self.server_talking(msg) == 1:
                    talk_to_client_flag = 0
                    self.update_ack(msg)
            if talk_to_client_flag == 1:
                self.talk_to_client(msg, client)

    def update_ack(self,message):
        global ack

        decoded_string = message.decode("utf-8")

        substr_to_remove = "SERVERTALKING "
        result = decoded_string.strip(substr_to_remove)
        int_val = int(result)

        ack.append(int_val)
    def handle_server(self,message,client):
        self.update_ack(message)
        while True:
            time.sleep(0.1)
            need_list = []
            flag = []
            for x in range (0, index):
                need_list.append(x)
                flag.append(1)

            for i in need_list:
                for j in ack:
                    if i == j:
                        flag[i] = 0
                        break


            for x in range(0, len(flag)):
                if flag[x] == 1:
                    self.send_packet(x)

    def send_packet(self,num):
        look_for = b'CRLF'
        str_val = str(num)
        byte_val = str_val.encode()

        look_for += byte_val
        look_for += b' '


        phrase_index = all_data.find(look_for)

        data = b''
        if num == 0:
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

            data = all_data[space_index + 1 : phrase_index + 4 + len(str(num)) + 1]
        self.sock.sendto(data,(lossyIP,lossyPort))

    def server_talking(self,message):
        #checks if message starts with : b'LOSSYTALKING '
        #if yes return 1, if no return 0

        decoded_string = message.decode("utf-8")
        if decoded_string.startswith('SERVERTALKING '):
            return 1
        return 0

    def talk_to_client(self, message, address):
        global all_data
        global index


        # Sending a reply to client
        str_val = str(index)
        byte_val = str_val.encode()

        message += b'CRLF' #end of the packet
        message += byte_val #packet index comes after end of the packet
        message += b' '




        all_data += message

        self.sock.sendto(message, (lossyIP,lossyPort))
        index += 1
