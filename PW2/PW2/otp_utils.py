import os

def generate_key(length):
    """Генерує випадковий ключ заданої довжини (в байтах)."""
    return os.urandom(length)

def encrypt_decrypt(data, key):
    """
    Виконує операцію XOR для шифрування або дешифрування.
    data та key повинні бути об'єктами bytes.
    """
    if len(data) != len(key):
        raise ValueError("Довжина даних та ключа повинна бути однаковою.")

    result = bytearray()
    for i in range(len(data)):
        result.append(data[i] ^ key[i])
    return bytes(result)