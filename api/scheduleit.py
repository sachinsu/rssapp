import pymongo
from api import Feed,Notification,Helper
import conn, logging, sys, os,time
from datetime import timedelta , datetime

class Scheduleit():

	def setUp(self):
		prxyval = Helper.getconfigvalue('dev.cfg','http_proxy',None)
		
		if prxyval is not None:
			self.prxydict = {'http_proxy':prxyval}
		else:
			self.prxydict = None
			
		dburl = Helper.getconfigvalue('dev.cfg','DATABASE_URI',None)
		dbname = Helper.getconfigvalue('dev.cfg','DBNAME',None)		

		self.db = pymongo.MongoClient(dburl)[dbname]
		self.feed = Feed()
		self.log = logging.getLogger('scheduleit')
		
	
	def schedule(self):
		while True:
			self.log.info("Executing updateall at %s" % (datetime.now()))
			notobj = self.feed.updateall(self.db,self.prxydict)
			time.sleep(10*60)

if __name__ == '__main__':
	logging.basicConfig(stream=sys.stdout)
	logging.getLogger('api').setLevel(logging.DEBUG)
	logging.getLogger('Feed').setLevel(logging.DEBUG)
	s = Scheduleit()
	s.setUp()
	s.schedule()
			

