import os
import re
import csv
from peer_app import *

conn = peer_api('http://127.0.0.1:8000/api/', 'abcd')

basedir = os.path.dirname(os.path.abspath(__file__))
print "Looking into " + basedir

student = {}
with open('roster_username.csv', 'rb') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        if len(row) == 3:
            s = row[0].strip().lower()
            sinfo = student_info()
            sinfo.set_email(s)
            sinfo.set_username(row[1].strip().lower())
            sinfo.set_type(row[2].strip().lower())
            student[s] = sinfo

with open('roster_gtid.csv', 'rb') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        if len(row) == 4:
            s = row[0].strip().lower()
            if student.has_key(s):
                sinfo = student[s]
                sinfo.set_gtid(row[1].strip().lower())
                sinfo.set_name(row[3].strip(), row[2].strip())

print "Student dictinary built with " + str(len(student)) + " items."

# Listing submission URLs
print "Writing to roster.csv"
with open('roster.csv', 'wb') as file:
    writer = csv.writer(file, delimiter=',')
    for s in student:
        data = {}
        student[s].get_dict(data)
        if conn.add_student(data) == 200:
            r = conn.get_response()
            if not r['error']:
                print r['message']
            else:
                print "Error! " + str(r['error'])
        else:
            print "Failed"
            break
        writer.writerow([student[s].username, s, student[s].gtid, student[s].usertype, student[s].lastname, student[s].firstname])

print "roster.csv created"
