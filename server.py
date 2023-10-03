import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5551))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            newMess=message.split()

            if "lst_ppl" in newMess:
                lst= " ".join(nicknames).encode('ascii')  
                client.send(lst)

            elif "private" in newMess:
                ind=nicknames.index(newMess[2])
                mes= " ".join(newMess[3::])
                prv_mes= newMess[0]+mes
                client= clients[ind]
                client.send(prv_mes.encode('ascii'))

            else:
                broadcast(lst) 
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)

        client.send('PASS'.encode('ascii'))
        password = client.recv(1024).decode('ascii')
        clients.append(client)

        if password == "1234":
            print(f"Nickname of the client is {nickname}!")
            broadcast(f"{nickname} joined the chat!".encode('ascii'))
            client.send("Connected to the server!".encode('ascii'))
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        else:
            client.close()


receive()
