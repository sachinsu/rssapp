import unittest, pymongo, random, api , logging, sys

class UserTest(unittest.TestCase):

	def setUp(self):
		self.db = pymongo.MongoClient("localhost",27017,safe=True).feedtester
		self.user = api.User()
		self.feed = api.Feed()
		self.log = logging.getLogger('apitest')
		self.testfeedurl = 'http://feeds.harvardbusiness.org/harvardbusiness/bregman/'
		self.prxydict = {'http_proxy':'http://www-proxy.au.oracle.com:80'}

	def tearDown(self):
		self.db.users.remove()
		self.db.feeds.remove()

	# def test_user_wronglogin(self):
			# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
			# self.assertFalse(notobj.haserrors)
			# self.assertIsNone(self.user.login(self.db,'gg@try.com','bb').result)
			
	# def test_user_login(self):
			# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
			# self.assertFalse(notobj.haserrors)
			# self.assertIsNotNone(self.user.login(self.db,'a@b.com','xyz').result)
				
	# def test_save_user_wrongemail(self):
		# notobj = self.user.save(self.db,'wrongmail','abc','xyz')
		# self.assertTrue(notobj.haserrors)
	# def test_save__user_wrongname(self):
		# notobj = self.user.save(self.db,'a@b.com','','xyz')
		# self.assertTrue(notobj.haserrors)
	# def test_save_user_samenamepwd(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','abc')
		# self.assertTrue(notobj.haserrors)
	# def test_save_user(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# self.assertFalse(self.db.users.find_one({'_id':'a@b.com','name':'abc','pwd':'xyz'})  is None)
	# def test_addcategory_wrongemail(self):
		# notobj = self.user.addcategory(self.db,'','abc')
		# self.assertTrue(notobj.haserrors)
	# def test_addcategory_wrongemail_emptycat(self):
		# notobj = self.user.addcategory(self.db,'','')
		# self.assertTrue(notobj.haserrors)
	# def test_removecategory_blankcategory(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.removecategory(self.db,'a@b.com','')
		# self.assertTrue(notobj.haserrors)
		
	# def test_removecategory_removal(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.removecategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# self.assertTrue(self.db.users.find_one({'_id':'a@b.com','categories':'fun','subs.category':'fun'}) is None)
	# def test_changecategory_wrongnewcat(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.changecategory(self.db,'a@b.com','fun','')
		# self.assertTrue(notobj.haserrors)
		
	# def test_changecategory_wrongoldcat(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.changecategory(self.db,'a@b.com','','money')
		# self.assertTrue(notobj.haserrors)
		
	# def test_changecategory_wrongemail(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.changecategory(self.db,'','fun','money')
		# self.assertTrue(notobj.haserrors)
		
	# def test_changecategory_save(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.changecategory(self.db,'a@b.com','fun','money')
		# self.assertFalse(notobj.haserrors)
		# self.assertIsNone(self.db.users.find_one({'_id':'a@b.com','categories':'fun'}))
		# self.assertIsNotNone(self.db.users.find_one({'_id':'a@b.com','categories':'money'}))

	# def test_addfeed_wrongurl(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com','y.com','fun',self.prxydict)
		# self.assertTrue(notobj.haserrors)

		
	# def test_addfeed_save(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com','http://devinder-sharma.blogspot.com/feeds/posts/default','fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)

	# def test_getfeeddata_wrongemail(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com',self.testfeedurl,'fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.getfeeddata(self.db,'t@e.com',self.testfeedurl)
		# self.assertTrue(notobj.haserrors)

	# def test_getfeeddata_allfeeds(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com','http://devinder-sharma.blogspot.com/feeds/posts/default','money',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com','http://www.readwriteweb.com/hack/rss.xml','fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com','http://feeds.feedburner.com/typepad/sethsmainblog','fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.getfeeddata(self.db,'a@b.com',None)
		# self.assertFalse(notobj.haserrors)

		
	# def test_getfeeddata_wrongfeedurl(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com',self.testfeedurl,'fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.getfeeddata(self.db,'a@b.com','www.self.com')
		# self.assertTrue(notobj.haserrors)
	
	# def test_getfeeddata_success(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com',self.testfeedurl,'fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.getfeeddata(self.db,'a@b.com',self.testfeedurl)
		# self.assertFalse(notobj.haserrors)
		
	# def test_removefeed_wrongfeed(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com',self.testfeedurl,'fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.removefeed(self.db,'a@b.com','www.google.com')
		# self.assertTrue(notobj.haserrors)
		
	# def test_removefeed_remove(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com',self.testfeedurl,'fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.removefeed(self.db,'a@b.com',self.testfeedurl)
		# self.assertFalse(notobj.haserrors)
	# def test_changefeedcategory_change(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com',self.testfeedurl,'fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.changefeedcategory(self.db,'a@b.com',self.testfeedurl,'tech')
		# self.assertFalse(notobj.haserrors)
		# self.assertFalse(self.db.users.find_one({'_id':'a@b.com','subs._id':self.testfeedurl,'subs.category':'tech'}) 
