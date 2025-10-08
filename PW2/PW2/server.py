import socket
import threading
from otp_utils import encrypt_decrypt

HOST = '127.0.0.1'  
PORT = 65432       

def handle_client(conn, addr):
    print(f"Підключено до {addr}")
    try:
        # 1. Отримати довжину ключа/повідомлення
        length_bytes = conn.recv(4) # Очікуємо 4 байти для довжини
        if not length_bytes:
            print("Клієнт відключився або не надіслав довжину.")
            return
        message_length = int.from_bytes(length_bytes, 'big')
        print(f"Очікувана довжина повідомлення/ключа: {message_length} байт")

        # 2. Отримати зашифроване повідомлення
        encrypted_message = b''
        while len(encrypted_message) < message_length:
            packet = conn.recv(message_length - len(encrypted_message))
            if not packet:
                print("Клієнт відключився під час надсилання повідомлення.")
                return
            encrypted_message += packet
        print(f"Отримано зашифроване повідомлення: {encrypted_message}")

        # 3. Отримати ключ
        key = b''
        while len(key) < message_length:
            packet = conn.recv(message_length - len(key))
            if not packet:
                print("Клієнт відключився під час надсилання ключа.")
                return
            key += packet
        print(f"Отримано ключ: {key}")

        # 4. Дешифрувати повідомлення
        decrypted_message = encrypt_decrypt(encrypted_message, key)
        print(f"Дешифроване повідомлення: {decrypted_message.decode('utf-8')}")

    except Exception as e:
        print(f"Помилка при обробці клієнта {addr}: {e}")
    finally:
        print(f"Відключено {addr}")
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер слухає на {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()