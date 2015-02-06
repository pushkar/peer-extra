import os
import re
import csv

base_url = "http://54.163.244.26/7641/supervised/"
feedback_dir_original = "Feedback Attachment(s)"
submission_dir_original = "Submission attachment(s)"

basedir = os.path.dirname(os.path.abspath(__file__))
print "Looking into " + basedir

student = {}
with open('roster.csv', 'rb') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        if len(row) == 7:
            s = row[4].strip().lower() + row[5].strip().lower()
            student[s] = row[0]

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
        s = r.group(1).strip().lower() + r.group(2).strip().lower()
        if student.has_key(s):
            dir_count = dir_count + 1
            dir_path = os.path.join(basedir, fn)
            if os.path.isdir(dir_path):
                os.rename(dir_path, os.path.join(basedir, student[s]))
        else:
            not_keyed.append(fn)

    else:
        not_regexed.append(fn)

print "Found " + str(dir_count) + " dirs."
print "These were skipped:"
print not_regexed
print "No key found for these:"
print not_keyed

# Listing submission URLs
with open('submissions.csv', 'wb') as file:
    writer = csv.writer(file, delimiter=',')

    for fn in os.listdir(basedir):
        submission_dir = os.path.join(basedir, fn, "submission")
        if os.path.isdir(submission_dir):
            for n in os.listdir(submission_dir):
                f = base_url + fn + "/submission/" + n
                writer.writerow([fn, n, f])
