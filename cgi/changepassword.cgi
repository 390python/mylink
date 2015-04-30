#!/usr/bin/env python3


#import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting

import mysql.connector

import session


#Change password
def password_screen():
    html="""
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>MyLink</H2></center>

<H3>You may change your password here:</H3>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="changepassword.cgi">
<TR><TH>Old Password:</TH><TD><INPUT TYPE=text NAME="oldpass"></TD><TR>
<TR><TH>New Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
<TR><TH>Confirm Password:</TH><TD><INPUT TYPE=password NAME="confirm"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="change">
<INPUT TYPE=submit VALUE="Enter">
</FORM>
</BODY>
</HTML>
"""
    print_html_content_type()
    print(html)





def print_html_content_type():
        # Required header that tells the browser how to render the HTML.
    print("Content-Type: text/html\n\n")
    print('<link rel="stylesheet" href="bootstrap.min.css">')


###################################################################
# Define function to test the password.
def check_password(user, passwd):

    conn = mysql.connector.connect(user='root', password='!M@Y#S$Q%L', host='127.0.0.1', database='mylink')
    c = conn.cursor()

    t = (user,)
    c.execute('SELECT * FROM users WHERE email=%s', t)

    row = stored_password=c.fetchone()
    conn.close();

    if row != None:
      stored_password=row[1]
      if (stored_password==passwd):
         return "passed"

    return "failed"



##########################33
# Define function to change password in db
def change_password(user,passwd):
    conn = mysql.connector.connect(user='root', password='!M@Y#S$Q%L', host='127.0.0.1', database='mylink')
    c = conn.cursor()

    t = (user,)
    m = (passwd,)
    c.execute('UPDATE users SET password=%s WHERE email=%s', (passwd,user))
    conn.close();





##############################################################
# Define main function.
def main():
    form = cgi.FieldStorage()
    if "action" in form:
        action=form["action"].value
        #print("action=",action)
        if action == "change":
           password_screen()
           if "oldpass" in form and "password" in form and "confirm" in form:
               old=form["oldpass"].value
               pw=form["password"].value
               confirm=form["confirm"].value
               if check_password(username, password)=="passed":
                   if pw!=confirm:
                       print("<H3>Passwords do not match!</H3>")
                   else:
                       change_password(user,password)
                       print("<H3>Password successfully changed!</H3>")
    else:
        password_screen()
###############################################################
# Call main function.
main()
