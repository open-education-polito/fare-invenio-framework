import angular from "angular";

var fileUploadModule = angular.module('fileUploadModule', []);

fileUploadModule.directive('fileModel', ['$parse', function ($parse) {
  return {
     restrict: 'A',
     link: function(scope, element, attrs) {
        var model = $parse(attrs.fileModel);
        var modelSetter = model.assign;

        element.bind('change', function() {
           scope.$apply(function() {
              modelSetter(scope, element[0].files[0]);
           });
        });
     }
  };
}]);

fileUploadModule.service('fileUpload', ['$http', '$window', function ($http, $window) {
  this.uploadFileToUrl = function(uploadUrl, fields, file) {

    var isFormValid = true;

    // check if the form is valid
    for(var i=0; i<fields.length; i++){
      if(angular.isUndefined(fields[i])){
        isFormValid = false;
      }
    }
    if(angular.isUndefined(file)){
      isFormValid = false;
    }

    if(isFormValid){

      var fd = new FormData();
      fd.append('title', fields[0]);
      fd.append('contributor_name', fields[1]);
      fd.append('educationLevel', fields[2]);
      fd.append('subject', fields[3]);
      fd.append('coverage', fields[4]);
      fd.append('license', fields[5]);
      fd.append('description', fields[6]);
      fd.append('file_content', file);
      fd.append('csrf_token', fields[7]);

      $http.put(uploadUrl, fd, {
        transformRequest: angular.identity,
        headers: {'Content-Type': undefined}
      })
        .success(function(response) {
          console.log("SUCCESSO");
          console.log(response);
          $window.location.href = response;
        })
        .error(function(response) {
          console.log("ERRORE");
          console.log(response);
          //$window.location.href = 'create';
        });
    }

  }
}]);

fileUploadModule.controller('fileUploadController', ['$scope', 'fileUpload', function($scope, fileUpload) {
  $scope.uploadFile = function() {

    var fields = [];

    // adding the value of the fields to an array
    fields.push($scope.recordTitle);
    fields.push($scope.recordContributors);
    fields.push($scope.recordEducationLevel);
    fields.push($scope.recordSubject);
    fields.push($scope.recordCoverage);
    fields.push($scope.recordLicense);
    fields.push($scope.recordDescription);
    fields.push(angular.element(document.getElementById('csrf_token'))[0].value);
    var file = $scope.fileToUpload;
    var uploadUrl = "/file_management/create";

    console.log('file is ' );
    console.dir(file);

    fileUpload.uploadFileToUrl(uploadUrl, fields, file);
  };
}]);

