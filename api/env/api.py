#from flask import Flask
#from flask.ext.restful import reqparse, abort, Api, Resource
import json, logging
import feedparser, urllib2
import time
from datetime import datetime
"""
- Users {
	id : <email>,
	name : string,
	pwd : string,
	categories : [],
	subs :[
		{
		_id: <url>,
		unreadcount: integer,
		category: string,
		items :{
		  	<feeditem_id> : {
			isread : boolean,
			isstarred : boolean,
		  }	
		}
	]
- Feeds {
	_id : <url>,
	title: string,
	items : [{
		_id: <objectid>,
		link: string,
		title: string,
		summary (content): string,
		published_date: number,
	}]
}
"""
class User(object):
	def __init__(self):
		self.log  = logging.getLogger(__name__)

	def login(self,db,email,pwd):
		resultobj = Notification()
		# mandatory: email,name,pwd
		self.log.info("User login for %s",email)
		try:
			resultobj.result = db.users.find_one({'_id':email,'pwd':pwd},{'subs':0})
		except Exception, err:
			self.log.error("User login failed %s" , str(err))
			raise

		return resultobj
		
	def save(self,db,email,name,pwd):
		resultobj = Notification()
		# mandatory: email,name,pwd
		self.log.info("Saving user %s, %s",email,name)
		Validators.check_required(email,"E-mail",resultobj)
		Validators.validate_email(email,"E-mail",resultobj)
		Validators.check_required(name,"Name/pwd",resultobj)
		
		if name == pwd:
			resultobj.adderror("Name/pwd is not valid")
		
		if not resultobj.haserrors:
			try:
				# check any error during update
				db.users.update({'_id':email},{'$set':{'name':name,'pwd':pwd,'categories':[],'subs':[]}},upsert=True)
			except Exception, err:
				self.log.error("User saving failed %s" , str(err))
				raise
				
		return resultobj

	def getcategorylist(self,db,email):
		self.log.info("Get list of categories for %s", email)
		res = Notification()
		try:
			catlist=[]
			cats = db.users.find({'_id':email},{'categories':1,'_id':0})
			if cats is not None:
				for category in cats[0]['categories']:
					catlist.append(category)
							
			res.setdata(False,None,catlist)
		except Exception,err:
			self.log.error("Getting category list failed %s", str(err))
			raise

		return res
			
	def addcategory(self,db,email,category):
		self.log.info("Adding category %s,%s", email, category)
		
		res = Notification()
		# mandatory: email
		Validators.check_required(email,"E-mail",res)
		Validators.validate_email(email,"E-mail",res)
		Validators.check_required(category,"Category",res)
		
		# catch any error during update
		if not res.haserrors:
			try:
#				print list(db.users.find())
				db.users.update({'_id':email},{'$addToSet':{'categories':category}},upsert=False)
			except Exception, err:
				self.log.error("Category addition failed %s", str(err))
				raise

		return res			
	
	def removecategory(self,db,email,category):
		self.log.info("Removing category %s,%s", email, category)

		res = Notification()
		# mandatory: email
		Validators.check_required(email,"E-mail",res)
		Validators.check_required(category,"Category",res)
		
		# catch any error during update
		if not res.haserrors:
			try:
