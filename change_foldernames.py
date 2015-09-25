import os
import re
import csv
from peer_app import *

conn = peer_api('http://127.0.0.1:8000/api/', 'abcd')

assignment = "supervised"
server_url = "7641/supervised/"
feedback_dir_original = "Feedback Attachment(s)"
submission_dir_original = "Submission attachment(s)"

basedir = os.path.dirname(os.path.abspath(__file__))
print "Looking into " + basedir

student = {}
with open('grades.csv', 'rb') as file:
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
    # Rename submission and feedback folder names
    feedback_dir = os.path.join(basedir, fn, feedback_dir_original)
    if os.path.isdir(feedback_dir):
        os.rename(feedback_dir, os.path.join(basedir, fn, "feedback"))

    submission_dir = os.path.join(basedir, fn, submission_dir_original)
    if os.path.isdir(submission_dir):
        os.rename(submission_dir, os.path.join(basedir, fn, "submission"))

    # Rename base folders
    r = re.search(r'^(.*), (.*)\(([^)]+)\)$', fn)

    if r:
        s = r.group(3).strip().lower()
        print s
        if student.has_key(s):
            dir_count = dir_count + 1
            dir_path = os.path.join(basedir, fn)
            if os.path.isdir(dir_path):
                print s
                os.rename(dir_path, os.path.join(basedir, student[s]))
        else:
            not_keyed.append(fn)

    else:
        not_regexed.append(fn)

print "Found " + str(dir_count) + " dirs."
print "\nThese were skipped:"
for n in not_regexed:
    print n,
print "\n\nNo key found for these:"
for n in not_keyed:
    print n

# Listing submission URLs
total_files_added = 0
total_students_added = 0
with open('submissions.csv', 'wb') as file:
    writer = csv.writer(file, delimiter=',')

    for fn in os.listdir(basedir):
        submission_dir = os.path.join(basedir, fn, "submission")
        if os.path.isdir(submission_dir):
            sub = submission_info()
            sub.set_server(server_url)
            sub.set_assignment(assignment)
            sub.set_username(fn)
            print "Submission for " + fn
            for n in os.listdir(submission_dir):
                f = server_url + fn + "/submission/" + n
                writer.writerow([fn, n, f])
                sub.add_file(n, f)
                print n, f
            total_files_added += sub.total_files()
            if sub.total_files() == 0:
                print "Skipping " + fn
            else:
                total_students_added += 1
                data = {}
                sub.get_dict(data)
                if conn.add_submission(data) == 200:
                    r = conn.get_response()
                    if not r['error']:
                        print r['message']
                    else:
                        print "Error! " + str(r['error'])
                else:
                    print "Failed"
                    break
            print "\n"

print str(total_files_added) + " submissions uploaded for " + str(total_students_added) + " students"