# is None)
		
	# def test_updatefeeditem_update(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com',self.testfeedurl,'fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# feeditem = self.db.users.find_one({'_id':'a@b.com','subs._id':self.testfeedurl})
		# self.assertFalse(feeditem is None)
		# flist = feeditem['subs'][0]['items'].items()
		# fitem = None
		# for i in flist:
			# fitem = i
		
		# self.assertFalse(self.user.updatefeeditem(self.db,'a@b.com',fitem[0],True,False).haserrors)
		# self.assertIsNotNone(self.db.users.find_one({'_id':'a@b.com',('subs.items.%s.isread' % fitem[0]) :True,
						# ('subs.items.%s.isstarred' % fitem[0]): False}))

	# def test_getfeedtree_checkmail(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com','http://devinder-sharma.blogspot.com/feeds/posts/default','money',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com','http://www.readwriteweb.com/hack/rss.xml','fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com','http://feeds.feedburner.com/typepad/sethsmainblog','fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.getfeedlist(self.db,'a@f.com')
		# self.assertTrue(notobj.haserrors)
		
	
	# def test_getfeedtree_checkorder(self):
		# notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addcategory(self.db,'a@b.com','fun')
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com','http://devinder-sharma.blogspot.com/feeds/posts/default','money',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com','http://www.readwriteweb.com/hack/rss.xml','fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.addfeed(self.db,'a@b.com','http://feeds.feedburner.com/typepad/sethsmainblog','fun',self.prxydict)
		# self.assertFalse(notobj.haserrors)
		# notobj = self.user.getfeedlist(self.db,'a@b.com')
		# self.assertFalse(notobj.haserrors)
		# self.assertTrue(notobj.result[0]['category']=='fun')
	
	def test_getfeeddata_checkindb(self):
		notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		self.assertFalse(notobj.haserrors)
		notobj = self.user.addcategory(self.db,'a@b.com','fun')
		self.assertFalse(notobj.haserrors)
		notobj = self.user.addfeed(self.db,'a@b.com','http://devinder-sharma.blogspot.com/feeds/posts/default','money',self.prxydict)
		self.assertFalse(notobj.haserrors)
		notobj = self.user.getfeeddata(self.db,'a@b.com','http://devinder-sharma.blogspot.com/feeds/posts/default')
		self.assertFalse(notobj.haserrors)
		feedinfo = self.db.feeds.find_one({'_id':'http://devinder-sharma.blogspot.com/feeds/posts/default', 'items._id':notobj.result[0]['_id']})
		self.assertIsNotNone(feedinfo)
		self.assertTrue(len(feedinfo['items']) == len(notobj.result))

	def test_updateall(self):
		notobj = self.user.save(self.db,'a@b.com','abc','xyz')
		self.assertFalse(notobj.haserrors)
		notobj = self.user.addcategory(self.db,'a@b.com','fun')
		self.assertFalse(notobj.haserrors)
		notobj = self.user.addfeed(self.db,'a@b.com','http://devinder-sharma.blogspot.com/feeds/posts/default','money',self.prxydict)
		self.assertFalse(notobj.haserrors)
		notobj = self.user.addfeed(self.db,'a@b.com','http://www.readwriteweb.com/hack/rss.xml','fun',self.prxydict)
		self.assertFalse(notobj.haserrors)
		notobj = self.user.addfeed(self.db,'a@b.com','http://feeds.feedburner.com/typepad/sethsmainblog','fun',self.prxydict)
		self.assertFalse(notobj.haserrors)
		notobj = self.user.addfeed(self.db,'a@b.com','http://zeenut.blogspot.com/feeds/posts/default?alt=rss','fun',self.prxydict)
		self.assertFalse(notobj.haserrors)
		notobj = self.user.addfeed(self.db,'a@b.com','http://www.spiegel.de/international/index.rss ','fun',self.prxydict)
		self.assertFalse(notobj.haserrors)
		notobj = self.feed.updateall(self.db,self.prxydict)
		self.assertFalse(notobj.haserrors)		

		
		
if __name__ == '__main__':
	logging.basicConfig(stream=sys.stderr)
	# logging.getLogger('jsonapi').setLevel(logging.DEBUG)
	# logging.getLogger('api').setLevel(logging.DEBUG)
	# logging.getLogger('apitest').setLevel(logging.DEBUG)
	unittest.main()
