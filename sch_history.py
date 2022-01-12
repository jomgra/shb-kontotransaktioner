#!/usr/bin/env python3

import sqlite3
import os
import datetime

db = "mydb2.db"
commadelimiter = True

def dateconvert(s):
	d = datetime.date(int(s[0:4]), int(s[5:7]), int(s[8:10]))
	return d
	

def create_connection(fn):
	conn = None
	try:
		conn = sqlite3.connect(fn)
	except Error as e:
		print(e)
	
	return conn


fn = os.path.splitext(db)[0]+"_balance.csv"
print("Writing history to file (" + fn + ")...")

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

day = {}
accounts = []
oldsaldo = {}

for id, k, resnr, resdat, tradat, text, belopp, saldo in cursor:
	
	s = str(saldo)
	if commadelimiter:
		s = s.replace(".",",")
		
	if k not in accounts:
		accounts.append(k)
	try:
		day[resdat][k] = s
	except:
		day[resdat] = {}
		day[resdat][k] = s

conn.close()

keys = list(day.keys())
currentdate = dateconvert(keys[0])
enddate = dateconvert(keys[len(keys)-1])

d = datetime.timedelta(days=1)

f = open(fn, 'w', encoding="ISO-8859-1")
f.write("Datum")
for a in accounts:
	f.write(";Konto "+a)
f.write("\n")

while currentdate <= enddate:
	c = str(currentdate)
	if c in day:
		f.write(c)
		for a in accounts:
			if a in day[c]:
				f.write(";"+day[c][a])
				oldsaldo[a] = day[c][a]
			else:
				f.write(";"+oldsaldo[a])
		f.write("\n")
	currentdate += d
f.close()

print("Finished")
