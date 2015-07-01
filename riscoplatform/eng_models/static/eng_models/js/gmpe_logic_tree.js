"use strict";

var gmpeLogicTreeApp = angular.module('gmpeLogicTreeApp', ['ui.sortable']).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});


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


gmpeLogicTreeApp.controller('gmpeLogicTreeCtrl', function($scope) {

	$scope.new_gmpes = [];

	$scope.regions = [{name: 'Continental',
						gmpes: ['AtkinsonBoore2010', 'Toro']},
						{name: 'Subduction',
						gmpes: ['Toro']}]

	$scope.levels =[{
		level: 1,
		tectonic_region: 'Subduction',
		gmpes: [{name: 'AtkinsonBoore2010',
				weight: 0.523423525},
				{name: 'Toro',
				weight: 0.5},
				{name: 'AtkinsonBoore2010',
				weight: 0.5},
				{name: 'Toro',
				weight: 0.5},
				{name: 'AtkinsonBoore2010',
				weight: 0.5},
				{name: 'Toro',
				weight: 0.5},
				]
	},
	{
		level: 2,
		tectonic_region: 'Inter slab',
		gmpes: [{name: 'AtkinsonBoore2010',
				weight: 0.5},
				{name: 'Toro',
				weight: 0.5},
				]
	},
	{
		level: 3,
		tectonic_region: 'Continental',
		gmpes: [{name: 'AtkinsonBoore2010',
				weight: 0.5},
				{name: 'Toro',
				weight: 0.5},
				]
	}];


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
	$scope.levels.push({level: $scope.levels.length , tectonic_region: region.name, gmpes: $scope.new_gmpes});
	$scope.new_region = undefined;
	$scope.gmpe = undefined;
	$scope.weight = undefined;
	$scope.new_gmpes = [];
}

$scope.addGMPE = function(gmpe, weight){
	$scope.new_gmpes.push({name: gmpe, weight: weight});
}


$scope.cantAddLevel = function(){
	if ($scope.new_gmpes.length == 0 ){
		return true;
	}
	else {
		var sum = 0;
		for (var i=0;i< $scope.new_gmpes.length; i++ ){
			sum = sum + $scope.new_gmpes[i].weight;
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