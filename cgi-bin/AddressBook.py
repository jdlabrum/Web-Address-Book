'''
Joseph Labrum
CSCI310 - Final
Web based address book. 
'''

import cgi, cgitb #cgi trace back
import sqlite3
import http.cookies, os, time
import uuid #universally unique identifier
import hashlib


cgitb.enable()

dbConnection = sqlite3.connect('CGIAddressBook.db') #create a connection
dbCursor = dbConnection.cursor()

def GetHeader():
	header = """
		<!DOCTYPE html>
		<html>
			<head>
			<meta charset="utf-8">
				<script>
				
				</script>
				<title>Address Book</title>
				<link rel="stylesheet" href="../style.css" />	
			</head>
			<body>
				<header> 
					<div class="headertext1" style="margin-left:180;">Welcome To Your Address Book </div>
				</header>
			
			<menu>
			</menu>
				<h2 style="padding-left:200;">Contact Manager</h2>
				<a href="AddressBook.py" style="padding-left:200;">Add New</a>
				<hr>
			"""
	return header
	
				
def CreateAddressBookTable():
	global dbConnection, dbCursor
	
	sql = '''CREATE TABLE IF NOT EXISTS AddressBook (FirstName text, LastName text, Phone text)'''
	dbCursor.execute(sql)
	dbConnection.commit()

	
def Add(firstName, lastName, phone):
	global dbConnection, dbCursor
	
	#Insecure way!!! Do not do the following as it'll result into injection vulnerability
	#sql = '''INSERT INTO AddressBook (FirstName, LastName, Phone) VALUES ('%s', '%s', '%s')'''%('a', 'b', 'c\'); drop table AddressBook--')
	#dbCursor.execute(sql)
		
	#secure parameterized way
	sql = '''INSERT INTO AddressBook (FirstName, LastName, Phone) VALUES (?,?,?)'''
	dbCursor.execute(sql, (firstName, lastName, phone))
		
	dbConnection.commit() #must save/commit the changes or will be lost if the connection is closed.

def Update(rowid, firstName, lastName, phone):
	global dbConnection, dbCursor
	
	#Insecure way!!! Do not do the following as it'll result into injection vulnerability
	#sql = '''UPDATE AddressBook SET FirstName='%s', LastName='%s', Phone='%s' where rowid=%d'''%(firstName, lastName, phone, rowid)
	#dbCursor.execute(sql)
		
	#secure way
	sql = '''UPDATE AddressBook SET FirstName=?, LastName=?, Phone=? where rowid=?'''
	dbCursor.execute(sql, (firstName, lastName, phone, rowid))
		
	dbConnection.commit() #must save/commit the changes or will be lost if the connection is closed.

def GetAllContacts(searchText=""):
	global dbConnection, dbCursor
	html = ""

	if searchText:
		sql = '''SELECT rowid, FirstName, LastName, Phone FROM AddressBook where FirstName like ? or LastName like ? order by FirstName'''
		dbCursor.execute(sql, (searchText, searchText))
	else:
		sql = "SELECT rowid, FirstName, LastName, Phone FROM AddressBook order by FirstName"
		dbCursor.execute(sql)
	
	rows = dbCursor.fetchall()
	if rows:
		if searchText:
			html += '<h2>Your Search Resulted the Following Contacts!</h2>'
		else:
			html += '<h2 style="padding-left:200;">All Contacts</h2>'
			
		html += '<table>'
		html += '<tr><th style="margin-left:-10;">First Name</th><th>Last Name</th><th>Phone</th><th colspan="2" width="20%">Tools</th></tr>'
		for row in rows:
			html += '''
				<tr>
				<td>%s</td><td>%s</td><td>%s</td>
				<td><a href="AddressBook.py?edit=%s">Edit</a></td>
				<td><a href="AddressBook.py?delete=%s">Delete</a></td>
				</tr>
				'''%(row[1], row[2], row[3], row[0], row[0])
		
		html += '</table>'
	else:
		if searchText:
			html += '<h2>Your Search Resulted 0 Contacts!</h2>'
		else:
			html += '<div class="info" style="padding-laft:200;">No Contacts Found in the Database!</div>'
			
	html += '<hr><br />'
	return html
		
	
def GetContactDetails(rowid):
	global dbConnection, dbCursor

	sql = "SELECT FirstName, LastName, Phone FROM AddressBook where rowid=? order by FirstName"
	dbCursor.execute(sql, (rowid,))
	
	row = dbCursor.fetchone()
	if row:
		return GetForm(firstName=row[0], lastName=row[1], phone=row[2], rowid=rowid, disabled='save')
	else:
		return GetForm()
	
	

def GetForm(firstName="", lastName="", phone="", rowid='', disabled='edit'):
	
	html = """
				<form action="" method="post">
					<table>
						<tr>
							<td><label for="txtFName">First Name:</label></td>
							<td><input type="text" name="txtFName" value="{firstName}" required></td>
						</tr>
						<tr>
							<td><label for="txtLName">Last Name:</label></td>
							<td><input type="text" name="txtLName" value="{lastName}" required></td>
						</tr>
						<tr>
							<td><label for="txtPhone">Phone #:</label></td>
							<td><input type="text" name="txtPhone" value="{phone}" required></td>
						</tr>
					</table>
					<hr>
					<input type="hidden" value="{rowid}" name="rowid">
			"""
			
	html = html.format(**locals())
	
	if disabled == 'save':
		html += '''<input type="submit" style="margin-left:200;" value="Save" name="save" disabled>
					<input type="submit" value="Update" name="update">
				'''
	else:
		html += '''<input type="submit"  style="margin-left:200;" value="Save" name="save">
					<input type="submit" value="Update" name="update" disabled>
				'''
				
	html += '''
				<hr>
			</form>
			'''

	return html
	
def main():
	global dbConnection, dbCursor
	CreateAddressBookTable()
	form = cgi.FieldStorage() #Create instance of FieldStorage
	
	firstName = form.getvalue('txtFName')
	lastName = form.getvalue('txtLName')
	phone = form.getvalue('txtPhone')
	html = GetHeader()
	rowid = form.getvalue('rowid', '0')

	if form.getvalue('save'):
		Add(firstName, lastName, phone)
		html += GetAllContacts()
		html += '<div class="info" style="padding-left:200;">Contact added successfully!</div>'
		
	elif form.getvalue('edit') and not form.getvalue('update'):
		html += GetAllContacts()
		rowid = form.getvalue('edit')
		
	elif form.getvalue('update'):
		Update(rowid, firstName, lastName, phone)
		html += GetAllContacts()
		html += '<div class="info" style="padding-left:200;">Contact updated successfully!</div>'
		
	elif form.getvalue('delete'):
		sql = "DELETE FROM AddressBook WHERE rowid=?"
		dbCursor.execute(sql, (form.getvalue('delete'),))
		dbConnection.commit()
		rowid = '1000'
		html += GetAllContacts()

	else:
		html += GetAllContacts()
		
	html += GetContactDetails(rowid)
	
	print('content-type: text/html\n\n')
	
	print(form.keys())
	#print str(form.values())
	print(html)
	dbConnection.close()
	
	#print form.getvalue('txtFName')
	#print str(form)
	
if __name__ == "__main__":
	main()
	#pass
	
