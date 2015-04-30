#!/usr/bin/env python3

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting

import mysql.connector

import session

#important directories
IMAGEPATH="../images/"

##############################################################
# Define function to generate login HTML form.
def login_form():
    html="""
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>MyLink</H2></center>

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

##########################################################
# Diplay the options of admin
def display_admin_options(user, session):
    html="""
        <H1>MyLink</H1>
        <ul>
        <li> <a href="login.cgi?action=new-album&user={user}&session={session}">Create new album</a>
        <li> <a href="login.cgi?action=upload&user={user}&session={session}">Upload Picture</a>
        <li> <a href="login.cgi?action=show_image&user={user}&session={session}&image=user1/image-102.jpg">Show Image</a>
        <li> Delete album
        <li> Make album public
        <li> Change pasword
        </ul>
        """
        #Also set a session number in a hidden field so the
        #cgi can check that the user has been authenticated

    print_html_content_type()
    print(html.format(user=user,session=session))

#################################################################
def create_new_session(user):
    return session.create_session(user)

##############################################################
def new_album(form):
    #Check session
    if session.check_session(form) != "passed":
        return
        
    html="""
        <H1> New Album</H1>
        """
        
    conn = mysql.connector.connect(user='root', password='!M@Y#S$Q%L', host='127.0.0.1', database='mylink')
    c = conn.cursor()
    visibility = "private"
    if visibility in form:
        visibility = "public"

    user = form["user"].value
    sid = form["session"].value
    
    name = None;
    if "name" in form:    
        name = form["name"].value
        
    if name != None:
        t = (name,user,visibility,)
        c.execute('INSERT INTO albums VALUES (%s,%s,%s)', t)
        conn.commit()
        html = "<h1>Created album: " + name + '</h1><a href="login.cgi?action=home&user={user}&session={session}">Go home</a>'
    else:
        html="""
        <H1>New Album</H1>
        <form action="login.cgi" method="get">
        <input type="hidden" name="action" value="new-album" />
        <input type="hidden" name="user" value="{user}" />
        <input type="hidden" name="session" value="{session}" />
        Album name:<br>
        <input type="text" name="name">
        <br>
        <input type="checkbox" name="visibility" value="public">make it public<br>
        <br><br>
        <input type="submit" value="Submit">
        </form>
        <a href="login.cgi?action=home&user={user}&session={session}">Go home</a>
        """
        
    conn.close()
    print_html_content_type()
    print(html.format(user=user,session=sid));

##############################################################
def show_image(form):
    #Check session
    if session.check_session(form) != "passed":
       login_form()
       return

    fileName = form["image"].value
    username = form["user"].value
    # Your code should get the user album and picture and verify that the image belongs to this
    # user and this album before loading it
    conn = mysql.connector.connect(user='root', password='!M@Y#S$Q%L', host='127.0.0.1', database='mylink')
    c = conn.cursor()

    t = (fileName[fileName.rfind("/"):],)
    c.execute('SELECT * FROM pictures WHERE path=%s', t)
    row = c.fetchone()


    if row != None: 
        album=row[1]
        t = (album,)
        c.execute('SELECT * FROM albums WHERE name=%s', t)
        row = c.fetchone()
        if row != None:
            owner=row[1]		
            visibility=row[2]
            if ( visibility == "private" and owner != username ):
                fileName = "error.jpg"
        else:
            fileName = "error.jpg"
	
    conn.close();
    # Read image
    with open(IMAGEPATH+fileName, 'rb') as content_file:
       content = content_file.read()

    # Send header and image content
    hdr = "Content-Type: image/jpeg\nContent-Length: %d\n\n" % len(content)
    sys.stdout.buffer.write(bytes(hdr, 'UTF-8'))
    sys.stdout.buffer.write(content)


###############################################################################

def upload(form):
    if session.check_session(form) != "passed":
       login_form()
       return

    html="""
        <HTML>

        <FORM ACTION="login.cgi" METHOD="POST" enctype="multipart/form-data">
            <input type="hidden" name="user" value="{user}">
            <input type="hidden" name="session" value="{session}">
            <input type="hidden" name="action" value="upload-pic-data">
            <BR><I>Browse Picture:</I> <INPUT TYPE="FILE" NAME="file">
            <br>
            <input type="submit" value="Press"> to upload the picture!
            </form>
        </HTML>
    """

    user=form["user"].value
    s=form["session"].value
    print_html_content_type()
    print(html.format(user=user,session=s))

#######################################################

def upload_pic_data(form):
    #Check session is correct
    if (session.check_session(form) != "passed"):
        login_form()
        return

    #Get file info
    fileInfo = form['file']

    #Get user
    user=form["user"].value
    s=form["session"].value

    # Check if the file was uploaded
    if fileInfo.filename:
        # Remove directory path to extract name only
        fileName = os.path.basename(fileInfo.filename)
        open(IMAGEPATH+'/user1/test.jpg', 'wb').write(fileInfo.file.read())
        image_url="login.cgi?action=show_image&user={user}&session={session}".format(user=user,session=s)
        print_html_content_type()
        print('<H2>The picture ' + fileName + ' was uploaded successfully</H2>')
        print('<image src="'+image_url+'">')
    else:
        message = 'No file was uploaded'

def print_html_content_type():
	# Required header that tells the browser how to render the HTML.
    print("Content-Type: text/html\n\n")
    print('<link rel="stylesheet" href="bootstrap.min.css">')


##############################################################
# Define main function.
def main():
    form = cgi.FieldStorage()
    if "action" in form:
        action=form["action"].value
        #print("action=",action)
        if action == "login":
            if "username" in form and "password" in form:
                #Test password
                username=form["username"].value
                password=form["password"].value
                if check_password(username, password)=="passed":
                   session=create_new_session(username)
                   display_admin_options(username, session)
                else:
                   login_form()
                   print("<H3><font color=\"red\">Incorrect user/password</font></H3>")
        elif (action == "new-album"):
            new_album(form)
        elif (action == "upload"):
            upload(form)
        elif (action == "show_image"):
            show_image(form)
        elif action == "upload-pic-data":
            upload_pic_data(form)
        elif action == "home":
            username = form["user"].value
            sid = form["session"].value
            display_admin_options(username, sid)
        else:
            login_form()
    else:
        login_form()

###############################################################
# Call main function.
main()
