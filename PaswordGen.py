import hashlib as h

# основная функция
def pwdGenerator(pwd_str, salt_str, num_char):
    # конкатенация строк
    pwd_str = pwd_str + salt_str
    # кодирование в байт-строку
    byte_str = pwd_str.encode()
    # хеширование
    hash_str = h.sha256(byte_str)
    # преобразование объекта хеш-строки в обычную строку
    hex_str = hash_str.hexdigest()[:int(num_char)]
    # возврат хеш-строки
    return hex_str