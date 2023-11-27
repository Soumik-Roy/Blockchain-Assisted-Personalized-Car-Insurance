
var Insurance = artifacts.require("Insurance");
var CarInsurance = artifacts.require("CarInsurance");
 
module.exports = function(deployer) {
    deployer.deploy(CarInsurance, {value: 10000000000000000000});
};