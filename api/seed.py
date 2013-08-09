from api import User,Feed,Notification,Helper
import pymongo

def seed_data():
	prxyval = Helper.getconfigvalue('dev.cfg','http_proxy',None)
	
	if prxyval is not None:
		prxydict = {'http_proxy':prxyval}
	else:
		prxydict = None
		
	dburl = Helper.getconfigvalue('dev.cfg','DATABASE_URI',None)
	dbname = Helper.getconfigvalue('dev.cfg','DBNAME',None)		

	db = pymongo.MongoClient(dburl)[dbname]

	emailid = "mo@green.com"
	user  = User()
	notobj = user.save(db,emailid,emailid,'pwd')
	notobj = user.addcategory(db,emailid,'fun')
	notobj = user.addcategory(db,emailid,'money')	
	notobj = user.addfeed(db,emailid,'http://raptitude.com/rss','fun',prxydict)
	notobj = user.addfeed(db,emailid,'http://feeds.feedburner.com/typepad/sethsmainblog','fun',prxydict)
	notobj = user.addfeed(db,emailid,'http://feeds.feedburner.com/TheInvestorBlog','money',prxydict)
	
	 

	
if __name__ == '__main__':
	seed_data()	
	