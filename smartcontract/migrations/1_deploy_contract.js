
var Insurance = artifacts.require("Insurance");
var CarInsurance = artifacts.require("CarInsurance");
 
module.exports = function(deployer) {
    deployer.deploy(CarInsurance,10);
};