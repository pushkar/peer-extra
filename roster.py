import os
import re
import csv
import sys
from peer_app import *

api_url = "http://rldm.herokuapp.com/api/"
api_key = "E3nl1gchwUT7qOTC2G77A7f2i5wcMZdf"

if len(sys.argv) < 2:
    print "Try: python " + sys.argv[0] + " <roster.csv>"
    sys.exit()

roster = sys.argv[1]

conn = peer_api(api_url, api_key)

basedir = os.path.dirname(os.path.abspath(__file__))
print "Looking into " + basedir

student = {}
with open(roster, 'rb') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        if len(row) == 5:
            username = row[0].strip().lower()
            gtid = row[1].strip().lower()
            lastname = row[2].strip()
            firstname = row[3].strip()
            email = row[4].strip().lower()
            sinfo = student_info()
            sinfo.set_username(username)
            sinfo.set_email(email)
            sinfo.set_gtid(gtid)
            sinfo.set_name(firstname, lastname)
            sinfo.set_type('student')
            student[username] = sinfo

print "Student dictinary built with " + str(len(student)) + " items."

for s in student:
    data = {}
    if conn.add_student(student[s].get_dict(data)) == 200:
        r = conn.get_response()
        if not r.has_key('error'):
            print r['message']
        else:
            print "Error! " + str(r['error'])
    else:
        print "Failed"
        break
