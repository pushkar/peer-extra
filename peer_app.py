import os
import re
import csv
import json
import requests

class peer_api:
    base_url = ""
    apikey = ""
    data = {}
    add_student_url = "student/add/"
    get_student_url = "student/get/"
    update_student_url = "student/update/"
    add_submission_url = "submission/add/"
    add_review_url = "review/add"
    update_review_url = "review/update"
    get_review_url = "review/get"
    get_codework_url = "codework/get"
    update_codework_url = "codework/update"

    response = {}

    def __init__(self, base_url, key):
        self.base_url = base_url
        self.apikey = key

    def set_key(self, key):
        self.apikey = key

    def get_response(self):
        data = json.loads(self.response.content)
        return data

    def get_response_url(self):
        return self.response.url

    def add_student(self, data):
        self.data = data
        self.data['apikey'] = self.apikey
        url = self.base_url + self.add_student_url
        self.response = requests.get(url, params=self.data, headers=dict(Referer=url))
        if self.response.status_code != 200:
            print "Failed for "
            print self.response.url
        return self.response.status_code

    def get_student(self, username):
        self.data = {}
        self.data['apikey'] = self.apikey
        url = self.base_url + self.get_student_url + username
        self.response = requests.get(url, params=self.data, headers=dict(Referer=url))
        if self.response.status_code != 200:
            print "Failed for "
            print self.response.url
        return self.response.status_code

    def update_student(self, username, data):
        self.data = data
        self.data['apikey'] = self.apikey
        url = self.base_url + self.update_student_url + username
        self.response = requests.get(url, params=self.data, headers=dict(Referer=url))
        if self.response.status_code != 200:
            print "Failed for "
            print self.response.url
        return self.response.status_code

    # TODO: Bug! get_student not defined.
    def get_all_students(self):
        return get_student(self, "all")

    def add_submission(self, data):
        self.data = data
        self.data['apikey'] = self.apikey
        url = self.base_url + self.add_submission_url
        self.response = requests.get(url, params=self.data, headers=dict(Referer=url))
        if self.response.status_code != 200:
            print "Failed for "
            print self.response.url
        return self.response.status_code

    def add_review(self, data):
        self.data = data
        self.data['apikey'] = self.apikey
        url = self.base_url + self.add_review_url
        self.response = requests.get(url, params=self.data, headers=dict(Referer=url))
        if self.response.status_code != 200:
            print "Failed for "
            print self.response.url
        return self.response.status_code

    def update_review(self, data):
        self.data = data
        self.data['apikey'] = self.apikey
        url = self.base_url + self.update_review_url
        self.response = requests.get(url, params=self.data, headers=dict(Referer=url))
        if self.response.status_code != 200:
            print "Failed for "
            print self.response.url
        return self.response.status_code

    def get_review(self, data):
        self.data = data
        self.data['apikey'] = self.apikey
        url = self.base_url + self.get_review_url
        self.response = requests.get(url, params=self.data, headers=dict(Referer=url))
        if self.response.status_code != 200:
            print "Failed for "
            print self.response.url
        return self.response.status_code

    def get_codework(self, data, name, username):
        self.data = data
        self.data['apikey'] = self.apikey
        url = self.base_url + self.get_codework_url + "/" + name + "/" + username
        self.response = requests.get(url, params=self.data, headers=dict(Referer=url))
        if self.response.status_code != 200:
            print "Failed for "
            print self.response.url
        return self.response.status_code

    def update_codework(self, data, id):
        self.data = data
        self.data['apikey'] = self.apikey
        url = self.base_url + self.update_codework_url + "/" + id
        self.response = requests.get(url, params=self.data, headers=dict(Referer=url))
        if self.response.status_code != 200:
            print "Failed for "
            print self.response.url
        return self.response.status_code

class student_info:
    gtid = ""
    email = ""
    username = ""
    firstname = ""
    lastname = ""
    usertype = ""

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

    def set_email(self, e):
        self.email = e

    def set_type(self, t):
        self.usertype = t

    def get_dict(self, data):
        if self.username:
            data['username'] = self.username
        if self.gtid:
            data['gtid'] = self.gtid
        if self.email:
            data['email'] = self.email
        if self.firstname:
            data['firstname'] = self.firstname
        if self.lastname:
            data['lastname'] = self.lastname
        if self.usertype:
            data['usertype'] = self.usertype
        return data

class submission_info:
    username = ""
    assignment = ""
    server = ""
    files = {}

    def __init__(self):
        self.files.clear()

    def set_server(self, s):
        self.server = s

    def set_assignment(self, a):
        self.assignment = a

    def set_username(self, u):
        self.username = u

    def add_file(self, f_name, f_link):
        self.files[f_link] = f_name

    def total_files(self):
        return len(self.files)

    def get_dict(self, data):
        data['username'] = self.username
        data['assignment'] = self.assignment
        data['files'] = json.dumps(self.files)
        return data

class review_info:
    submission_username = None
    assigned_to_username = None
    assignment_short_name = None
    score = 0
    comments = ""

    def __init__(self):
        pass

    def set_assignment_by_short_name(self, assignment):
        self.assignment_short_name = assignment

    def set_submission_by_username(self, username):
        self.submission_username = username

    def set_assigned_to_by_username(self, username):
        self.assigned_to_username = username

    def set_score_and_comments(self, s, c):
        self.score = s
        self.comments = c

    def get_dict(self, data):
        data['assignment_short_name'] = self.assignment_short_name
        data['submission_username'] = self.submission_username
        data['assigned_to_username'] = self.assigned_to_username
        data['score'] = self.score
        data['comments'] = self.comments
        return data

class codework_info:
    username = None
    assignment_short_name = None
    score = 0
    comments = ""

    def __init__(self):
        pass

    def set_assignment_by_short_name(self, assignment):
        self.assignment_short_name = assignment
