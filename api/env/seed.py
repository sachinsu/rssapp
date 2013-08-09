from api import User,Feed,Notification
import pymongo

def seed_data():
	db = pymongo.MongoClient("localhost",27017,safe=True).feedtest
	emailid = "mo@green.com"
	user  = User()
	prxydict = {'http_proxy':'http://www-proxy.au.oracle.com:80'}	
	notobj = user.save(db,emailid,emailid,'pwd')
	notobj = user.addcategory(db,emailid,'fun')
	notobj = user.addcategory(db,emailid,'money')	
	notobj = user.addfeed(db,emailid,'http://raptitude.com/rss','fun',prxydict)
	notobj = user.addfeed(db,emailid,'http://feeds.feedburner.com/typepad/sethsmainblog','fun',prxydict)
	notobj = user.addfeed(db,emailid,'http://feeds.feedburner.com/TheInvestorBlog','money',prxydict)
	
	 

	
if __name__ == '__main__':
	seed_data()	
	