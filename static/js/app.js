'use strict';

var reviewApp = angular.module('reviewApp',['wu.masonry','angular-loading-bar'])
.directive('reviewDirective', ['$timeout', function($timeout) {
  return function(scope, element, attrs) {
    if (scope.$last){
      $timeout(function () {
        $('.poster').tooltip();
        /*var container = document.querySelector('#reviews');
        var msnry = new Masonry( container, {
          itemSelector: '.review',
          columnWidth: '.review',                
        });*/
        $('div.raty').raty({
          path: '/static/img',
          score: function() {
            return $(this).attr('data-score');
          }
        });
      }, 0, false);
    }
  };
}]);
var reviews = [];

var prediction = function() {
  $('#text')
};

reviewApp.controller('reviewController', function($scope, $http) {
  $scope.reviews = [];

  //$http.get('/r/get/20').success(function(data) {
  $http.get('/r/cached/20').success(function(data) {
    reviews = data.data;
    $scope.reviews = data.data;
  });
});
