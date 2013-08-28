'use strict';

angular.module('projectApp')
  .controller('MainCtrl', function ($scope,rssfactory,$dialog) {
    //console.log("calling factory method");
    // rssfactory.register('bb@mail.com','bb','pwd',function(d,s){
	// console.log(d);
	// console.log(s);
	// });
	$scope.factory = rssfactory;
	
	//ref: http://stackoverflow.com/questions/14502006/scope-emit-and-on-angularjs
	$scope.$on('onerror',function(e,args) { 
		// console.log("error occured" + args);
		if (args.length == 0)
			args = ["Error while processing request !!"];
		$scope.errors = args;
	});
	
	$scope.$on('onsuccess',function(e,args) { 
		// console.log("on success" + args);
		$scope.successmsg = args;
	});

	$scope.updateitem = function(id,isread,isstarred){
		// console.log("inside updateitem" + isread);
		var f = _.first(rssfactory.feed.data,function(item){
			return item._id==id;
		});
		
		if (f && (f.isread != isread || f.isstarred != isstarred)){
			rssfactory.updateitem(id,isread,isstarred,function(result){
				f.isread = isread;
				f.isstarred = isstarred;
			},function(d,s,h,c){
				$scope.$emit('onerror',d);
			});
		}
	};
	
	$scope.keepunread = function(id,$event){
			// console.log("in keepunread");
			var chkbox = $event.target;
			$scope.updateitem(id,!chkbox.checked,false);
	};

  })
  .controller('LoginCtrl', function($scope,rssfactory,$dialog){ 
		$scope.factory = rssfactory;
		
		$scope.user = {emailid:"",pwd:"",name:""};
		
		$scope.login = function(emailid,name,pwd) { 
			 // console.log("in login method");
			 // console.log(emailid);
			rssfactory.register(emailid,name,pwd,function(result){
				// console.log("login success->")
				// console.log(result);
				rssfactory.emailid=emailid;
				rssfactory.pwd=pwd;	
				rssfactory.feedlist = result.feedlist
				rssfactory.categories = result.categories
				// $scope.$emit('onsuccess','Logged in...');
			},function(d,s,h,c){
				// error occured
				console.log("in error handler" + d);
				$scope.$emit('onerror',["Login/registration failed "]);
			});			
		};
		
		$scope.logout = function(){
			rssfactory.logout();
		};

		$scope.opts = {
			backdrop: true,
			keyboard: true,
			backdropClick: true
		  };
			//resolve: {rssfactory: function(){ return angular.copy(rssfactory); }} 					
		$scope.addcat= function(){
			$scope.opts.templateUrl=  'views/partials/category.html';
			$scope.opts.controller= 'AddCatCtrl';
			 var d = $dialog.dialog($scope.opts);
			 d.open().then(function(result){
				if(result)
				{
				//todo: update feedtree
				}
			});			
		};

	$scope.addfeed= function(){
			$scope.opts.templateUrl='views/partials/addfeed.html';
			$scope.opts.controller='AddFeedCtrl';
			 var d = $dialog.dialog($scope.opts);
			 d.open().then(function(result){
				if(result)
				{
				//todo: update feedtree
				}
			});			
		};

	$scope.refreshfeed = function(feedurl) { 
		 // console.log("in refreshfeed method" + feedurl);
		// console.log(emailid);
		rssfactory.refreshfeed(feedurl,function(d,s){
			// console.log("refreshfeed success");
			// console.log(d);
			rssfactory.feed.data = d;				
		},function(d,s,h,c){
			// error occured
			console.log("in error handler" + d);
			$scope.$emit('onerror',["Refreshing feed failed .." ]);
		});					
	};

	$scope.markallread = function(uri){
		var fdata = rssfactory.feed.data;
		var ptimestamp = 0;
		for (var i=0;i<fdata.length;i++)
		{
			if (!fdata[i].isread) {
				if (ptimestamp < fdata[i].published_date)
						ptimestamp = fdata[i].published_date;
			}
		}
		// todo: pass pid (which is latest unread item in reader) to server 
		// server is expected to mark all  items as read that have timestamp <= pid
		rssfactory.markallasread(uri,ptimestamp,function(result){
			rssfactory.feedlist = result.feedlist;
			rssfactory.feed.data = result.feeddata;
			$scope.$emit('onsuccess',["All items in feed are marked as read" ]);		
		},function(d,s,h,c){
			$scope.$emit('onerror',d);
		});
	};
	
	$scope.changecategory = function(newcategory){
		rssfactory.changecat(rssfactory.feed.url,rssfactory.feed.category,newcategory,function(result){
			rssfactory.feedlist = result;
			$scope.$emit('onsuccess',["Category of feed " + feedurl + " changed successfully" ]);		
		},function(d,s,h,c){
			$scope.$emit('onerror',d);
		});
	};
	
	$scope.removefeed = function(feedurl) { 
		var title = 'Unsubscribe feed';
		var msg = "Remove Feed '" + feedurl + "' ?";
		var btns = [{result:'no', label: 'No'}, {result:'yes', label: 'Yes', cssClass: 'btn-primary'}];

		$dialog.messageBox(title, msg, btns)
		  .open()
		  .then(function(result){
				if (result=="yes")
					{
					rssfactory.removefeed(feedurl,function(d,s){
								rssfactory.getsublist(function(result){
									rssfactory.feedlist = result;
									rssfactory.feed = null;
									$scope.$emit('onsuccess',["feed " + feedurl + " removed from your subscription list" ]);
								},function(d,s,h,c){
									$scope.$emit('onerror',d);
								});															
							},function(d,s,h,c){
								// error occured
								$scope.$emit('onerror',["Unsubscribing to feed " + feedurl + " failed .." ]);
							});		
					}
		});		
	};
	
		
  })
  .controller('AddCatCtrl',function($scope,dialog,rssfactory){
	$scope.save = function(category){
		rssfactory.addcategory(category,function(result){
					rssfactory.categories.push(category);
					dialog.close(true);
					$scope.$emit('onsuccess','Category ' + category + " added ");
				},function(d,s,h,c){
						$scope.alerts = [
							{ type: 'error', msg: 'Category addition failed' }
						  ];
				});
	}
  })
  .controller('AddFeedCtrl',function($scope,dialog,rssfactory){
	$scope.factory = rssfactory;
	$scope.save = function(furl,category){
		rssfactory.addfeed(furl,category,function(result){
					dialog.close(true);
					rssfactory.feedlist = result.feedlist
					$scope.$emit('onsuccess','feed subscription successful');
				},function(d,s,h,c){
						$scope.alerts = [
							{ type: 'error', msg: 'Feed addition failed' }
						  ];
				});
	}
  })
  .controller('SideBarCtrl', function($scope,$dialog,rssfactory){ 
		$scope.factory = rssfactory;

		$scope.getfeeds = function(furl,title,caty){
			if (furl=="")
			{
				// console.log('url ' + url);
				rssfactory.getallfeeds(function(result){
						rssfactory.feed = {url: furl, category: caty, title:title,data: result};
						// console.log("printing result from factory");
						// console.log(rssfactory.feed);
						// $scope.$emit('onsuccess','Feed data fetched');
					},function(d,s,h,c){
						$scope.$emit('onerror',d);
					});
			}
			else 
			{
			// console.log('url ' + url);
			rssfactory.getfeeds(furl,function(result){
					rssfactory.feed = {url: furl, category: caty, title:title,data: result};
					// console.log("printing result from factory");
					// console.log(rssfactory.feed);
					// $scope.$emit('onsuccess','Feed data fetched');
				},function(d,s,h,c){
					$scope.$emit('onerror',d);
				});
			}
		};
  });