#				print list(db.users.find())
				db.users.update({'_id':email,'subs.category':category},{'$pull':{'categories':category},'$unset':{'subs.$.category':category}})
			except Exception, err:
				self.log.error("Category removal failed %s", str(err))
				raise

		return res			
	
	def changecategory(self,db,email,url,newcat):
		self.log.info("Change category %s,%s,%s", email, newcat)

		res = Notification()
		# mandatory: email,oldcat,newcat
		Validators.check_required(email,"E-mail",res)
		# check if category exists, if not add it 
		# update category for feed 
			
		if not res.haserrors:
			try:
				ret = db.users.update({'_id':email,'subs._id':url},
				{'$set':{'subs.$.category':newcat}})
				retval,err = Helper.checkValid(ret)

				if not retval:
					res.adderror(err)
				else:
					ret = db.users.update({'_id':email},{'$addToSet':{'categories':newcat}})
					retval,err = Helper.checkValid(ret)
					if not retval:
						res.adderror(ret)
						
			except Exception,err:
				self.log.error("Change Category failed %s", str(err))
				raise
				
		return res

	
	def renamecategory(self,db,email,oldcat,newcat):
		self.log.info("Rename category %s,%s,%s", email, oldcat,newcat)

		res = Notification()
		# mandatory: email,oldcat,newcat
		Validators.check_required(email,"E-mail",res)
		Validators.check_required(oldcat,"Existing Category",res)
		Validators.check_required(newcat,"Category",res)
		# check if email exists
		# catch any error during update
		if not res.haserrors:
			try:
				if db.users.find_one({'_id':email,'categories':oldcat,'subs.category':oldcat},{'subs':0,'categories':0}) is not None:
							ret = db.users.update({'_id':email,'categories':oldcat,'subs.category':oldcat},{'$set':{'categories.$':newcat},'$set':{'subs.$.category':newcat}})
							retval,err = Helper.checkValid(ret)
							if not retval:
								res.adderror(err)					
				elif db.users.find_one({'_id':email,'categories':oldcat},{'subs':0,'categories':0}) is not None:
							ret = db.users.update({'_id':email,'categories':oldcat},{'$set':{'categories.$':newcat}})
							retval,err = Helper.checkValid(ret)
							if not retval:
								res.adderror(err)					
				
			except Exception,err:
				self.log.error("Change Category failed %s", str(err))
				raise
				
		return res

	def refreshfeed(self,db,email,feedurl,settings):
		# function to refresh existing feed
		feed = Feed()
		nobj = feed.updatefeed(db.connection,feedurl,settings)

		if not nobj.haserrors:
			nobj = getfeeddata(db.connection,email,feedurl)
			# app.logger.info(nobj)	
	
		return nobj
		
		
	# a feed can be part of one or no category  at a time
	def addfeed(self,db,email,feedurl,category,settings):
		self.log.info("Adding %s feed for %s", feedurl,email)
		res = Notification()
		try:
			if db.users.find_one({'_id':email,'subs._id':feedurl}):
				res.setdata(True,"User has already subscribed to feed!",None)
				return res
			elif not db.users.find_one({'_id':email}):
				res.setdata(True,"Unregistered User!",None)
				return res
			
			feed_data = Feed().updatefeed(db,feedurl,settings)
			if not feed_data.haserrors:
				itemlist = {}
				for feeditem in feed_data.result['items']:
					itemlist[feeditem['_id']]={'isread':False,'isstarred':False}

				ret = db.users.update({'_id':email},{'$addToSet':{'categories':category,'subs':{'_id':feedurl,'category':category,'unreadcount':len(itemlist),'items':itemlist}}})				

				retval,err = Helper.checkValid(ret)
				if not retval:
					res.adderror(err)					
				else:
					res.result = db.users.find_one({'_id':email,'subs._id':feedurl},{'subs':1,'_id':0})
			else:
				res =  feed_data
		except Exception,err:
			self.log.error("Adding feed failed %s", str(err))
			raise
	
		#self.log.debug("returning result from addfeed")
		#self.log.debug(str(res))
		return res

			
	def removefeed(self,db,email,feedurl):
		self.log.info("Removing %s feed for %s", feedurl,email)
		res = Notification()
		try:
			feed = db.users.find_one({'_id': email,'subs._id':feedurl},{'subs':0})
			
			if not feed:
				res.setdata(True,"User hasn't subscribed to feed !!",None)
				return res
			else:
				# Ref: http://stackoverflow.com/questions/7702212/why-pull-operator-doesnt-work-on-mongodb-when-using-empty-criteria
				ret = db.users.update({'_id': email,'subs._id':feedurl},{'$pull':{'subs':{'_id':feedurl}}})

				retval,err = Helper.checkValid(ret)

				res.setdata(not retval,err,None)
		except Exception,err:
			self.log.error("Removing feed failed %s", str(err))
			raise
		return res
		
	def changefeedcategory(self,db,email,feedurl,category):
		self.log.info("Change feed category for %s [%s]", feedurl,category)
		res = Notification()
		try:
			ret = db.users.update({'_id':email,'subs._id':feedurl},{'$addToSet':{'categories':category},'$set':{'subs.$.category':category}})
		
			retval,err = Helper.checkValid(ret)
			
			if not retval:
				res.adderror(err)

			res.result = (None,db.users.find_one({'_id':email,'subs._id':feedurl},{'subs':1,'_id':0}))[retval]
				
		except Exception,err:
			self.log.error("changing feed category failed %s", str(err))
			raise
		
		return res

			
	def updatefeeditem(self,db,email,feeditemid,isread,isstarred):
		self.log.info("Update feed item for %s [%s]", email,feeditemid)
		try:
			ret = db.users.update({'_id':email,('subs.items.%s' % feeditemid):{'$exists':True}},{'$inc':{'subs.$.unreadcount': (1,-1)[isread]},'$set':{('subs.$.items.%s.isread' % feeditemid):isread, ('subs.$.items.%s.isstarred' % feeditemid):isstarred}})
				
			#self.log.debug("updatefeeditem")
			#self.log.debug(ret)
			#todo: update unread count
			
			retval,err = Helper.checkValid(ret)

			res =  Notification()
			res.setdata(not retval,err,None)
			return res

		except Exception,err:
			self.log.error("Updating feed item failed  %s", str(err))
			raise
	
	def getfeedtree(self,db,email):
		self.log.info("Get Feed Tree for %s", email)
		nobj = self.getfeedlist(db,email)
		if nobj.haserrors:
			return nobj
			
		feedtree = nobj.result

		feeddata = []
		category = ""
		curfeed = None
		
		for feed in feedtree:
			# self.log.debug("printing feed")				
			# self.log.debug(feed)
			if feed['category'] != category:
				curfeed = {'category': feed['category'],'items':[]}
				category = curfeed['category']
				feeddata.append(curfeed)						
			
			if curfeed is not None: 
				# if 'title' in feed:
					# ttl = feed['title']
				# else:
					# ttl= ""
				curfeed['items'].append({'unreadcount':feed.get('unreadcount',0),'title': feed.get('title',''),'link':feed['link']})

		nobj.result = feeddata
		
		return nobj
			
	def getfeedlist(self,db,email):
		from operator import itemgetter
		self.log.info("Get Feed list for %s", email)
		# returns hierarchical tree of categories and feeds but no feed details
		res = Notification()
		try:
			idlist=[]
			feedtree= []
			feeds = db.users.find_one({'_id':email},{'subs':1,'_id':0})
			
			if feeds is not None:
				for sub in feeds['subs']:
					if sub != {}:					
						treeobj = {'link':sub['_id'],'unreadcount': sub['unreadcount'],'category':sub['category']}
						# get feeditems and title from feed collection
						masteritems = []
						masterfeed = db.feeds.find({'_id':sub['_id']},{'title':1,'items._id':1,'_id':0})
						for r in masterfeed:
							treeobj['title'] = r['title']
							for mid in r['items']:
								masteritems.append(mid['_id'])
								
						treeobj['unreadcount'] = treeobj['unreadcount'] + len(set(masteritems) - set(sub['items']))
						# get array feed items from master
						feedtree.append(treeobj)
					
				#src: http://wiki.python.org/moin/SortingListsOfDictionaries
				# sort by category
				feedtree = sorted(feedtree,key=itemgetter('category'))
							
				res.setdata(False,None,feedtree)
			else:
				res.setdata(True,"User not found",None)				
		except Exception,err:
			self.log.error("Getting feed tree failed %s", str(err))
			raise

		return res
	
	def getfeeddata(self,db,email,feedurl):
		from operator import itemgetter
		# retrieve feed item list for user by joining results from user and feeds 
		# print("Get Feed Data for %s, %s" % (email, feedurl))
		self.log.info("Get Feed Data for %s, %s",email, feedurl)
		allfeeds = feedurl is None or feedurl==''
		try:
			if allfeeds:
				# User has opted to view "All" feeds				
				# Get all subscriptions for user
				useritems = list(db.users.find({'_id':email},{'subs':1,'_id':0}))
				urllist = []
				for u in useritems:
					for feed in u['subs']:
						urllist.append(feed['_id'])
				# get feeds for user's subscriptions
				feeditems = db.feeds.find(spec={'_id':{'$in': urllist}},fields={'_id':0,'title':1,'items':1},sort=[('published_date',2),('title',1)])
				# get 
			else:
				feeditems = db.feeds.find({'_id':feedurl},{'_id':0,'title':1,'items':1},sort=[('published_date',2),('title',1)])
				useritems = list(db.users.find({'_id':email,'subs._id':feedurl},{'subs':1,'_id':0}))						
			#self.log.debug("in data")
			#self.log.debug(feeditems)
			#self.log.debug(useritems)
			
			if not feeditems or not useritems:
				res =  Notification()
				res.setdata(True,"Incorrect feed url or mail id",None)
				return res

			feedlist=[]
			for feed in feeditems:
				# print(feed)
				# print("****")
				for fitem in feed['items']:
					useritem = None
					fitem['published_date']=str(Helper.datefromtimestamp(fitem['published_date']))					
					for usersub in useritems:
						for usub in usersub['subs']:
							for uitem in usub['items']:
								if uitem == fitem['_id']:
									fitem['isread'] = usub['items'][uitem]['isread']
									fitem['isstarred'] = usub['items'][uitem]['isstarred']
					if allfeeds:
						fitem["feedtitle"] = feed['title'] 
						
					feedlist.append(fitem)
					# print("***** done ******")

			res =  Notification()
			# print("length of array")
			# print(len(feedlist))
			feedlist = sorted(feedlist,key=itemgetter('published_date'),reverse=True)			
			res.setdata(False,None,feedlist)
			return res
		except Exception,err:
			self.log.error("Getting feed data failed %s", str(err))
			raise
			
		
