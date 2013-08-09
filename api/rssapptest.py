#--post request using curl
#curl -v  --user "a@b.com:a" --header "Accept:application/json"  --data "category=money" http://localhost:3000/category

import os
import rssapp
import unittest
import pymongo
import base64

class RssTestCase(unittest.TestCase):

    def setUp(self):
        rssapp.app.config['HTTP_PROXY'] = "http://www-proxy.au.oracle.com:80"
        rssapp.app.config['DATABASE_URI'] = "mongodb://localhost:27017/feedtest"		
        self.app = rssapp.app.test_client()
	self.email = 'a@b.com'
	self.pwd = 'pwd'

    def tearDown(self):
	c = pymongo.MongoClient( "mongodb://localhost:27017/feedtest")
	c["feedtest"].users.remove()
	c["feedtest"].feeds.remove()
	c.close()

    def test_root_uri(self):
        rv = self.app.get('/')
	#print "return value"
	#print rv
	#print rv.status_code
	#print rv.status
	#print rv.data
        assert 'root route' in rv.data


    def test_register(self):
	rv = self.app.post('/register', data=dict(email=self.email,pwd=self.pwd,name='a'))		
	print rv.status_code
	assert rv.status_code == 201

    #https://gist.github.com/jarus/1160696
    def open_with_auth(self, url, method,formdata):
	#http://werkzeug.pocoo.org/docs/test/#werkzeug.test.Client.open
	return self.app.open(url,
		method=method,
		data=formdata,
		headers={
		'Authorization': 'Basic %s' %  base64.b64encode('%s:%s'% (self.email, self.pwd))
		})

    def test_AuthRequired(self):
	rv = self.app.post('/category',data=dict(category='money'))
	self.assertTrue(rv.status_code==401)
	self.assertTrue('WWW-Authenticate' in rv.headers)
	self.assertTrue('Basic' in rv.headers['WWW-Authenticate'])


    def test_addcategory(self):
	rv = self.app.post('/register', data=dict(email=self.email,pwd=self.pwd,name='a'))
        assert rv.status_code == 201
	rv = self.open_with_auth('/category', 'POST',dict(category='fun'))
	print rv
	assert rv.status_code == 201	

    

		
if  __name__== '__main__':
	unittest.main()
