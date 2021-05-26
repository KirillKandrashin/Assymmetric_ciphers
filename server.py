import random
import socket
import time
from crypting import Encryption


class Encryption_Data:

    def __init__(self):
        self.b = random.randint(2, 100)
        self.g = 0
        self.p = 0
        self.A = 0

    def public_key_B(self):
        B = self.g ** self.b % self.p
        return B

    def private_key_K(self):
        K = self.A ** self.b % self.p
        return K


enc_data = Encryption_Data()
enc = Encryption()

sock = socket.socket()

port = input('Enter port: ')
sock.bind(('', int(port)))

while True:

    sock.listen(1)

    conn = sock.accept()[0]
    print()

    while True:
        if enc_data.A != 0 and enc_data.p != 0 and enc_data.g != 0:
            print(f'Отправили ключ B клиенту = {enc_data.public_key_B()}')
            print(f'Сформировали ключ K: {enc_data.private_key_K()}')
            time.sleep(0.25)
            conn.send(f'ключ B: {enc_data.public_key_B()}'.encode())

        try:
            data = conn.recv(1024).decode("utf8")
        except ConnectionResetError:
            break

        if data[:6] == 'ключ A':
            print(data)
            enc_data.A = int(data.split(' ')[2])
        elif data[:8] == 'пар-тр g':
            print(data)
            enc_data.g = int(data.split(' ')[2])
        elif data[:8] == 'пар-тр p':
            print(data)
            enc_data.p = int(data.split(' ')[2])
        else:

            data = enc.Enc(data, enc_data.private_key_K())
            new_data = enc.Enc("Вашим сообщением было - " + data, enc_data.private_key_K())

            # ВЫХОД КЛИЕНТА
            if data == "" or data == "exit":
                break
            elif data == "stop":
                break
            else:

                conn.send(new_data.encode())

                print()

    if data == "stop":
        break

conn.close()