class Feed(object):

	def __init__(self):
		self.log = logging.getLogger(__name__)
		
	def removefeed(self,db,feedurl):
		db.feeds.remove({'_id':feedurl})

	def updateall(self,db,settings):
		#ref: http://pythonhosted.org/futures/
		from concurrent import futures
		from datetime import datetime,timedelta
		print("invoked")
		self.log.info("Update all method invoked")
		nobj= Notification()
		# loop through feeds that are not updated in last 30 mins
		#http://stackoverflow.com/questions/4541629/how-to-create-a-datetime-equal-to-15-minutes-ago
		try:
			tilltime = Helper.datetotimestamp(datetime.now()-timedelta(minutes=15))
			feedlist = []
			for feed in db.feeds.find({'lastupdated':{'$lt':tilltime}},{'items':0}):
				# and call updatefeed for each feedurl
				feedlist.append(feed['_id'])
			
			if len(feedlist) > 0:
				with futures.ThreadPoolExecutor(max_workers=5) as executor:
					future_to_url = dict((executor.submit(self.updatefeed,db, feed, settings), feed) for feed in feedlist)

				for future in futures.as_completed(future_to_url):
					feed = future_to_url[future]
					if future.exception() is not None:
						err = '%r generated an exception: %s' % (feed,future.exception())
						nobj.adderror(err)
						print(err)
					else:
						print('%r page is done' % (feed))
		except Exception,err:
			nobj.adderror(str(err))
			self.log.error("Update all feeds failed with error %s",str(err))
			
		return nobj
		
	def updatefeed(self,db,feedurl,settings):
		from bson.objectid import ObjectId
		from time import mktime
		from datetime import datetime

		self.log.info("Updating feed for %s" , feedurl)
		# Use feedparser to get updates 
		feedObj = FeedGateway.getfeed(feedurl,settings)
		fitemdb = None

		if feedObj.haserrors:
			return feedObj
		else:
			try:
				feed_data = feedObj.result
				feedindb = db.feeds.find_one({'_id':feedurl})
				if feedindb is None:
					feedindb = {'_id':feedurl,'title':"",'items':[]}

				feedindb["title"] = feed_data["feed"]["title"]
				
				if 'items' not in feedindb:
					feedindb["items"] = []


				for fitem in feed_data["entries"]:
					fitemdb=None
					# search if item is already available in DB
					for fi in feedindb["items"]:	
						if fi["link"] == fitem["link"]:
							fitemdb = fi
							break
					"""
					src:-> http://www.seehuhn.de/pages/pdate#struct							
					"""
					# if not found then add it else do nothing
					if fitemdb is None:			
						if fitem.has_key('published_parsed'):
							pdate = mktime(fitem['published_parsed'])
						else:
							pdate = Helper.datetotimestamp(datetime.today())

						feedindb["items"].append({
							'_id': str(ObjectId()),	
							'link':fitem["link"],
							'title':fitem["title"],
							'author': fitem.get("author",""),
							'summary':fitem["summary"],
							"published_date":pdate
						})							
						
