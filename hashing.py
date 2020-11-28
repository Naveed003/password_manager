from cryptography.fernet import Fernet

key = Fernet.generate_key()
crypter = Fernet(key)
pw = crypter.encrypt(b"PASS")
decrypt=crypter.decrypt(pw)
print(str(pw,'utf8'))
print(str(decrypt,'utf8'))
