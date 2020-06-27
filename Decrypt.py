from cryptography.fernet import Fernet
key = "cNfqq-aQD8Ba2qGu_nXJOv0yUTl-ygpiKcmAW7aWzBY="
key_log = "key_log_e.txt"

with open(key_log, 'rb') as f:
    data = f.read()
fernet = Fernet(key)
decrypted = fernet.decrypt(data)

with open(key_log, 'wb') as ef:
    ef.write(decrypted)