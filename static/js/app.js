'use strict';

var data = {
    labels: ["NAVER review", "Watcha review", "Harry Potter", "Lord of the Rings"],
    datasets: [
        {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.5)",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "rgba(220,220,220,0.75)",
            highlightStroke: "rgba(220,220,220,1)",
            data: [51114728, 27556222, 1084000, 473000]
        },
        {
            label: "My Second dataset",
            fillColor: "rgba(151,187,205,0.5)",
            strokeColor: "rgba(151,187,205,0.8)",
            highlightFill: "rgba(151,187,205,0.75)",
            highlightStroke: "rgba(151,187,205,1)",
            data: [7594020, 2523652, 0, 0]
        }
    ]
};
var ctx = document.getElementById("myChart").getContext("2d");
var myBarChart = new Chart(ctx).Bar(data, {scaleShowLabels: true});


var global;

var reviewApp = angular.module('reviewApp',['wu.masonry','angular-loading-bar'])
.directive('reviewDirective', ['$timeout', function($timeout) {
  return function(scope, element, attrs) {
    if (scope.$last){
      $timeout(function () {
        $('.poster').tooltip();

        $('div.raty').raty({
          size: 20,
          path: '/static/img',
          score: function() {
            return $(this).attr('data-score');
          }
        });
      }, 0, false);

      $timeout(function () {
        var imgLoad = imagesLoaded($('.poster'));
        imgLoad.on( 'always', function( instance ) {
          console.log('ALWAYS - all images have been loaded');
          var container = document.querySelector('#reviews');
          var msnry = new Masonry( container, {
            itemSelector: '.review',
            columnWidth: '.col-md-5',
            gutter: 0
          });
        });
      }, 2, false);
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
  $http.get('/r/cached/50').success(function(data) {
    reviews = data.data;
    $scope.reviews = data.data;
  });

  $scope.prediction();
});
