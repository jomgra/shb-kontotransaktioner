#!/usr/bin/env python3

import sqlite3
import os

db = "mydb2.db"
commadelimiter = True

def create_connection(fn):
	conn = None
	try:
		conn = sqlite3.connect(fn)
	except Error as e:
		print(e)
	
	return conn


fn = os.path.splitext(db)[0]+".csv"
print("Exporting db to file (" + fn + ")...")

f = open(fn, 'w', encoding="ISO-8859-1")
conn = create_connection(db)
cursor = conn.cursor()
sql = '''
	SELECT * 
	FROM "transaktioner"
	ORDER BY
		konto ASC,
		reskontradatum ASC,
		reskontranummer ASC;	
'''
cursor.execute(sql)

f.write("Konto;Reskontranr;Reskontradatum;Transaktionsdatum;Text;Belopp;Saldo\n")

for id, k, resnr, resdat, tradat, text, belopp, saldo in cursor:
	if commadelimiter:
		b = str(belopp).replace(".",",")
		s = str(saldo).replace(".",",")
	else:
		b = belopp
		s = saldo
		
	f.write(f'{k};{resnr};{resdat};{tradat};{text};{b};{s}\n')

f.close()
conn.close()
print("Finished")
