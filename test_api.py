import os
import unittest
from unittest import mock
from unittest.mock import Mock, patch
from flask import Flask, jsonify, request, Response, make_response
 
from app import *
from UserModel import User
from settings import *

import pytest
from flask import json


app.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
     
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/animal_db.sqlite'
        self.app = app.test_client()
        db.create_all()
         
     
    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

        
     
    ###############
    #### tests ####
    ###############
     
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_animals_page_no_auth(self):
        response = self.app.post('/animals', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    ## Helper defs ##

    def register(self):
        return self.app.post(
        '/register',
        data=json.dumps({"username": "user2111", "password": "TaTi21"}),
        headers={'Cache-Control': 'no-cache', 'Content-Type': 'application/json'}
        )
     
    def login(self, username, password):
        return self.app.post(
        '/login',
        data=dict(username=username, password=password),
        follow_redirects=True
        )

    def test_valid_user_registration(self):
        response = self.register()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"message":"User already exists"}\n', response.data)

if __name__ == "__main__":
    unittest.main()