'use strict';
//Src: http://victorblog.com/2012/12/20/make-angularjs-http-service-behave-like-jquery-ajax/
var app = angular.module('projectApp', ['projectApp.factories','ui.bootstrap'], function($httpProvider)
{
  // Use x-www-form-urlencoded Content-Type
  $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
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
  }).config(function ($httpProvider) {
	 $httpProvider.responseInterceptors.push(function ($rootScope) {
		  $rootScope.numLoadings = 0;
		  $rootScope.loading = false;
		  return function (promise) {
			$rootScope.numLoadings++;
			$rootScope.loading = true;
			// make sure the loading screen is visible
			var hide = function (r) {
			  if ((--$rootScope.numLoadings)===0){
				//console.log('hide the loading screen');
				$rootScope.loading = false;
			  }
			  return r;
			};
			return promise.then(hide, hide);
		  };
		});
}).directive('focus', function () {
  return function (scope, element, attrs) {
      attrs.$observe('focus', function (newValue) {
            newValue === 'true' && element[0].focus();
                });
                  }
                  });
	


app.config(['$httpProvider', function($httpProvider) {  
        $httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common['X-Requested-With'];
  }]);
  
/* Todo,
	- refresh button on sidebar and/or auto refresh mechanism
*/
