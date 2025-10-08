import socket
from otp_utils import generate_key, encrypt_decrypt

HOST = '127.0.0.1'  
PORT = 65432       

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"Підключено до сервера {HOST}:{PORT}")

            message = input("Введіть повідомлення для шифрування: ")
            message_bytes = message.encode('utf-8')
            message_length = len(message_bytes)

            # 1. Генерувати ключ
            key = generate_key(message_length)
            print(f"Згенерований ключ (байтами): {key}")

            # 2. Шифрувати повідомлення
            encrypted_message = encrypt_decrypt(message_bytes, key)
            print(f"Зашифроване повідомлення (байтами): {encrypted_message}")

            # 3. Відправити довжину повідомлення/ключа (4 байти)
            s.sendall(message_length.to_bytes(4, 'big'))

            # 4. Відправити зашифроване повідомлення
            s.sendall(encrypted_message)
            print("Зашифроване повідомлення відправлено.")

            # 5. Відправити ключ
            s.sendall(key)
            print("Ключ відправлено.")

        except ConnectionRefusedError:
            print(f"Не вдалося підключитися до сервера {HOST}:{PORT}. Переконайтеся, що сервер запущений.")
        except Exception as e:
            print(f"Виникла помилка: {e}")
        finally:
            s.close()

if __name__ == "__main__":
    start_client()