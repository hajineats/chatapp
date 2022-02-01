# Python TLS chatting application
A secured chatting application, implemented using Python, PyQt, and mechanisms of *Sockets* and *Public Key Cryptography*.

Created for SOFTENG364 (Software Network) which was making a multiuser client/server chatting application that supports both 1:1 chat and group chat.

Dependencies: PyQT5(GUI) and Python 3. 

<img width="1005" alt="Screen Shot 2021-10-16 at 1 32 58 AM" src="https://user-images.githubusercontent.com/68993476/137487347-d37b0482-bb35-4933-909b-61d9b362ea4b.png">

This [blog post](https://optimizemarginality.tistory.com/82) documents a handful of technical challenges I had through creating this applications, and how I went about solving them. This is the [demo](https://drive.google.com/file/d/1ymrcKlB2f9G2Fl9a9GGo14Q4WTrKqJKh/view?usp=sharing).

## Functionality

- The application consists of a client-side graphical user interface (which is used to send messages to other clients), and a server that propagates messages, using socket management.
- PyQT is used for producing the graphical user interface.
- Clients can create chatting groups and invite their friends to join.
- Clients can communicate with others, either by direct messaging or joining an existing group.
- Communication between clients is fully encrypted using *public key cryptography*, so the messages cannot be intercepted and interpretted by attackers.

# Running the program
Start up the server by running ```python3 server.py```. Then boot up client processes using ```python3 client.py```. By default server.py binds to 127.0.0.1 (localhost) port 10000.
## Generating SSL certificate & key
Dummy key/certificate pairs are in the repository, but you can make a custom one through openssl.

openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt

# Screenshots
<img width="501" alt="Screen Shot 2021-10-16 at 1 41 22 AM" src="https://user-images.githubusercontent.com/68993476/137488321-f77a5a9d-8c10-4d79-903e-56f9247aa862.png">
<img width="1010" alt="Screen Shot 2021-10-16 at 1 44 09 AM" src="https://user-images.githubusercontent.com/68993476/137488704-b45dd8be-0b14-4e4d-bd11-7828077ba0fa.png">
<img width="1010" alt="Screen Shot 2021-10-16 at 1 44 37 AM" src="https://user-images.githubusercontent.com/68993476/137488833-06a776a3-a82a-454c-870f-399c0257cf65.png">
<img width="1007" alt="image" src="https://user-images.githubusercontent.com/68993476/137488967-a1e5d169-122f-4e2d-8918-a875fe6083d5.png">
<img width="1012" alt="image" src="https://user-images.githubusercontent.com/68993476/137489029-102ca1f5-17d1-44b7-b55a-8b73eb5d9837.png">



