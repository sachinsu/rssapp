'use strict';
var base64 = function(){
	var obj = {};
	
    obj.alphabet= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
    obj.lookup= null;
    obj.ie= /MSIE /.test(navigator.userAgent);
    obj.ieo= /MSIE [67]/.test(navigator.userAgent);
	
    obj.encode= function (s) {
        var buffer = obj.toUtf8(s),
            position = -1,
            len = buffer.length,
            nan1, nan2, enc = [, , , ];
        if (obj.ie) {
            var result = [];
            while (++position < len) {
                nan1 = buffer[position + 1], nan2 = buffer[position + 2];
                enc[0] = buffer[position] >> 2;
                enc[1] = ((buffer[position] & 3) << 4) | (buffer[++position] >> 4);
                if (isNaN(nan1)) enc[2] = enc[3] = 64;
                else {
                    enc[2] = ((buffer[position] & 15) << 2) | (buffer[++position] >> 6);
                    enc[3] = (isNaN(nan2)) ? 64 : buffer[position] & 63;
                }
                result.push(obj.alphabet[enc[0]], obj.alphabet[enc[1]], obj.alphabet[enc[2]], obj.alphabet[enc[3]]);
            }
            return result.join('');
        } else {
            result = '';
            while (++position < len) {
                nan1 = buffer[position + 1], nan2 = buffer[position + 2];
                enc[0] = buffer[position] >> 2;
                enc[1] = ((buffer[position] & 3) << 4) | (buffer[++position] >> 4);
                if (isNaN(nan1)) enc[2] = enc[3] = 64;
                else {
                    enc[2] = ((buffer[position] & 15) << 2) | (buffer[++position] >> 6);
                    enc[3] = (isNaN(nan2)) ? 64 : buffer[position] & 63;
                }
                result += obj.alphabet[enc[0]] + obj.alphabet[enc[1]] + obj.alphabet[enc[2]] + obj.alphabet[enc[3]];
            }
            return result;
        }
    };
    obj.decode= function (s) {
        var buffer = obj.fromUtf8(s),
            position = 0,
            len = buffer.length;
        if (obj.ieo) {
            result = [];
            while (position < len) {
                if (buffer[position] < 128) result.push(String.fromCharCode(buffer[position++]));
                else if (buffer[position] > 191 && buffer[position] < 224) result.push(String.fromCharCode(((buffer[position++] & 31) << 6) | (buffer[position++] & 63)));
                else result.push(String.fromCharCode(((buffer[position++] & 15) << 12) | ((buffer[position++] & 63) << 6) | (buffer[position++] & 63)));
            }
            return result.join('');
        } else {
            result = '';
            while (position < len) {
                if (buffer[position] < 128) result += String.fromCharCode(buffer[position++]);
                else if (buffer[position] > 191 && buffer[position] < 224) result += String.fromCharCode(((buffer[position++] & 31) << 6) | (buffer[position++] & 63));
                else result += String.fromCharCode(((buffer[position++] & 15) << 12) | ((buffer[position++] & 63) << 6) | (buffer[position++] & 63));
            }
            return result;
        }
    };
    obj.toUtf8= function (s) {
        var position = -1,
            len = s.length,
            chr, buffer = [];
        if (/^[\x00-\x7f]*$/.test(s)) while (++position < len)
        buffer.push(s.charCodeAt(position));
        else while (++position < len) {
            chr = s.charCodeAt(position);
            if (chr < 128) buffer.push(chr);
            else if (chr < 2048) buffer.push((chr >> 6) | 192, (chr & 63) | 128);
            else buffer.push((chr >> 12) | 224, ((chr >> 6) & 63) | 128, (chr & 63) | 128);
        }
        return buffer;
    };
    obj.fromUtf8= function (s) {
        var position = -1,
            len, buffer = [],
            enc = [, , , ];
        if (!obj.lookup) {
            len = obj.alphabet.length;
            obj.lookup = {};
            while (++position < len)
            obj.lookup[obj.alphabet[position]] = position;
            position = -1;
        }
        len = s.length;
        while (position < len) {
            enc[0] = obj.lookup[s.charAt(++position)];
            enc[1] = obj.lookup[s.charAt(++position)];
            buffer.push((enc[0] << 2) | (enc[1] >> 4));
            enc[2] = obj.lookup[s.charAt(++position)];
            if (enc[2] == 64) break;
            buffer.push(((enc[1] & 15) << 4) | (enc[2] >> 2));
            enc[3] = obj.lookup[s.charAt(++position)];
            if (enc[3] == 64) break;
            buffer.push(((enc[2] & 3) << 6) | enc[3]);
        }
        return buffer;
    }
	
	return obj;
};

