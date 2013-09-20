import pymongo
from api import Feed,Notification,Helper
import conn, logging, sys, os,time,logging.handlers
from datetime import timedelta , datetime
import sys 

class Scheduleit():

	def setUp(self):
		fpath  = os.path.realpath(__file__)
		cfgfile = os.path.dirname(fpath) + '/dev.cfg'
		prxyval = Helper.getconfigvalue(cfgfile,'http_proxy',None)

		if prxyval is not None:
			self.prxydict = {'http_proxy':prxyval}
		else:
			self.prxydict = None
			
		dburl = Helper.getconfigvalue(cfgfile,'DATABASE_URI',None)
		dbname = Helper.getconfigvalue(cfgfile,'DBNAME',None)	
		self.db = pymongo.MongoClient(dburl)[dbname]
		self.feed = Feed()
		self.log = logging.getLogger('scheduleit')
		
	
	def schedule(self):
		if len(sys.argv) > 1 and sys.argv[1].lower()=='cron':
			self.log.info("Executing updateall at %s" % (datetime.now()))
			notobj = self.feed.updateall(self.db,self.prxydict)         
		else:
			while True:
				self.log.info("Executing updateall at %s" % (datetime.now()))
				notobj = self.feed.updateall(self.db,self.prxydict)
				time.sleep(10*60)

if __name__ == '__main__':
	
        if len(sys.argv) > 1 and sys.argv[1].lower()=='cron':
        	fpath  = os.path.realpath(__file__)
		handler = logging.handlers.RotatingFileHandler(os.path.dirname(fpath) + "/logs/cron-updateall.log", backupCount=50)        	
		logging.getLogger('api').addHandler(handler) 
		logging.getLogger('Feed').addHandler(handler)
		logging.getLogger('scheduleit').addHandler(handler)
        else:
		logging.basicConfig(stream=sys.stdout)
		
	logging.getLogger('api').setLevel(logging.DEBUG)
	logging.getLogger('Feed').setLevel(logging.DEBUG)
	logging.getLogger('scheduleit').setLevel(logging.INFO)		
	
	s = Scheduleit()
	s.setUp()
	s.schedule()
			

