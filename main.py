import sqlite3
from cryptography.fernet import Fernet
import sys
import time
import random
import pandas as pd
pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
# my sql connction


mydb = sqlite3.connect("database.db")
mycursor = mydb.cursor()


def ENCRYPT(string, key):
    crypter = Fernet(key)
    encrypted = crypter.encrypt(bytes(string, encoding="utf8"))
    return str(encrypted, "utf8")


def DECRYPT(string, key):
    crypter = Fernet(key)
    decrypted = crypter.decrypt(bytes(string, encoding="utf8"))
    return str(decrypted, "utf8")


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
    cred = [USERNAME, EMAIL, PASSWORD]
    key = Fernet.generate_key()
    print(type(key))
    encrypt = []
    for i in cred:
        encrypted = ENCRYPT(i, key)
        encrypt.append(encrypted)
    query = "insert into USERS values('{}','{}','{}','{}')".format(
        encrypt[0], encrypt[1], encrypt[2], str(key, "utf8"))
    mycursor.execute(query)
    mydb.commit()


def master():
    print("="*20, "PASSWORD MANAGER", "="*20, "\n")
    query = "select UserName,MasterPassword,Key FROM USERS"
    mycursor.execute(query)
    response = mycursor.fetchall()
    key = bytes(response[0][2], encoding="utf8")
    decrypt = []
    count = 0
    for i in response:
        for j in i:
            if count != 2:
                decrypted = DECRYPT(j, key)
                decrypt.append(decrypted)
                count += 1
    MasterPass="logon@123"
    #MasterPass = input("ENTER MASTER PASSWORD FOR {}: ".format(decrypt[0]))

    if MasterPass == decrypt[1]:
        print("\n", "="*8,
              "WELCOME BACK {}!!!".format(decrypt[0]), "="*8, "\n")
        main_menu()
    else:
        print("\n", "="*8, "INCORRECT PASSWORD", "="*8, "\n")
        print("APPLICATION WILL QUIT IN 3 SECONDS, TRY AGAIN LATER!!!!")
        time.sleep(3)
        sys.exit()


def main_menu():
    print("\n", "="*4, "MAIN MENU", "="*4, "\n")
    print("OPTION 1: NEW RECORD")
    print("OPTION 2: VIEW RECORDS")
    print("OPTION 3: SEARCH RECORDS")
    print("OPTION 4: DELETE RECORD")
    print("OPTION 5: EXIT")
    list = [1, 2, 3, 4, 5]
    while True:
        opt = input("\nENTER OPTION NUMBER: ")
        try:
            opt = int(opt.strip())
            if opt in list:
                break
            else:
                print("\n", "="*4, "ENTER A VALID OPTION", "="*4, "\n")
                continue
        except Exception:
            print("\n", "="*4, "ENTER A VALID OPTION", "="*4, "\n")
            continue
    if opt == 1:
        NEW_RECORD()
    elif opt == 2:
        VIEW_RECORDS()
    elif opt == 3:
        SEARCH_RECORDS()
    elif opt == 4:
        DELETE_RECORD()


def NEW_RECORD():
    print("\n")
    while True:
        APPNAME = input("ENTER APPLICATION/WEBSITE NAME: ")
        if APPNAME.strip() != "":
            while True:
                URL = input(
                    "ENTER URL (IF NOT AVAILABLE ENTER APPLICATION NAME): ")
                if URL.strip() != "":
                    while True:
                        EMAIL_ID = input("ENTER EMAIL ADDRESS: ")
                        if EMAIL_ID.strip() != "":
                            while True:
                                USERNAME = input("ENTER USERNAME (IF NONE ENTER EMAIL ID): ")
                                if USERNAME.strip()!="":
                                    while True:
                                        PASSWORD=input("ENTER PASSWORD: ")
                                        if PASSWORD.strip()!="":
                                            pass
                                        else:
                                            print("\n", "="*4,"PLEASE ENTER A PASSWORD", "="*4, "\n")
                                            continue
                                        break
                                else:
                                    print("\n", "="*4,"PLEASE ENTER A USERNAME", "="*4, "\n")
                                    continue
                                break
                        else:
                            print("\n", "="*4,
                                  "PLEASE ENTER A EMAIL ID", "="*4, "\n")
                            continue
                        break              
                else:
                    print("\n", "="*4, "PLEASE ENTER A WEBSITE URL", "="*4, "\n")
                    continue
                break
        else:
            print("\n", "="*4, "PLEASE ENTER A APPLICATION NAME", "="*4, "\n")
            continue
        break
    query="select AccountNumber from PASSWORDS"
    mycursor.execute(query)
    response=mycursor.fetchall()
    ACCOUNTNUMBERS=[]
    for i in response:
        for j in i:
            ACCOUNTNUMBERS.append(int(j))
    while True:
        ACCOUNTNUMBER=random.randint(0,100000000)
        if ACCOUNTNUMBER in ACCOUNTNUMBERS:
            continue
        else:
            break
    creds=[ACCOUNTNUMBER,EMAIL_ID,USERNAME,PASSWORD,URL,APPNAME]
    key=Fernet.generate_key()
    encrypt=[]
    for i in creds:
        ENCRYPTED=ENCRYPT(str(i),key)
        encrypt.append(ENCRYPTED)
    
    try:
        query="insert into PASSWORDS values({},'{}','{}','{}','{}','{}')".format(ACCOUNTNUMBER,encrypt[1],encrypt[2],encrypt[3],encrypt[4],encrypt[5])
        mycursor.execute(query)
        query="insert into KeyDetails values({},'{}')".format(ACCOUNTNUMBER,str(key,"utf8"))
        mycursor.execute(query)
        mydb.commit()
    except Exception:
        print("UNKNOWN ERROR, TRY AGAIN LATER")

    pass


def VIEW_RECORDS():
    query="SELECT PASSWORDS.AppName,PASSWORDS.Email_id,PASSWORDS.Username,PASSWORDS.Password,PASSWORDS.URL,KeyDetails.Key FROM PASSWORDS,KeyDetails where KeyDetails.AccountNumber=PASSWORDS.AccountNumber"
    mycursor.execute(query)
    temp=[]
    response=[]
    for i in mycursor.fetchall():
        for j in i:
            temp.append(j)
        response.append(temp)
        temp=[]
    list=[["APP NAME","EMAIL ID","USERNAME","PASSWORD","URL"]]
    for i in range(len(response)):
        for j in range(len(response[i])):
            if j!=5:
                key=bytes(response[i][5],encoding="utf8")
                dec=DECRYPT(response[i][j],key)
                temp.append(dec)
        list.append(temp)
        temp=[]
    if len(list)!=1:
        df=pd.DataFrame(list[1:],columns=list[0],index=[i for i in range(len(list[1:]))])
        print(df)
        time.sleep(2)
        main_menu
    else:
        print("NO SAVED PASSWORDS")
        time.sleep(2)
        main_menu()



def SEARCH_RECORDS():
    pass


def DELETE_RECORD():
    pass


if __name__ == "__main__":
    query = "select * from USERS"
    mycursor.execute(query)
    if mycursor.fetchall() == []:
        initial()
    else:
        master()



