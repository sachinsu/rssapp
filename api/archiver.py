import pymongo
from api import Feed,Notification,Helper
import conn, logging, sys, os,time,logging.handlers
from datetime import timedelta , datetime
import sys

class Archiver():

	def setUp(self):
			
		dburl = Helper.getconfigvalue('dev.cfg','DATABASE_URI',None)
		dbname = Helper.getconfigvalue('dev.cfg','DBNAME',None)		

		self.db = pymongo.MongoClient(dburl)[dbname]
	
		self.feed = Feed()
		self.log = logging.getLogger('archiver')
	
	def schedule(self):
		if len(sys.argv) > 1 and sys.argv[1].lower()=='cron':
			self.log.info("Executing archiver at %s" % (datetime.now()))
                        notobj = self.feed.archivefeeds(self.db,5)               		
		else:
			while True:
				self.log.info("Executing archiver at %s" % (datetime.now()))
				notobj = self.feed.archivefeeds(self.db,5)
				time.sleep(120*60)

if __name__ == '__main__':

        if len(sys.argv) > 1 and sys.argv[1].lower()=='cron':
		handler = logging.handlers.RotatingFileHandler("logs/cron-archiver.log", backupCount=50)
                logging.getLogger('api').addHandler(handler)
                logging.getLogger('Feed').addHandler(handler)
                logging.getLogger('archiver').addHandler(handler)
        else:
               logging.basicConfig(stream=sys.stdout)
        
	logging.getLogger('api').setLevel(logging.DEBUG)
	logging.getLogger('Feed').setLevel(logging.DEBUG)
	logging.getLogger('archiver').setLevel(logging.DEBUG)	
	s = Archiver()
	s.setUp()
	s.schedule()
			

