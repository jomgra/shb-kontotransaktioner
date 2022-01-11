#!/usr/bin/env python3

import os
from bs4 import BeautifulSoup
import requests as req
import sqlite3
import hashlib

path = "./"
db = "mydb2.db"


def create_connection(fn):
	conn = None
	try:
		conn = sqlite3.connect(fn)
	except Error as e:
		print(e)
	
	return conn


def create_database(fn):
	conn = create_connection(fn)
	cursor = conn.cursor()
	sql = '''
	CREATE TABLE 'transaktioner' (
		'id' TEXT UNIQUE,
		'konto' INTEGER,
		'reskontranummer' INTEGER,
		'reskontradatum' TEXT,
		'transaktionsdatum' TEXT,
		'text' TEXT,
		'belopp' INTEGER,
		'saldo' INTEGER,
		PRIMARY KEY("id")
		)
	'''
	cursor.execute(sql)
	conn.close()


def import_transactions(fn):
	y = ["", 1]
	stat = [0, 0]
	
	with open(fn, 'r', encoding="ISO-8859-1") as f:
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
			sql = '''
				INSERT INTO transaktioner (
					id,
					konto,
					reskontranummer,
					reskontradatum,
					transaktionsdatum,
					text,
					belopp,
					saldo)
				values (?,?,?,?,?,?,?,?)
			'''
			cursor.execute(sql, a)
			stat[0] += 1
			
		except sqlite3.IntegrityError:
			stat[1] += 1

		conn.commit()
		conn.close()
	
	return {"file": fn, "account": k, "added": stat[0], "ignored": stat[1]}


def count_transactions(fn):
	conn = create_connection(fn)
	cursor = conn.cursor()
	cursor.execute("SELECT COUNT(*) FROM transaktioner")
	r = cursor.fetchone()[0]
	conn.close()
	return r


def main():
	
	if not os.path.isfile(db):
		create_database(db)

	files = [s for s in os.listdir(path) if s.endswith(".xls")]

	for file in files:
		r = import_transactions(file)
		print("\n")
		for key in r:
			print(key.capitalize(), ":", r[key])
			
	print("\nNumber of transactions in database:", count_transactions(db))

if __name__ == "__main__":
	main()