var rssfactory = function($rootScope,$http,base64){
	var baseurl = "/api/";

	var factory={emailid:"",pwd:"",feedlist:null,feed:null,categories:null};

	factory.isLoggedin = function() {
	//http://stackoverflow.com/questions/154059/how-do-you-check-for-an-empty-string-in-javascript
		// console.log("in isloggedin");
		// console.log(this.emailid);
		return (!this.emailid || 0 === this.emailid.length);
	};
	
	factory.logout = function() { 
		factory.emailid="";
		factory.pwd="";
		factory.feedlist=null;
		factory.feed=null;
		factory.categories=null;
	};
	
	//src: http://cvmlrobotics.blogspot.com/2013/04/angularjs-safe-scopeapply.html
	factory.safeApply = function(scope,fn) {
		var phase = scope.$root.$$phase;
		  if(phase == '$apply' || phase == '$digest')
		    scope.$eval(fn);
		  else
		    scope.$apply(fn);
	};

	factory.register = function(email,name,pwd,callback,errcallback){
			console.log("posting request");

			$http({method:'POST',
				url: baseurl + 'register',
				data:{'email':email,'name':name,'pwd':pwd}
				,headers: factory.buildheaders(false)
			}).success(function(d,s,h,c){
					//sample: ({errors:[], result:null, success:true})			
					if (d.success)
						factory.safeApply($rootScope,function() { callback(d.result);});
					else
						factory.safeApply($rootScope,function(){ errcallback(d.errors,null,null,null); });	
			}).error(function(d,s,h,c){
					//todo: show error 
					factory.safeApply($rootScope,function(){ errcallback(d,s,h,c); });
			});
			};

	factory.getsublist = function(callback,errcallback){
			console.log("get feeds");

			$http({method:'GET',
					url: baseurl + 'feedlist'
					,headers: factory.buildheaders(true)
					,withCredentials: true
			}).success(function(d,s,h,c){
					//sample: ({errors:[], result:null, success:true})			
					console.log("in success");
					if (d.success)
						factory.safeApply($rootScope,function() { callback(d.result);});
					else
						factory.safeApply($rootScope,function(){ errcallback(d.errors,null,null,null); });	
			}).error(function(d,s,h,c){
					//todo: show error 
					console.log("in error");
					// console.log(d);
					// console.log(s);
					// console.log(h);
					// console.log(c);
					factory.safeApply($rootScope,function(){ errcallback(d,s,h,c); });
			});
			};			


	factory.getfeeds = function(url,callback,errcallback){
			console.log("get feeds");

			$http({method:'GET',
					url: baseurl + 'feed'
					,params: {feedurl: url}
					,headers: factory.buildheaders(true)
					,withCredentials: true
			}).success(function(d,s,h,c){
					//sample: ({errors:[], result:null, success:true})			
					console.log("in success");
					if (d.success)
						factory.safeApply($rootScope,function() { callback(d.result);});
					else
						factory.safeApply($rootScope,function(){ errcallback(d.errors,null,null,null); });	
			}).error(function(d,s,h,c){
					//todo: show error 
					console.log("in error");
					 console.log(d);
					 console.log(s);
					 console.log(h);
					 console.log(c);
					factory.safeApply($rootScope,function(){ errcallback(d,s,h,c); });
			});
			};			

	factory.getallfeeds = function(url,callback,errcallback){

			$http({method:'GET',
					url: baseurl + 'feeds'
					,headers: factory.buildheaders(true)
					,withCredentials: true
			}).success(function(d,s,h,c){
					//sample: ({errors:[], result:null, success:true})			
					if (d.success)
						factory.safeApply($rootScope,function() { callback(d.result);});
					else
						factory.safeApply($rootScope,function(){ errcallback(d.errors,null,null,null); });	
			}).error(function(d,s,h,c){
					//todo: show error 
					console.log("in error");
					// console.log(d);
					// console.log(s);
					// console.log(h);
					// console.log(c);
					factory.safeApply($rootScope,function(){ errcallback(d,s,h,c); });
			});
			};			
			
	factory.updateitem = function(id,isread,isstarred,callback,errcallback){
			console.log("update item");

			$http({method:'PUT',
					url: baseurl + 'feeditem'
					,data: {'feedurl': factory.feed.url,'id': id,'isread':isread,'isstarred':isstarred}
					,headers: factory.buildheaders(true)
					,withCredentials: true
			}).success(function(d,s,h,c){
					//sample: ({errors:[], result:null, success:true})			
					console.log("in updateitem success");
					if (d.success)
						factory.safeApply($rootScope,function() { callback(d.result);});
					else
						factory.safeApply($rootScope,function(){ errcallback(d.errors,null,null,null); });	
			}).error(function(d,s,h,c){
					//todo: show error 
					console.log("in error");
					// console.log(d);
					// console.log(s);
					// console.log(h);
					// console.log(c);
					factory.safeApply($rootScope,function(){ errcallback(d,s,h,c); });
			});
			};			

	factory.getcategorylist = function(callback,errcallback){
			$http({method:'GET',
					url: baseurl + 'category'
					,headers: factory.buildheaders(true)
					,withCredentials: true
			}).success(function(d,s,h,c){
					//sample: ({errors:[], result:null, success:true})			
					console.log("in success");
					if (d.success)
						factory.safeApply($rootScope,function() { callback(d.result);});
					else
						factory.safeApply($rootScope,function(){ errcallback(d.errors,null,null,null); });	
			}).error(function(d,s,h,c){
					//todo: show error 
					console.log("in error");
					// console.log(d);
					// console.log(s);
					// console.log(h);
					// console.log(c);
					factory.safeApply($rootScope,function(){ errcallback(d,s,h,c); });
			});
			};			

	factory.addcategory = function(catname,callback,errcallback){
			$http({method:'POST',
					url: baseurl + 'category'
					,data: {'category': catname}
					,headers: factory.buildheaders(true)
					,withCredentials: true
			}).success(function(d,s,h,c){
					//sample: ({errors:[], result:null, success:true})			
					if (d.success)
						factory.safeApply($rootScope,function() { callback(d.result);});
					else
						factory.safeApply($rootScope,function(){ errcallback(d.errors,null,null,null); });	
			}).error(function(d,s,h,c){
					//todo: show error 
					console.log("in error");
					// console.log(d);
					// console.log(s);
					// console.log(h);
					// console.log(c);
					factory.safeApply($rootScope,function(){ errcallback(d,s,h,c); });
			});
			};			

	factory.addfeed = function(furl,category,callback,errcallback){

			$http({method:'POST',
					url: baseurl + 'feed'
					,data: {'feedurl': furl,'category':category}
					,headers: factory.buildheaders(true)
					,withCredentials: true
			}).success(function(d,s,h,c){
					//sample: ({errors:[], result:null, success:true})						
					if (d.success)
						factory.safeApply($rootScope,function() { callback(d.result);});
					else
						factory.safeApply($rootScope,function(){ errcallback(d.errors,null,null,null); });	
			}).error(function(d,s,h,c){
					//todo: show error 
					factory.safeApply($rootScope,function(){ errcallback(d,s,h,c); });
			});
			};						
			
	factory.removefeed = function(furl,callback,errcallback){

			$http({method:'DELETE',
					url: baseurl + 'feed'
					,params: {feedurl: furl}
					,headers: factory.buildheaders(true)
					,withCredentials: true
			}).success(function(d,s,h,c){
					//sample: ({errors:[], result:null, success:true})						
					if (s==204)
						factory.safeApply($rootScope,function() { callback(d.result);});
					else
						factory.safeApply($rootScope,function(){ errcallback(d.errors,null,null,null); });	
			}).error(function(d,s,h,c){
					//todo: show error 
					console.log("app.js in error");
					factory.safeApply($rootScope,function(){ errcallback(d,s,h,c); });
			});
			};			
			
	factory.refreshfeed = function(furl,callback,errcallback){
			$http({method:'GET',
					url: baseurl + 'feed/refresh'
					,params: {feedurl: furl}
					,headers: factory.buildheaders(true)
					,withCredentials: true
			}).success(function(d,s,h,c){
					//sample: ({errors:[], result:null, success:true})			
					if (d.success)
						factory.safeApply($rootScope,function() { callback(d.result);});
					else
						factory.safeApply($rootScope,function(){ errcallback(d.errors,null,null,null); });	
			}).error(function(d,s,h,c){
					//todo: show error 
					console.log("in error");
					// console.log(d);
					// console.log(s);
					// console.log(h);
					// console.log(c);
					factory.safeApply($rootScope,function(){ errcallback(d,s,h,c); });
			});
			};			
			
	factory.changecat = function(furl,oldcat,newcat,call,errcall){
			$http({method:'PUT',
					url: baseurl + 'category'
					,data: {url: furl,category:newcat}
					,headers: factory.buildheaders(true)
					,withCredentials: true
			}).success(function(d,s,h,c){
					//sample: ({errors:[], result:null, success:true})			
					if (d.success)
						factory.safeApply($rootScope,function() { call(d.result);});
					else
						factory.safeApply($rootScope,function(){ errcall(d.errors,null,null,null); });	
			}).error(function(d,s,h,c){
					//todo: show error 
					console.log("in error");
					// console.log(d);
					// console.log(s);
					// console.log(h);
					// console.log(c);
					factory.safeApply($rootScope,function(){ errcall(d,s,h,c); });
			});
		
	};

	factory.markallasread = function(furl,ts,call,errcall){
			$http({method:'PUT',
					url: baseurl + 'feeds'
					,data: {feedurl: furl,ts:ts}
					,headers: factory.buildheaders(true)
					,withCredentials: true
			}).success(function(d,s,h,c){
					//sample: ({errors:[], result:null, success:true})			
					if (d.success)
						factory.safeApply($rootScope,function() { call(d.result);});
					else
						factory.safeApply($rootScope,function(){ errcall(d.errors,null,null,null); });	
			}).error(function(d,s,h,c){
					//todo: show error 
					console.log("in error");
					// console.log(d);
					// console.log(s);
					// console.log(h);
					// console.log(c);
					factory.safeApply($rootScope,function(){ errcall(d,s,h,c); });
			});
		
	};

	
	//todo: private helper function to build headers
	factory.buildheaders = function(withauth){
			var hd =  {
				'Accept': 'application/json',
				'Content-Type':'application/json'
			};

			if (withauth){
				hd['Authorization'] = 'Basic ' + base64.encode(factory.emailid +':'+factory.pwd);
			}
			// console.log(hd);
			return hd;
	}
	
	//todo: private helper function to parse response to determine errors etc.
	//todo: provision to display error/warning messages 
	
			
	return factory;
}; 


