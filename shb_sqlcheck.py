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


conn = create_connection(db)
cursor = conn.cursor()

#cursor.execute("DELETE FROM transaktioner WHERE rowid=232")
#conn.commit()

sql = '''
	SELECT * 
	FROM "transaktioner"
	ORDER BY
		konto ASC,
		reskontradatum ASC,
		reskontranummer ASC;	
'''
cursor.execute(sql)

mem = {
	"konto": "",
	"saldo": float(0),
	"resdat": ""
}

for id, k, resnr, resdat, tradat, text, belopp, saldo in cursor:
	if mem["konto"] == k:
		if round(mem["saldo"] + float(belopp), 2) == float(saldo):
			mem["saldo"] = float(saldo)
			mem["resdat"] = resdat
			
		else:
			print(mem["resdat"])
			print(resdat + " - ", end="")
			mem["resdat"] = resdat
			mem["saldo"] = float(saldo)
			
	else:
		print(mem["resdat"])
		print("\nAccount: " + k)
		print(resdat + " - ", end="")
		mem["konto"] = k
		mem["saldo"] = float(saldo)
		mem["resdat"] = resdat
		
print(resdat)			
conn.close()
