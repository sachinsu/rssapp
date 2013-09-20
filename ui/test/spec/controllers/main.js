'use strict';

describe('Controller: MainCtrl', function () {

  // load the controller's module
  beforeEach(module('projectApp'));
  beforeEach(module('ui.bootstrap'));  

  var MainCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    MainCtrl = $controller('MainCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.factory).not.toBe(null);
  });

  it ('should have function updateitem attached to scope',function () { 
    expect(scope.updateitem).toBeDefined();
  });
  
  it ('should have function keepunread attached to scope',function () { 
    expect(scope.keepunread).toBeDefined();  
  });

  // todo: add tests to verify other behaviour of the controller
  
});