rssfactory.inject = ["$rootScope","$http",'base64'];

//Src: http://victorblog.com/2012/12/20/make-angularjs-http-service-behave-like-jquery-ajax/
var app = angular.module('projectApp', ['ui.bootstrap'], function($httpProvider)
{
  // Use x-www-form-urlencoded Content-Type
  $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
 
 /* 
     * The workhorse; converts an object to x-www-form-urlencoded serialization.
     * @param {Object} obj
     * @return {String}
  // Override $http service's default transformRequest
  $httpProvider.defaults.transformRequest = [function(data)
  {
    var param = function(obj)
    {
      var query = '';
      var name, value, fullSubName, subName, subValue, innerObj, i;
      
      for(name in obj)
      {
        value = obj[name];
        
        if(value instanceof Array)
        {
          for(i=0; i<value.length; ++i)
          {
            subValue = value[i];
            fullSubName = name + '[' + i + ']';
            innerObj = {};
            innerObj[fullSubName] = subValue;
            query += param(innerObj) + '&';
          }
        }
        else if(value instanceof Object)
        {
          for(subName in value)
          {
            subValue = value[subName];
            fullSubName = name + '[' + subName + ']';
            innerObj = {};
            innerObj[fullSubName] = subValue;
            query += param(innerObj) + '&';
          }
        }
        else if(value !== undefined && value !== null)
        {
          query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
        }
      }
      
      return query.length ? query.substr(0, query.length - 1) : query;
    };
    
    return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
  }];
*/  
  }
).config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  }).factory('rssfactory',rssfactory)
	.factory('base64',base64);


app.config(['$httpProvider', function($httpProvider) {  
        $httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common['X-Requested-With'];
  }]);
  
/* Todo,
 - error display section, visibility:hidden check instead of display none.
 - Mark all as Read & Mark as unread
 - refresh button on sidebar and/or auto refresh mechanism
 - Provision for Scroll bar 
*/