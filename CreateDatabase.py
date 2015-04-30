#!/usr/bin/env python3

import mysql.connector
conn = mysql.connector.connect(user='root', password='!M@Y#S$Q%L', host='127.0.0.1', database='mylink')

c = conn.cursor()

# Create users table
c.execute('''CREATE TABLE users
	     (email VARCHAR(256) NOT NULL, 
	      password VARCHAR(256) NOT NULL,
		  username VARCHAR(256),
	      PRIMARY KEY(email))''')

# Create album table
# Visibility is 'public' or 'private'
c.execute('''CREATE TABLE albums
	     (name VARCHAR(256) NOT NULL,
	      owner VARCHAR(256) NOT NULL,
	      visibility VARCHAR(256) NOT NULL,
	      FOREIGN KEY (owner) REFERENCES users(email),
	      PRIMARY KEY(name, owner))''')

# Create pictures table
c.execute('''CREATE TABLE pictures
	     (path VARCHAR(256) NOT NULL,
	      album VARCHAR(256) NOT NULL,
	      owner VARCHAR(256) NOT NULL,
	      FOREIGN KEY(album, owner) REFERENCES albums(name, owner),
	      FOREIGN KEY(owner) REFERENCES users(email),
	      PRIMARY KEY(path))''')

# Create sessions table
c.execute('''CREATE TABLE sessions
	     (user VARCHAR(256) NOT NULL,
	      session VARCHAR(256) NOT NULL,
	      FOREIGN KEY(user) REFERENCES users(email),
	      PRIMARY KEY(session))''')
          
# Create friends table
# confirmed is if the request has been accepted. 0 is the default and means not accepted
c.execute('''CREATE TABLE friends
	     (id INT NOT NULL AUTO_INCREMENT,
          requester VARCHAR(256) NOT NULL, 
	      receiver VARCHAR(256) NOT NULL,
		  confirmed INT NOT NULL DEFAULT 0,
	      PRIMARY KEY(id))''')
          
# Create circles table
c.execute('''CREATE TABLE circles
	     (name VARCHAR(256) NOT NULL,
	      circle VARCHAR(256) NOT NULL,
	      PRIMARY KEY(name, circle))''')
          
# Create posts table
c.execute('''CREATE TABLE posts
	     (id INT NOT NULL AUTO_INCREMENT,
          owner VARCHAR(256) NOT NULL,
          circle VARCHAR(256),
          text VARCHAR(256) NOT NULL,
	      PRIMARY KEY(id))''')


# Save the changes
conn.commit()

# Close the connection
conn.close()
