import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import time, datetime
import os
import sqlite3

def connect_db():
    return sqlite3.connect('DB_datalogger.db')

def count ():
    
    for i in range  (0, 30, 10):
        #print(i)
        print(f"{i} ", end="\r", flush=True)
        time.sleep(10)

def repeat():
    while True:
        os.system('cls')
        print (datetime.datetime.now())
        
        datalogger()
        
        print("----------------------------")
    #    time.sleep(90)
        print("Novo ucitavanje za 30 sekundi:")
        count()

def add_to_db(data):
    data_for_db=[]
    data_for_db.append(datetime.datetime.now())
    for d in data:
        if d[1]=='-inf' or d[1]=='nan':
            data_for_db.append(float(-100))
        else:
            data_for_db.append(float(d[1]))

    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute('''
        INSERT INTO datalogger1 (time, chanel_00, chanel_01, chanel_02, chanel_03, chanel_04, chanel_05, chanel_06, chanel_07, chanel_08, chanel_09)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data_for_db[0], data_for_db[1], data_for_db[2], data_for_db[3], data_for_db[4], data_for_db[5], data_for_db[6], data_for_db[7], data_for_db[8], data_for_db[9], data_for_db[10]))
    conn.commit()
    conn.close()
    return print("\nUspjelo dodavnje\n")


def datalogger():
    try:

        response = requests.get('http://192.168.1.2/currentinfo')
        
        print("Vrijednosti sa data logera 192.168.1.2 ")
        print ("*******************")
        soup=BeautifulSoup(response.text, 'html.parser')
        data = soup.get_text()
        #print(soup.get_text())
        #print (len(soup))
        data_split=data.split("\n")
        #print(data_split)
        out=[]
        for i in range (0, 10, 1):
            temp=data_split[i]
            out.append(temp.split("\t"))
        print(out)
        print("\nUbaci u DB\n")
        add_to_db(out)


    except Exception as e:
    
        print("Error: ", e)
        print("Nije uspjelo povezivanje")


if __name__=="__main__":
    #datalogger()
    repeat()
