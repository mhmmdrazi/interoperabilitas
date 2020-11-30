import threading
import socket

# setting koneksi
host = '127.0.0.1'
port = 12123

# Menjalankan server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# list untuk client dan nama di program
clients = []
nicknames = []

# Mengirim pesan ke klien yang terhubung
def broadcast(message):
    for client in clients:
        client.send(message)

# untuk menghandle pesan dari client
def handle(client):
    while True:
        try:
            # membroadcast pesan
            message = client.recv(1024)
            broadcast(message)
        except:
            # untuk ketika client keluar dari server
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# fungsi untuk menerima dam memproses pesan dari client
def receive():
    while True:
        # menerima koneksi server
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # meminta dan mengirim nama
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # menulis dan mengirim nama
        print("Nickname {} has joined to server".format(nickname))
        broadcast("{} joined! ".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # memulai proses thread untuk client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()