#				db.feeds.remove({'_id':feedurl})
				#self.log.debug(feedindb)
				feedindb["lastupdated"] = Helper.datetotimestamp(datetime.now())
				db.feeds.save(feedindb)							
			except Exception,err:
				self.log.error("Feed updation failed with error: %s", str(err))
		
			ret = Notification()
			#self.log.info(feedindb)
			ret.setdata(False,None, feedindb)
			
			return ret
			
class FeedGateway(object):
        @classmethod
        def getfeed(cls,feedurl,settings):
                feeddata = None
                retval = Notification()
                log = logging.getLogger('FeedGateway')
                log.info("Getting feed for %s", feedurl)
                try:
			if settings and settings["http_proxy"] and settings["http_proxy"]<>"":
				prxy = urllib2.ProxyHandler({"http": settings["http_proxy"]})
                                log.debug("Proxy being used is : %s",prxy)
			else:
                                log.debug("No Proxy in use")
	                        prxy = None
			

                        #print "before calling parse"
			if prxy:			
	                        feeddata = feedparser.parse(feedurl, handlers = [prxy])	
			else:
				feeddata = feedparser.parse(feedurl)

			#log.debug(feeddata)
                        #print "after calling parse"
                except Exception,err:
                        log.error("Getfeed failed for %s with error: %s",feedurl,str(err))
                        raise

                #print "feeddata"
                #print feeddata
		if feeddata.has_key('bozo_exception'):
			err = str(feeddata['bozo_exception'])
		else:
			err = ""

                retval.setdata(
                        not (feeddata and feeddata['bozo'] == 0),
                        err,feeddata)
                #print retval
                return retval
	
