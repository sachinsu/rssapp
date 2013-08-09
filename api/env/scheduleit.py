import pymongo
from api import Feed,Notification
import conn, logging, sys, os,time
from datetime import timedelta , datetime

class Scheduleit():

	def setUp(self):
		self.db = pymongo.MongoClient("localhost",27017,safe=True).feedtest
		self.feed = Feed()
		self.log = logging.getLogger('scheduleit')
		self.prxydict = {'http_proxy':'http://www-proxy.au.oracle.com:80'}
	
	def schedule(self):
		while True:
			self.log.info("Excuting updateall at %s" % (datetime.now()))
			notobj = self.feed.updateall(self.db,self.prxydict)
			time.sleep(15*60)

if __name__ == '__main__':
	logging.basicConfig(stream=sys.stdout)
	logging.getLogger('api').setLevel(logging.DEBUG)
	logging.getLogger('Feed').setLevel(logging.DEBUG)
	s = Scheduleit()
	s.setUp()
	s.schedule()
			

