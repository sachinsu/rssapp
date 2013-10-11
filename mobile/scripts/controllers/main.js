'use strict';
/*
-- Login controller, checks for logged in user and 
*/
angular.module('projectApp')
  .controller('MainCtrl', function ($scope,$route,rssfactory,$log,$location,$sce) {

	$scope.factory = rssfactory;
	$scope.pagesize = 5;
	// // $log.log($route);
	// $log.log("printing current");
	// $log.log($route.current);	
	// var renderPath = $route.current.action.split( "." );
	// $scope.renderPath = renderPath;

	
	$scope.go = function ( path ) {
	  $log.log("go called with " + path);
	  $location.path( path );
	};

	$scope.logout = function() { 
		rssfactory.logout();
		$scope.go("/");
	};
	
	$scope.login = function(email,pwd){
		$log.log("inside login method with " + email  + "," + pwd);
		rssfactory.register(email,"",pwd,function(result){
			rssfactory.emailid=email;
			rssfactory.pwd=pwd;	
			rssfactory.feedlist = result.feedlist
			rssfactory.categories = result.categories
			$log.info("login successful");
			$scope.go("/subs");
		},function(d,s,h,c){
			$log.error("login func. error handler" + d);
		});			
	};

	$scope.getfeeds = function(url,title,category){
		rssfactory.cururl = url;
		rssfactory.curtitle = title;
		rssfactory.curcat = category;
		rssfactory.pageno = 1;
		rssfactory.getpagefeeds(url,1,$scope.pagesize,function(result){
			rssfactory.feeddata = result;
			$scope.go('/posts');
		},function(d,s,h,c){
			$log.error("get feed items failed");
		});
	};
	
	$scope.getnextpage = function(){
		rssfactory.pageno = rssfactory.pageno + 1;
		rssfactory.getpagefeeds(rssfactory.cururl,rssfactory.pageno,$scope.pagesize,function(result){
			rssfactory.feeddata = result;
		},function(d,s,h,c){
			$log.error("get feed items failed");
		});
	};

	$scope.getprevpage = function(){
		rssfactory.pageno = rssfactory.pageno - 1;
		if (rssfactory.pageno > 0) {
			rssfactory.getpagefeeds(rssfactory.cururl,rssfactory.pageno,$scope.pagesize,function(result){
				rssfactory.feeddata = result;
			},function(d,s,h,c){
				$log.error("get feed items failed");
			});
		}
	};

	$scope.showpost = function(itm){
		$scope.factory.itm = itm;
		$scope.factory.itm.trustsummary =  $sce.trustAsHtml(itm.summary);
		$log.log(itm);
		$scope.go('/post');
	}
	
  })