#http://martinfowler.com/eaaDev/Notification.html
class Notification(object):
	haserrors = False
	errors = []
	result = None

	def setdata(self,haserror,error,result):
		self.haserrors = haserror
		self.errors.append(error)
		self.result= result
	
	def adderror(self,error):
		self.haserrors = True
		self.errors.append(error)
			
	def adderrors(self,errlist):
		self.haserrors = True
		self.errors.extend(errlist)

	def clear(self):
		self.errors = []
		self.result = None
		
		
class Helper(object):
	@classmethod
	def checkValid(cls,ret):
		if ret:
			if ret['ok'] and ret['ok']== 1:
				return True,""
			elif ret['err']:
				return False,ret['err']
		else:
			return True,""

	#http://www.seehuhn.de/pages/pdate
	@classmethod
	def datetotimestamp(cls,dt):
		from datetime import datetime
		from time import mktime
		return mktime(dt.timetuple())+1e-6*dt.microsecond

	@classmethod
	def datefromtimestamp(cls,ts):
		from datetime import datetime
		return datetime.fromtimestamp(ts) if ts else ""
	
import re
class Validators(object):
	@classmethod
	def validate_email(cls,field,fieldname,notobj):
			if notobj.haserrors:
				return
			pt = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)\b")
			if not pt.match(field):
				notobj.adderror("%s is not valid" % (fieldname))

	@classmethod	
	def check_required(cls,field,fieldname,notobj):
			if notobj.haserrors:
				return
			if not field:
				notobj.adderror("%s should not be empty" % (fieldname))
		

