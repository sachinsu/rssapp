from celery import Celery
from api import Feed
from pymongo import MongoClient

celery = Celery('rssapp.tasks',backend='mongodb://localhost:27017/celerystate',broker='mongodb://localhost:27017/celery')

@celery.task
def updatefeeds():
	feed= Feed()
	settings = {'http_proxy':'http://www-proxy.au.oracle.com:80'}
	db = MongoClient('mongodb://localhost:27017')['feedtest']
	feed.updateall(db,settings)

	
