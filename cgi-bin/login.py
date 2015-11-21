#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import os.path
import sqlite3
import http.cookies, os, time
import uuid #universally unique identifier
import hashlib
cgitb.enable() #enable cgi traceback for debugging

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
error = ""
userName = ""
password = ""
check = 0

print("Content-type:text/html")
print()

def CreateAddressBookTable():
        sql = '''CREATE TABLE IF NOT EXISTS logins (UserName text, Password text, ID integer PRIMARY KEY AUTOINCREMENT)'''
        curse.execute(sql)
        conn.commit()

def bSearch(userName):
            name = (userName,)
            sql = '''SELECT * FROM logins where UserName = ?'''
            curse.execute(sql, name)
            rows = curse.fetchall()
            if rows:
                print("Username Found")
                for row in rows:
                    if password == row[1]:
                        print("Password Matches")
                        html = ''
                        html +=  '<html><head>'
                        #print('''<meta http-equiv="refresh" content="0;URL='http://localhost:8000/cgi-bin/AddressBook.py'" />''')  
                        html += '</head>'


                        html += '<body>'
                        html += '<p>Server time is ' + str(time.asctime(time.localtime())) + '</p>'
                        #print(cookie.output())
                        cookie_string = os.environ.get('HTTP_COOKIE')
                        #print("cookie-string: ", cookie_string)
                        # The first time the page is run there will be no cookie sent from the client
                        if not cookie_string:
                            html += '<p>First visit or cookies disabled</p>'
                            now = time.time() #get the time in seconds since the epoch
                            cookie = http.cookies.SimpleCookie() #create a simple cookie
                            cookie['lastvisit'] = str(now) #set a cookie value with lastvisit as a key

                            # The returned cookie is available in the os.environ dictionary

                            cookie['sid'] = uuid.uuid4().hex

                            #throws and CookieError... valid keys are: expires, path, comment, domain, max-age, secure, version, httponly
                            #cookie['lastvisit']['bla'] = 'bla' # bla is not a valid key

                            cookie['lastvisit']['expires'] = now + (30*60) #set the date time when the cookie expires
                            cookie['lastvisit']['httponly'] = 1
                            print(cookie.output())

                        html = ''
                        html +=  '<html><head>'
                        html += '''<meta http-equiv="refresh" content="0;URL='../cgi-bin/AddressBook.py'" />'''
                        html += '<script></script>'
                        html += '</head>'
                        html += '<body>'
                        html += "<p>This page is restricted and need authentication to access it!</p>"
                        print(html)
                    else:
                        print("Password Incorrect")
                
            else:
                print("Authentication Failed. Please Try Again.")
            

if form:
    userName = form.getvalue('userName')
    password  = form.getvalue('password')
    
    if len(userName)>0 and len(password)>0:
        conn = sqlite3.connect('logins.db')
        curse = conn.cursor()
        CreateAddressBookTable()
        bSearch(userName)



html = """<html>
    <head>
        <title>Login</title>
        <link rel="stylesheet" href="../style.css" />
    </head>
    
    <body>
        <h2>Welcome to the Internet Address Book</h2>
        <p1>Please enter your username and password.</p1>
        <h3>%s</h3>

        <form action="/cgi-bin/login.py" method="get">
        User Name:<input type="text" style="margin-left: 10px;" name="userName">  <br />

        Password:<input type="text" style="margin-left: 18px;" name="password" />
        <input type="submit" value="Submit" />
        </form>
    </body>
    </html>
    """%(error)
print(html)
