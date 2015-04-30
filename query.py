#!/usr/bin/env python3

import mysql.connector
conn = mysql.connector.connect(user='root', password='!M@Y#S$Q%L', host='127.0.0.1', database='mylink')

c = conn.cursor()

print
print ('Print all users')
c.execute("SELECT * FROM users")
rows = c.fetchall()
if rows is not None:
	for row in rows:
		print (row)
else:
	print ("No results")

print
print ("Print peter's password")
t = ('peter@gmail.com',)
c.execute('SELECT * FROM users WHERE email=%s', t)
print (c.fetchone()[1])

