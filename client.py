import random
import socket
import time
from crypting import Encryption


# информация, с которой работает клиент
class Encryption_Data:

    def __init__(self):
        self.a = random.randint(2, 100)
        self.g = random.randint(2, 100)
        self.p = random.randint(2, 100)
        self.A = self.g ** self.a % self.p
        self.B = 0

    def private_key_K(self):
        K = self.B ** self.a % self.p
        return K


enc_data = Encryption_Data()
enc = Encryption()
# задаем настройки подключения к серверу
sock = socket.socket()
server = "localhost"
port = input('Enter Port: ')
print()
# подключаемся к серверу
try:
    sock.connect((server, int(port)))
    print(f"Усешное подключение к серверу: {server}/{port}")
except ConnectionRefusedError as e:
    print(f"ERROR: {e}")

while True:
    if enc_data.B == 0: # если это начало работы - отправляем серверу первоначальное сообщения с открытым ключом
        sock.send(f'ключ A: {enc_data.A}'.encode())
        time.sleep(0.25)
        sock.send(f'пар-тр g: {enc_data.g}'.encode())
        time.sleep(0.25)
        sock.send(f'пар-тр p: {enc_data.p}'.encode())
        time.sleep(0.25)
        print(f'Отправили необходимые параметры серверу: A: {enc_data.A}\n g: {enc_data.g}\n p: {enc_data.p}')

        while True: # если получили необходимый ответ - формируем закрытый ключ K
            data = sock.recv(1024).decode("utf8")
            if data[:6] == 'ключ B':
                enc_data.B = int(data.split(' ')[2])
                print(f'Пришел открытый ключ от сервера: {enc_data.B}')
                print(f'Сформировали закрытый ключ K: {enc_data.private_key_K()}')
            if enc_data.B != 0:
                break
    # начинаем отправление сообщения и ожидаем его обратно в томже формате
    text = input("\nВведите сообщение: ")
    new_text = enc.Enc(text, enc_data.private_key_K())
    sock.send(new_text.encode())

    if len(text) == 0 or text.lower() == 'stop':
        print("Вы остоединились от сервера")
        break

    try:
        enced_data = sock.recv(1024).decode("utf8")
        denced_data = enc.Enc(enced_data, enc_data.private_key_K())
        print(f"\nОтвет сервера: {denced_data}")
    except ConnectionResetError as e:
        print(f"ERROR: {e}")
        break

sock.close()
