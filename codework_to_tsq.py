import os
import re
import csv
import sys

from peer_app import *

api_url = "http://rldm.herokuapp.com/api/"
api_key = "E3nl1gchwUT7qOTC2G77A7f2i5wcMZdf"

if len(sys.argv) < 3:
    print "Try: python " + sys.argv[0] + " <assignment_short_name> <grades.csv>"
    sys.exit()

assignment = sys.argv[1]
grades_filename = sys.argv[2]

conn = peer_api(api_url, api_key)

basedir = os.path.dirname(os.path.abspath(__file__))
print "Finding " + grades_filename + " in " + basedir

scores = {}

grade_file = os.path.join(basedir, grades_filename)
with open(grade_file, 'rb') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        if len(row) == 5:
            username = row[0].strip().lower()
            data = {}
            if conn.get_codework(data, assignment, username) == 200:
                r = conn.get_response()
                if not r['error']:
                    print r['message']
                    score = 0.0
                    for key in r['data']:
                        score += float( r['data'][key]['score'] )
                    scores[username] = score
                else:
                    print "Error! " + str(r['error'])
            else:
                print "Failed. Moving on."# + conn.get_response_url()
                #break

print "Writing to " + grades_filename
grade_file_out = os.path.join(basedir, "temp.csv")
with open(grade_file, 'rb') as file, open(grade_file_out, 'wb') as file_out:
    reader = csv.reader(file, delimiter=',')
    writer = csv.writer(file_out, delimiter=',')
    for row in reader:
        score = 0
        if len(row) == 5:
            username = row[0].strip().lower()
            if row[0] == "Display ID":
                score = "grade"
            if scores.has_key(username):
                score = scores[username]
                score = round(score, 1)
            writer.writerow([row[0], row[1], row[2], row[3], score])
        else:
            writer.writerow(row)

os.remove(grade_file)
os.rename(grade_file_out, grade_file)
