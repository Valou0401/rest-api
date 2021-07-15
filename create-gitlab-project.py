#!/usr/bin/python3

import json 
import sys
import urllib
import requests
import os

#r=requests.post('http://root:rootroot@172.19.0.4/api/v4/projects?')
#print(r)
os.system('git init')
os.system('git add .')
os.system('git commit -m "push project"')
os.system('git push --set-upstream http://root:rootroot@172.19.0.4/root/testproject.git master')


