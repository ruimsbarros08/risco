"use strict";

var gmpeLogicTreeApp = angular.module('gmpeLogicTreeApp', ['ui.sortable', 'ui-notification']).config(function($interpolateProvider, NotificationProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');

    NotificationProvider.setOptions({
        delay: 10000,
        startTop: 20,
        startRight: 10,
        verticalSpacing: 20,
        horizontalSpacing: 20,
        positionX: 'left',
        positionY: 'bottom'
    });


});

gmpeLogicTreeApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);



// gmpeLogicTreeApp.filter('availableGMPEs', function() {

// 	return function(input) {

// 	    var output = [];

// 	    for (var i = 0; $scope.new_gmpes.length; i++ ){
// 	    	if ($scope.new_gmpes[i].name == input){
// 	    		output.push(input);
// 	    	}
// 	    }

// 	    return output;

//   }

// });



gmpeLogicTreeApp.factory('GMPEltLevels', function($http) {

    var url = document.URL.split('/');
    var model_id = url[url.length -2];

	var myService = {
	    get: function() {
		    var promise = $http.get('/models/logictree_gmpe/'+model_id+'/ajax/').then(function (response) {
		        return response.data;
		    });
		    return promise;
	    },
	    post: function(data) {
		    var promise = $http.post('/models/logictree_gmpe/'+model_id+'/ajax/', data).then(function (response) {
		        return response.data;
		    });
		    return promise;
	    },

	};
	return myService;
});



gmpeLogicTreeApp.directive('dragAlert', function() {
  	return function(scope, element) {
	    element.bind('mouseover', function() {
	      	element.css({'background-color': '#E3E3E3'});
	    });
	    element.bind('mouseout', function() {
	      	element.css({'background-color': '#ECF0F1'});
	    });
  	};
});


gmpeLogicTreeApp.controller('gmpeLogicTreeCtrl', function($scope, GMPEltLevels, Notification) {

	$scope.new_gmpes = [];

	GMPEltLevels.get().then(function(data){
		$scope.levels = data.levels;
		$scope.regions = data.regions;
	});

	$scope.save = function(){
		GMPEltLevels.post($scope.levels).then(function(data){
			$scope.levels = data.data;
			Notification.success('Logic tree updated');
		}).catch(function(){
			Notification.error('Error');

		});
	}



	$scope.getLevel = function(level){
		var index = $scope.levels.indexOf(level);
		return index+1;
	}


	$scope.checkFirst = function(level){
		var index = $scope.levels.indexOf(level);
		if (index == 0){
			return true;
		}
		else {
			return false;
		}
	}

	$scope.checkLast = function(level){
		var index = $scope.levels.indexOf(level);
		if (index == $scope.levels.length-1){
			return true;
		}
		else {
			return false;
		}
	}

	$scope.move = function(level, add){
		var index = $scope.levels.indexOf(level);
		$scope.levels.splice(index, 1);
		$scope.levels.splice(index+add, 0, level)
	}

	$scope.deleteLevel = function(level){
		var index = $scope.levels.indexOf(level);
		$scope.levels.splice(index, 1);
	}

	$scope.deleteGMPE = function(gmpe){
		$scope.gmpe = undefined;
		$scope.weight = undefined;
		var index = $scope.new_gmpes.indexOf(gmpe);
		$scope.new_gmpes.splice(index, 1);
	}

	$scope.addLevel = function(region){
		$scope.levels.push({fields: {tectonic_region: region.name}, gmpes: $scope.new_gmpes});
		$scope.new_region = undefined;
		$scope.gmpe = undefined;
		$scope.weight = undefined;
		$scope.new_gmpes = [];
	}

	$scope.addGMPE = function(gmpe, weight){
		$scope.new_gmpes.push({fields: {gmpe: gmpe, weight: weight}});
	}


	$scope.cantAddLevel = function(){
		if ($scope.new_gmpes.length == 0 ){
			return true;
		}
		else {
			var sum = 0;
			for (var i=0;i< $scope.new_gmpes.length; i++ ){
				sum = sum + $scope.new_gmpes[i].fields.weight;
			}
			if (sum != 1.0){
				return true;
			}
			return false;
		}
	}

	$scope.cantAddGMPE = function(){
		if ($scope.gmpe == undefined || $scope.weight == undefined ){
			return true;
		}
		else {
			return false;
		}
	}

	$scope.clearGMPEs = function(){
		$scope.gmpe = undefined;
		$scope.weight = undefined;
		$scope.new_gmpes = [];
	}


	$scope.sortableOptions = {
	    handle: '.panel-heading',
	}


});