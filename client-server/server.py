import socket
from threading import Thread
from typing import final

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 10000 
separator_token = "<SEP>" # we will use this to separate the client name & message

class Server():
    def __init__(self) -> None:
        self.client_sockets = set()
        # configurate socket
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((SERVER_HOST, SERVER_PORT))
        self.s.listen(5)
        print(f"[*] Listening as {self.s.getsockname()}")
        pass
    
    def listen_for_client(self, cs):
        while True:
            try:
                msg = cs.recv(1024).decode()
            except Exception as e:
                # client no longer connected
                print(f"[!] Error: {e}")
                self.client_sockets.remove(cs)
            else:
                msg = msg.replace(separator_token, ": ")
            for client_socket in self.client_sockets:
                client_socket.send(msg.encode())

    def block_for_connection(self):
        while True:
            client_socket, client_address = self.s.accept()
            print(f"[+] {client_address} connected.")
            self.client_sockets.add(client_socket)

            t = Thread(target=self.listen_for_client, args=(client_socket,))
            t.daemon = True
            t.start()
    
    
    def finish_server(self):
        for cs in self.client_sockets:
            cs.close()
        self.s.close()        



if __name__ == '__main__':
    server:Server = None
    try:
        server = Server()
        server.block_for_connection()
    finally:
        server.finish_server()



