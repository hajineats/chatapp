import socket
import random
from threading import Thread
from datetime import datetime
from typing import final
from comm_enum import *

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 10000 # server's port



class Client():
    def __init__(self):
        self.nickname = input("Enter your name: ")
        self.initialized = False
        self.s = socket.socket()
        self.configurate_socket()
        self.sockname = self.s.getsockname()
        self.block_to_send_message()
        pass

    # (important) sends user input to server
    def block_to_send_message(self):
        while True:
            def make_message():
                # Client configuration message
                if not self.initialized:
                    self.initialized = True
                    return f"{CENUM_START_OF_MESSAGE}{sep}{CENUM_CLIENT_CONFIG}{sep}{self.nickname}{sep}{self.s.getsockname()}"
                
                # Send message
                message = "hello my brother!"
                sendto = input("enter sockname of other client")
                print(sendto)
                to_send = f"{CENUM_START_OF_MESSAGE}{sep}{CENUM_INDIVIDUALMESSAGE}{sep}{self.sockname}{sep}{sendto}{sep}"
                to_send += f"{message}"
                return to_send

                # Whatever you want to send
                to_send = input()
                date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                to_send = f"[{date_now}] {self.nickname}{sep}{to_send}"
                return to_send

            self.s.send(make_message().encode())

    def configurate_socket(self):
        self.s.connect((SERVER_HOST, SERVER_PORT))
        self.listen_server()
        print(self.s.getsockname())

    def listen_server(self):
        def listen_for_messages():
            while True:
                message = self.s.recv(1024).decode()
                print("\n" + message)
        t = Thread(target=listen_for_messages)
        t.daemon = True
        t.start()



    def finish_client(self):
        # close the socket
        self.s.close()
    
if __name__ == '__main__':
    client = None
    try:
        client = Client()
    finally:
        client.finish_client()











