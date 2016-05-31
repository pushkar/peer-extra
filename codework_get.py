import os
import re
import csv
import sys

from peer_app import *

api_url = "http://rldm.herokuapp.com/api/"
api_key = "E3nl1gchwUT7qOTC2G77A7f2i5wcMZdf"

assignment = "hw4"

conn = peer_api(api_url, api_key)

students = {}

if conn.get_student("all") == 200:
    students = conn.get_response()['data']
    
for s in students:
    data = {}
    if conn.get_codework(data, assignment, s) == 200:
        mdp = conn.get_response()['data']
        print mdp
