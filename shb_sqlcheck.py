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
	"saldo": 0,
	"resdat": ""
}

for id, k, resnr, resdat, tradat, text, belopp, saldo in cursor:
	print(float(saldo))
	
'''
	if mem["konto"] == k:
		if mem["saldo"] + float(belopp) == float(saldo):
			mem["saldo"] = float(saldo)
		else:
			print(mem["resdat"])
			print(resdat + "-", end="")
			mem["resdat"] = resdat
			mem["saldo"] = saldo
	else:

		print(mem["resdat"])
		print("Account:" + k)
		print(resdat + "-", end="")
		mem["konto"] = k
		mem["saldo"] = saldo
		mem["resdat"] = resdat
		
'''
			
conn.close()
