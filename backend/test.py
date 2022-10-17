import hashlib

if __name__ == '__main__':
    hasher = hashlib.md5()
    hasher.update(bytes('hello', encoding='utf-8'))


    def hash_password(password: str):
        hashed_password = hashlib.md5(bytes('hello', encoding='utf-8'))
        hashed_password.update(bytes(password, encoding='utf-8'))
        return hashed_password.hexdigest()

    print(hasher.hexdigest(), '\n', hash_password('hello'))