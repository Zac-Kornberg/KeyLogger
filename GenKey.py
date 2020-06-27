from cryptography.fernet import Fernet

key = Fernet.generate_key()
file = open("Encryption_keys.txt", 'wb')
file.write(key)
file.close()