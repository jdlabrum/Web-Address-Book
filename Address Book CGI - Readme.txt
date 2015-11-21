Address Book CGI - Readme

Start the server - localCGIserver.py, through the command prompt.

Using a web browser go to localhost:8080. 
This brings you to a screen with a link to the login page. 

At the login page the users are prompted for a username and password. 

Use 'Admin' for both the username and passord.
The login information is checked for a match in the logins.db file

If there is a match a cookie is created and the user is sent to the address book.
If there is not a match the page reloads with an Authentication Failed message. 

I tried to get the addressbook page to verifiy the cookie, but was unable to make this work. Are Cookies only good for the webpage they are created on?

In the end, I removed the cookie check so the addressbook page would load. I understand that this makes the Addressbook unsecure as the page will load if a user simply enters the Addressbook URL.

The address book is working. You can ADD, Delete and Update contacts. 