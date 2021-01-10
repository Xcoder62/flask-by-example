app.controller('WordcountController', ['$scope', '$log',
function($scope, $log) {
  $scope.list = ["clean room", "read books"];
  $scope.getResults = function() {
    $log.log("test");
  };
}
]);