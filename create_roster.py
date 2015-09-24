import os
import re
import csv

class student_info:
    gtid = ""
    username = ""
    firstname = ""
    lastname = ""
    type = ""

    def __init__(self):
        pass

    def check():
        if len(self.gtid) <= 0 or len(self.username) <= 0:
            return False
        else:
            return True

    def set_username(self, u):
        self.username = u

    def set_gtid(self, g):
        self.gtid = g

    def set_name(self, f, l):
        self.firstname = f
        self.lastname = l

    def set_type(self, t):
        self.type = t

basedir = os.path.dirname(os.path.abspath(__file__))
print "Looking into " + basedir

student = {}
with open('roster_username.csv', 'rb') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        if len(row) == 3:
            s = row[0].strip().lower()
            sinfo = student_info()
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
        writer.writerow([student[s].username, s, student[s].gtid, student[s].type, student[s].lastname, student[s].firstname, 0])

print "roster.csv created"
