import sqlite3
from cryptography.fernet import Fernet
import sys
import time


mydb = sqlite3.connect("database")
mycursor = mydb.cursor()

def ENCRYPT(string,key):
    crypter = Fernet(key)
    encrypted = crypter.encrypt(bytes(string,encoding="utf8"))
    return str(encrypted,"utf8")

def DECRYPT(string,key):
    crypter = Fernet(key)
    decrypted = crypter.decrypt(bytes(string,encoding="utf8"))
    return str(decrypted,"utf8")





def initial():
    print("="*20, "PASSWORD MANAGER", "="*20)
    print("\n", "="*8, "CREATE ACCOUNT", "="*8, "\n")

    while True:
        USERNAME = input("ENTER USERNAME: ")
        USERNAME = USERNAME.strip()
        if USERNAME != "":
            while True:
                EMAIL = input("ENTER A VALID EMAIL ADDRESS: ")
                EMAIL = EMAIL.strip()
                if EMAIL != "":
                    while True:
                        PASSWORD = input("ENTER MASTER PASSWORD: ")
                        PASSWORD.strip()
                        if PASSWORD != "":
                            pass
                        else:
                            print("\n", "="*4,
                                  "ENTER A VALID PASSWORD", "="*4, "\n")
                            continue
                        break

                else:
                    print("\n", "="*4, "ENTER A VALID EMAIL ADDRESS", "="*4, "\n")
                    continue
                break

        else:
            print("\n", "="*4, "ENTER A VALID USERNAME", "="*4, "\n")
            continue
        break
    cred=[USERNAME,EMAIL,PASSWORD]
    key = Fernet.generate_key()
    print(type(key))
    encrypt=[]
    for i in cred:
        encrypted=ENCRYPT(i,key)
        encrypt.append(encrypted)
    query="insert into USERS values('{}','{}','{}','{}')".format(encrypt[0],encrypt[1],encrypt[2],str(key,"utf8"))
    mycursor.execute(query)
    mydb.commit()


def master():
    print("="*20, "PASSWORD MANAGER", "="*20,"\n")
    query="select UserName,MasterPassword,Key FROM USERS"
    mycursor.execute(query)
    response=mycursor.fetchall()
    key=bytes(response[0][2],encoding="utf8")
    decrypt=[]
    count=0
    for i in response:
        for j in i:
            if count!=2:
                decrypted=DECRYPT(j,key)
                decrypt.append(decrypted)
                count+=1
    

    MasterPass=input("ENTER MASTER PASSWORD FOR {}: ".format(decrypt[0]))

    if MasterPass==decrypt[1]:
        print("\n", "="*8, "WELCOME BACK {}!!!".format(decrypt[0]),"="*8, "\n")
        main_menu()
    else:
        print("\n", "="*8, "INCORRECT PASSWORD","="*8, "\n")
        print("APPLICATION WILL QUIT IN 3 SECONDS, TRY AGAIN LATER!!!!")
        time.sleep(3)
        sys.exit()


def main_menu():
    print("hello")

    


            


if __name__ == "__main__":
    query = "select * from USERS"
    mycursor.execute(query)
    if mycursor.fetchall() == []:
        initial()
    else:
        master()
