import os
import re
import csv
import sys

from peer_app import *

if len(sys.argv) < 2:
    print "Try: python " + sys.argv[0] + " <folder_name>"
    sys.exit()

conn = peer_api('http://127.0.0.1:8000/api/', 'abcd')
#conn = peer_api('http://oms-fall2015.herokuapp.com/api/', 'abcd')

assignment = "randomized"
server_url = "http://cs7641-fall2015.robotvisions.org/assignment/"
feedback_dir_original = "Feedback Attachment(s)"
submission_dir_original = "Submission attachment(s)"

basedir = os.path.dirname(os.path.abspath(__file__))
basedir = os.path.join(basedir, sys.argv[1])

print "Looking into " + basedir

student = {}
student_scores = {}
grade_file = os.path.join(basedir, "grades.csv")
grade_file_out = os.path.join(basedir, "grades_out.csv")

with open(grade_file, 'rb') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        if len(row) == 5:
            s = row[1].strip().lower()
            s_val = row[0].strip().lower()
            if len(s) > 0:
                student[s] = s_val

print "Student dictinary built with " + str(len(student)) + " items."

not_regexed = []
not_keyed = []
dir_count = 0
for fn in os.listdir(basedir):
    # Find comments file
    comments_file = os.path.join(basedir, fn, "comments.txt")
    # Rename base folders
    r = re.search(r'^(.*), (.*)\(([^)]+)\)$', fn)

    if r:
        s = r.group(3).strip().lower()
        if student.has_key(s):
            ri = review_info()
            ri.set_submission_by_username(student[s])
            ri.set_assignment_by_short_name(assignment)
            data = {}
            if conn.get_review(ri.get_dict(data)) == 200:
                r = conn.get_response()
                if not r['error']:
                    # Deal with reviews and convos here
                    if r.has_key('reviews') and r.has_key('convos'):
                        for review_pk, review in r['reviews'].iteritems():
                            if str(review['assigned_usertype']) == 'ta':
                                ta_pk = review_pk
                                student_scores[s] = review['score']
                                print "Looking into Review " + str(review_pk)
                                print "Score is " + str(review['score'])

                        if r['convos'].has_key(ta_pk):
                            comments = open(comments_file, 'w')
                            comments.write("You can find your feedback here: " + server_url + assignment + "/?review=" + str(ta_pk))
                            # I had to comment this out because of how t-sq imports comments! Removes my \n and br
                            #for user_pk, conv in r['convos'][ta_pk].iteritems():
                                #comments.write("\n\n----------------------\n\n")
                                #comments.write(conv['text'].replace('\n', '<br />'))
                                #comments.write("\n\n----------------------\n\n")
                            comments.close()
                else:
                    print "Error! " + str(r['error'])
            else:
                print "Failed"
                break
        else:
            not_keyed.append(fn)

    else:
        not_regexed.append(fn)

with open(grade_file, 'rb') as file, open(grade_file_out, 'wb') as file_out:
    reader = csv.reader(file, delimiter=',')
    writer = csv.writer(file_out, delimiter=',')
    for row in reader:
        score = 0
        if len(row) == 5:
            s = row[1].strip().lower()
            s_val = row[0].strip().lower()
            if len(s) > 0:
                student[s] = s_val
            if student_scores.has_key(s):
                score = student_scores[s]
            if row[0] == "Display ID":
                score = "grade"
            writer.writerow([row[0], row[1], row[2], row[3], score])
        else:
            writer.writerow(row)

print "Found " + str(dir_count) + " dirs."
print "\nThese were skipped:"
for n in not_regexed:
    print n,
print "\n\nNo key found for these:"
for n in not_keyed:
    print n
