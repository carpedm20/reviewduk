'use strict';

var reviewApp = angular.module('reviewApp',['angular-loading-bar']);
var reviews = [];

var prediction = function() {
  $('#text')
};

reviewApp.controller('reviewController', function($scope, $http) {
  $scope.reviews = [];

  $http.get('/r/get/10').success(function(data) {
    reviews = data.data;
    $scope.reviews = data.data;
  });
});
