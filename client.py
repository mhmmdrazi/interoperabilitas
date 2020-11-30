import socket
import threading

# membuat nickname
nickname = input("Choose your nickname: ")

# konek ke server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12123))

# menerima dan mengirim data ke server
def receive():
    while True:
        try:
            # menerima pesan dari server
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # untuk menutup koneksi jika error
            print("An error occured!")
            client.close()
            break

# Mengirim pesan ke server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

# menjalankan thread(agar program dapat dijalankan bersamaan
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()