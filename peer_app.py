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

    response = {}

    def __init__(self, base_url, key):
        self.base_url = base_url
        self.apikey = key

    def set_key(self, key):
        self.apikey = key

    def get_response(self):
        data = json.loads(self.response.content)
        return data

    def add_student(self, data):
        self.data = data
        self.data['apikey'] = self.apikey
        url = self.base_url + self.add_student_url
        self.response = requests.get(url, params=self.data, headers=dict(Referer=url))
        if self.response.status_code != 200:
            print self.response.content
        return self.response.status_code

    def get_student(self, username):
        self.data = {}
        self.data['apikey'] = self.apikey
        url = self.base_url + self.get_student_url + username
        self.response = requests.get(url, params=self.data, headers=dict(Referer=url))
        if self.response.status_code != 200:
            print self.response.content
        return self.response.status_code

    def get_all_students(self):
        return get_student(self, "all")

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
        data['username'] = self.username
        data['gtid'] = self.gtid
        data['email'] = self.email
        data['firstname'] = self.firstname
        data['lastname'] = self.lastname
        data['usertype'] = self.usertype
        return data
