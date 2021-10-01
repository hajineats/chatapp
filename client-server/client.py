import socket
import random
from threading import Thread
from datetime import datetime

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 10000 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

class Client():
    def __init__(self) -> None:
        self.s = socket.socket()
        self.s.connect((SERVER_HOST, SERVER_PORT))
        self.name = input("Enter your name: ")
        self.listen_server()
        self.block_to_send_message()
        pass


    def block_to_send_message(self):
        while True:
            to_send = input()
            if to_send.lower() == 'q':
                break
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            to_send = f"[{date_now}] {self.name}{separator_token}{to_send}"
            self.s.send(to_send.encode())

    def listen_server(self):
        t = Thread(target=self.listen_for_messages)
        t.daemon = True
        t.start()

    def listen_for_messages(self):
        while True:
            message = self.s.recv(1024).decode()
            print("\n" + message)

    def finish_client(self):
        # close the socket
        self.s.close()
    
if __name__ == '__main__':
    Client()









