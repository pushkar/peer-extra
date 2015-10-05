import os
import re
import csv
import sys

from peer_app import *
assignment_short_name = "supervised"

if len(sys.argv) < 2:
    print "Try: python " + sys.argv[0] + " <csv_file>"
    sys.exit()

conn = peer_api('http://127.0.0.1:8000/api/', 'abcd')

basedir = os.path.dirname(os.path.abspath(__file__))
basedir = os.path.join(basedir, sys.argv[1])

print "Looking into " + basedir

with open('grading_assignments.csv', 'rb') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        if len(row) == 2:
            review = review_info()
            review.set_assignment_by_short_name(assignment_short_name)
            review.set_submission_by_username(row[0])
            review.set_assigned_to_by_username(row[1])

            data = {}
            data = review.get_dict(data)
            if conn.add_review(data) == 200:
                r = conn.get_response()
                if not r['error']:
                    print r['message']
                else:
                    print "Error! " + str(r['error'])
