#!/usr/bin/env python3

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting

import mysql.connector


##############################################################
# Define function to generate register HTML form.
def register_form():
    html="""
<HTML>
<HEAD>
<TITLE>Register Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>Sign up!</H2></center>

<H3>Type User and Password:</H3>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="register.cgi">
<TR><TH>Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="confirm"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="register">
<INPUT TYPE=submit VALUE="Enter">
</FORM>
</BODY>
</HTML>
"""
    print_html_content_type()
    print(html)



#############################
# Register Form WITH PASSWORD ERROR

def register_form_with_error():
    html="""
<HTML>
<HEAD>
<TITLE>Register Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>Sign up!</H2></center>

<H3>Type User and Password:</H3>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="register.cgi">
<TR><TH>Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="confirm"></TD></TR>
</TABLE>
<BODY>Error: Password Do Not Match!</BODY>
<BR>
<INPUT TYPE=hidden NAME="action" VALUE="register">
<INPUT TYPE=submit VALUE="Enter">
</FORM>
</BODY>
</HTML>
"""
    print_html_content_type()
    print(html)




def register_form_with_erroruser():
    html="""
<HTML>
<HEAD>
<TITLE>Register Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>Sign up!</H2></center>

<H3>Type User and Password:</H3>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="register.cgi">
<TR><TH>Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="confirm"></TD></TR>
</TABLE>
<BODY>Error: User already exists!!</BODY>
<BR>
<INPUT TYPE=hidden NAME="action" VALUE="register">
<INPUT TYPE=submit VALUE="Enter">
</FORM>
</BODY>
</HTML>
"""
    print_html_content_type()
    print(html)



##############################################################
# Define content type function.
def print_html_content_type():
	# Required header that tells the browser how to render the HTML.
	print("Content-Type: text/html\n\n")



###################################################################
# Define function to test the password.
#def check_user(user):

#    conn = mysql.connector.connect(user='root', password='!M@Y#S$Q%L', host='127.0.0.1', database='mylink')
#    c = conn.cursor()

#    t = (user,)
    
#    c.execute("SELECT * FROM users WHERE email=%s", t)

#    rows = c.fetchall()
#    newtmp = ','.join(str(x) for x in rows)
#    conn.close();
#    tmp = open("tmp.txt","w")
#    for row in newtmp:
        #tmp.writerow(row)
        #print>>tmp,row[0]i
#        tmp.write = row
        #tmp.close()
#        if row==user:
#            return "exists"
#    if row != None:
 #     stored_user=row[0]
  #    if (stored_userd != None):
  #       return "passed"

#    return "notexist"



#Login page successful
def login_page_success():
    html="""
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>MyLink</H2></center>
<H1>You may now login!</H1>
<H3>Type User and Password:</H3>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="login.cgi">
<TR><TH>Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="login">
<INPUT TYPE=submit VALUE="Enter">
</FORM>
</BODY>
</HTML>
"""
    print_html_content_type()
    print(html)



###############
# Create User
def register_user(username,password):
    conn = mysql.connector.connect(user='root', password='!M@Y#S$Q%L', host='127.0.0.1', database='mylink')
    c = conn.cursor()
    c.execute('INSERT INTO users VALUES (%s,%s,%s)',(username,password,"test"))
    conn.commit()
# conn.commit()
    conn.close()
    login_page_success()



##############################################################
# Define main function.
def main():
    form = cgi.FieldStorage()
    if "action" in form:
        action=form["action"].value
        #print("action=",action)
        if action == "register":
            username=form["username"].value
            password=form["password"].value
            confirm=form["confirm"].value
            if confirm == password:
                register_user(username,password)
                #register_form()
                #if check_user(username)=="notexist":
                #    register_user(username,password)
                #else:
                #    register_form_with_erroruser()
            else:
                register_form_with_error()
    else:
        register_form()

###############################################################
# Call main function.
main()
