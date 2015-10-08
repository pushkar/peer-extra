import os
import re
import csv
import sys

from peer_app import *

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

assignment_short_name = "supervised"


if len(sys.argv) < 2:
    print "Try: python " + sys.argv[0] + " <folder_name>"
    sys.exit()

conn = peer_api('http://127.0.0.1:8000/api/', 'abcd')
#conn = peer_api('http://oms-fall2015.herokuapp.com/api/', 'abcd')

basedir = os.path.dirname(os.path.abspath(__file__))
basedir = os.path.join(basedir, sys.argv[1])

print "Looking into " + basedir

scores = {}
grade_file = os.path.join(basedir, "grades.csv")
with open(grade_file, 'rb') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        if len(row) == 5:
            s = row[1].strip().lower()
            s_val = row[0].strip().lower()
            score = row[4].lower()
            if len(s) > 0:
                scores[s_val] = score

with open('grading_assignments.csv', 'rb') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        if len(row) == 2:
            review = review_info()
            review.set_assignment_by_short_name(assignment_short_name)
            review.set_submission_by_username(row[0])
            review.set_assigned_to_by_username(row[1])

            submission_dir = os.path.join(basedir, row[0], "submission")
            if os.path.isdir(submission_dir):
                comments_file = os.path.join(basedir, row[0], "comments.txt")
                comments = ""
                with open(comments_file, 'rb') as file:
                    s = MLStripper()
                    s.feed(file.read())
                    comments = s.get_data()
                #print "Submission for " + row[0]
                #print "Score is " + scores[row[0]]
                #print comments
                #print "\n---------"
            if not scores.has_key(row[0]):
                continue
            review.set_score_and_comments(scores[row[0]], comments)

            data = {}
            data = review.get_dict(data)
            if conn.update_review(data) == 200:
                r = conn.get_response()
                if not r['error']:
                    print r['message']
                else:
                    print "Error! " + str(r['error'])
