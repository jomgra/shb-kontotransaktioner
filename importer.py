#!/usr/bin/env python

import os
from bs4 import BeautifulSoup
import requests as req
import sqlite3
import hashlib

path = "./"
db = "mydb2.db"


def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)
	
	return conn


def create_table(f):
	conn = create_connection(f)
	cursor = conn.cursor()
	sql = '''
	CREATE TABLE "transaktioner" (
		"id" TEXT UNIQUE,
		"konto" INTEGER,
		"reskontranummer" INTEGER,
		"reskontradatum" TEXT,
		"transaktionsdatum"	TEXT,
		"Text" TEXT,
		"Belopp" INTEGER,
		"Saldo" INTEGER,
		PRIMARY KEY("id")
		)
	'''
	cursor.execute(sql)
	conn.close()
	

if not os.path.isfile(db):
	create_table(db)
	
files = [s for s in os.listdir(path) if s.endswith(".xls")]

for file in files:
	y = ["", 1]
	stat = [0, 0]
	
	with open(path + file, 'r', encoding="ISO-8859-1") as f:
		c = f.read()

	k = c[c.find("Konto: ")+7:c.find("&nbsp;&nbsp;Period:")]
	
	soup = BeautifulSoup(c, "html5lib")
	table = soup.find_all("table")
	
	for tr in table[3].find_all("tr")[1:]:
		
		td = tr.find_all("td", {"class": "", "nowrap": "nowrap"})
			
		if td[0].text == y[0]:
			y[1] += 1
		else:
			y[1] = 1
			y[0] = td[0].text
			
		a = [k, str(y[1])]
		
		for s in td:
			a.append(s.text)
			
		a.insert(0, hashlib.sha256("".join(a).encode("utf-8")).hexdigest())
		
		conn = create_connection(db)
		cursor = conn.cursor()
	
		try:
			cursor.execute("INSERT INTO transaktioner (id, konto, reskontranummer, reskontradatum, transaktionsdatum, Text, Belopp, Saldo) values (?,?,?,?,?,?,?,?)", a)
			stat[0] += 1
			
		except sqlite3.IntegrityError:
			stat[1] += 1

		conn.commit()
		conn.close()
		
	print("\nFile:", file)
	print("Bankkonto:", k)
	print("Transactions added:", stat[0])
	print("Duplicates ignored:", stat[1])