if __name__ == '__main__':
    app.run(debug=True)


#http://flask.pocoo.org/docs/config/

"""
app = Flask(__name__,instance_relative_config=True)
app.config.from_pyfile('default.cfg',silent=True)

api = restful.Api(app)
db = dbcon(app)

parser = reqparse.RequestParser()

class Auth(Resource):
	def post(self)
        args = parser.parse_args()
		user = db.users.find_one({"_id": args['email']})
		if user is None:
			db.users.insert({"_id":args['email'],"name":args['name'],"pwd":args['pwd'],
				categories: []	})

			return args['email'], 201	
		else:
			return "{} Already registered !!".format(args['email']), 400
		

api.add_resource(auth, '/signup')		

class Category(Resource):
	def post(self):
	    args = parser.parse_args()
		if args['email'] is None:
			abort(404, message="email isn't available")			
		elif args['category'] is None or len(args['category'])) == 0:
			abort(404, message="category name cannot be empty")

			
		qry = json.loads('{"_id":"%s","categories.%s":{"$exists":true}' % (args['email'],args['category']))

		cat = db.users.find_one(qry)

		if cat is not None:
			abort(404,message="Category already exists")
		else:
			cat = db.users.update(qry,json.loads('{"$set":{"categories.%s":{}}}' % args['category'])

		if cat["ok"]==1:
		        return cat["value"],201
		else:
			return cat["lastErrorObject"], 400

api.add_resource(Category,'/category')
			
class CategoryUpdate(Resource):
	def delete(self, category):
		args = parser.parse_args()
		if category is None:
			abort(404, message="Category doesn't exist")			

		qry = json.loads('{"_id":"%s","categories.%s":{'$exists':true}' % (args['email'],category))
	
		for item in list(db.users.find(qry)):
			db.users.remove(item["_id"])
		
		return category, 204

		
	def put(self,category):
		args = parser.parse_args()
		newname = args["newname"]
		if category is None or newname is None:
			abort(404, message="Category and/or new category name doesn't exist")			

		qry = json.loads('{"_id":"%s","categories.%s":{'$exists':true}' % (args['email'],category))

		obj = db.users.find_one(qry)
		
		if obj is Not None:
			db.users.update(qry,json.loads('{"$rename": {"categories.%s":"categories.%s"}}' % (category,newname))
		else
			abort(404,message="Category does not exists")
		
		return newname, 204

api.add_resource(CategoryUpdate,'/category/<string:category>')	
		
class Feeds(Resource):
	def get(self):
		# get the feeds for logged-in user 
		# it should be union of users and feeds collections
		args = parser.parse_args()
		if args['email'] is None:
			abort(404,message="Email is not available")
		# build the hierarchical feed structure, 
		# it is assumed that batch job would populate user collection with new feeds 
		feeds = db.users.find_one({"_id":args['email']},{'categories':1,'_id':0})
			
		return feeds

	def delete(self):
	# remove subscription 
		args = parser.parse_args()
		if args['email'] is None:
			abort(404,message="Email is not available")
		if args['email'] is None:
			abort(404,message="Email is not available")
		# build the hierarchical feed structure, 
		# it is assumed that batch job would populate user collection with new feeds 
		feeds = db.users.find_one({"_id":args['email']},{'categories':1,'_id':0})
		return feeds

		
	def put(self):
	# modify feed item like mark as read or star it or change category !!



class Feed_subscription(Resource):
	def post(self):
		import urllib2
		# subscribe to a new post 
		args = parser.parse_args()  
		if args['email'] is None:
			abort(404,message="Email is not available")
		# check if url is already subscribed to 
		if args['feedurl'] is None:
			abort(404,message="Url for subscription can not be empty")

		# check if feed is already subscribed to by user
		feed_data = db.users.find_one({"_id":args['email']},{'categories':1,'_id':0})
		
		# check if feed is already available in collection
		feed_data = db.feeds.find_one({"url": args["feedurl"]})
		if feed_data is None:
		else:
			#t = datetime.now()
			#t1 = t.timetuple()
			#time.mktime(t1)
"""
