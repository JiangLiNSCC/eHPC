from django.test import TestCase
from django.conf import settings
import json
from newt.tests import MyTestClient, newt_base_url, login
#from Cookie import SimpleCookie

class AuthTests(TestCase):
    fixtures = ["test_fixture.json"]

    def setUp(self):
        self.client = MyTestClient()

    def test_login(self):
        # Should not be logged in
        #print ( ' test not log in ? ')
        r = self.client.get(newt_base_url + "/auth")
        #print ('get ok ?' ,r.status_code )
        self.assertEquals(r.status_code, 200)
        json_response = r.json()
        #print ( 'json' ,  json_response  )
        self.assertEquals(json_response['output']['auth'], False)
        
        # Should be logged in
        r = self.client.post(newt_base_url + "/auth", data=login)
        self.assertEquals(r.status_code, 200)
        json_response = r.json()
        #print('cookies 1 : ' ,  self.client.cookies )
        self.assertEquals(json_response['output']['auth'], True)
        self.assertEquals(json_response['output']['username'], login['username'])
        cookies= self.client.cookies 
        # Loggen in self.client should return user info
        #print( 'session id :' , json_response["output"]["newt_sessionid"])
        #self.client.session['newt_sessionid'] =  json_response["output"]["newt_sessionid"]
        r = self.client.get(newt_base_url + "/auth" )
        self.assertEquals(r.status_code, 200)
        json_response = r.json()
        #print( 'cookies 2 : ' , self.client.cookies )
        self.assertEquals(json_response['output']['auth'], True)
        self.assertEquals(json_response['output']['username'], login['username'])


    def test_logout(self):
        # Should be logged in
        r = self.client.post(newt_base_url + "/auth", data=login)
        self.assertEquals(r.status_code, 200)
        json_response = r.json()
        self.assertEquals(json_response['output']['auth'], True)
        self.assertEquals(json_response['output']['username'], login['username'])

        r = self.client.delete(newt_base_url + "/auth")
        self.assertEquals(r.status_code, 200)
        json_response = r.json()
        self.assertEquals(json_response['output']['auth'], False)

        r = self.client.get(newt_base_url + "/auth")
        self.assertEquals(r.status_code, 200)
        json_response = r.json()
        self.assertEquals(json_response['output']['auth'], False)
