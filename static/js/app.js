'use strict';

var global;

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
}]).filter('reverse', function() {
  return function(items) {
    return items.slice().reverse();
  };
});

var reviews = [];

reviewApp.controller('reviewController', function($scope, $http) {
  $scope.reviews = [];
  $scope.sentences = [];

  $scope.prediction = function() {
    //$http.post('/r/predict', data).success(function(data) {
    $http({url:'/r/predict',
           data: {text: $('#text')[0].value},
           method: 'POST',
           transformRequest: function(obj) {
             var str = [];
             for(var p in obj)
             str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
             return str.join("&");
           },
           headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    }).success(function(data) {
      $scope.sentences.push({text:data.data[0].text[1], pred:data.data[0].pred});
    });
  };

  //$http.get('/r/get/20').success(function(data) {
  $http.get('/r/cached/30').success(function(data) {
    reviews = data.data;
    $scope.reviews = data.data;
  });
});
