import pymongo
from api import Feed,Notification,Helper
import conn, logging, sys, os,time
from datetime import timedelta , datetime

class Archiver():

	def setUp(self):
			
		dburl = Helper.getconfigvalue('dev.cfg','DATABASE_URI',None)
		dbname = Helper.getconfigvalue('dev.cfg','DBNAME',None)		

		self.db = pymongo.MongoClient(dburl)[dbname]
	
		self.feed = Feed()
		self.log = logging.getLogger('archiver')
	
	def schedule(self):
		 while True:
			self.log.info("Executing archiver at %s" % (datetime.now()))
			notobj = self.feed.archivefeeds(self.db,5)
			time.sleep(120*60)

if __name__ == '__main__':
	logging.basicConfig(stream=sys.stdout)
	logging.getLogger('api').setLevel(logging.DEBUG)
	logging.getLogger('Feed').setLevel(logging.DEBUG)
	logging.getLogger('archiver').setLevel(logging.DEBUG)	
	s = Archiver()
	s.setUp()
	s.schedule()
			

