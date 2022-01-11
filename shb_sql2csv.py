#!/usr/bin/env python3

import sqlite3
import os

db = "mydb2.db"

def create_connection(fn):
	conn = None
	try:
		conn = sqlite3.connect(fn)
	except Error as e:
		print(e)
	
	return conn


def count_transactions(fn):
	conn = create_connection(fn)
	with conn:
		cursor = conn.cursor()
		cursor.execute("SELECT COUNT(*) FROM transaktioner")
		r = cursor.fetchone()[0]
		return r


c = [0, count_transactions(db)]

fn = os.path.splitext(db)[0]+".csv"

f = open(os.path.splitext(db)[0]+".csv", 'w', encoding="ISO-8859-1")
conn = create_connection(db)
cursor = conn.cursor()
sql = '''
	SELECT * 
	FROM "transaktioner"
	ORDER BY
		konto ASC,
		reskontradatum ASC,
		reskontranummer DESC;	
'''
cursor.execute(sql)

for id, k, resnr, resdat, tradat, text, belopp, saldo in cursor:
	c[0] += 1
	f.write(f'{k};{resnr};{resdat};{tradat};{text};{belopp};{saldo}\n')
	print("\r" + str(round((c[0]/c[1])*100)), end="")

f.close()
conn.close()
		
