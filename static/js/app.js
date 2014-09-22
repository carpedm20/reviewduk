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
          size: 20,
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

reviewApp.controller('reviewController', function($scope, $http) {
  $scope.reviews = [];
  $scope.sentences = [];

  $scope.prediction = function() {
    $http.post('/r/predict', {'text': $('#text')[0].value}).success(function(data) {
      $scope.sentences.push(data.data[0]);
    });
  };

  //$http.get('/r/get/20').success(function(data) {
  $http.get('/r/cached/30').success(function(data) {
    reviews = data.data;
    $scope.reviews = data.data;
  });
});
