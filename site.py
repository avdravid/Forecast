#!/usr/bin/env python3

import cgitb, cgi
cgitb.enable(display=0, logdir="/home/ubuntu/workspace/logs")
vals = cgi.FieldStorage();
print("Content-type: text/html\n")
try:
    destination = vals['site'].value;
except KeyError:
    destination = 'dashboard'
if destination == 'dashboard':
    site = open("../dashboard.html","r")
elif destination == 'search':
    site = open("../search.html", "r")
elif destination == 'settings':
    site = open("../settings.html", "r")
elif destination == 'user':
    site = open("../user.html","r")
else:
    site = open("../dashboard.html","r") 
print(site.read())