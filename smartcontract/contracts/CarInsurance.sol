// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.4.15;

import './Insurance.sol';
import './Algorithms.sol';

contract CarInsurance is Insurance {

    struct InsuranceTaker {
        bool isDefaulter;
        bool policyInValid;
        uint256 lastPayment;
        uint256 numClaims;
    }

    address[] private insuranceTakerIds;
    mapping (address => bool) private isACustomer;

    mapping(address => InsuranceTaker) private insuranceTakers;

    uint256 private paymentPeriod = 30 days;

    uint256 private premiumPerClaim = 0.1 ether;

    uint256 private defaulterPenalty = 0.2 ether;

    uint256 private claimPayment = 1 ether;

    uint256 private balance;

    // uint256 public balance = 0 ether;


    constructor() payable {
        balance = msg.value;
    }

    function getBalance() public view returns (uint256) {
        return balance;
    }

    function underwrite() override payable public {
        if (!isACustomer[msg.sender]) {
             insuranceTakerIds.push(msg.sender);
             isACustomer[msg.sender] = true;
         }

        InsuranceTaker storage customer = insuranceTakers[msg.sender];

        // do not accept new customers that have been isDefaulter previously
        require(!customer.isDefaulter);

        // in order to underwrite the customer needs to pay the first premium upfront
        require(msg.value == getPremium(msg.sender));

        customer.lastPayment = block.timestamp;
        customer.policyInValid = false;

    }

    function update(address insuranceTaker) override  public {
        // if insurance taker did not pay within required interval they will loose their insurance
        // and will be isDefaulter for future insurance policies

        InsuranceTaker storage customer = insuranceTakers[insuranceTaker];

        if (!customer.policyInValid && customer.lastPayment + paymentPeriod < block.timestamp) {
            customer.policyInValid = false;
            customer.isDefaulter = true;
        }
    }

    // checks if an insurance taker is currently insured
    function isInsured(address insuranceTaker) override view public returns (bool insured) {
        InsuranceTaker storage customer = insuranceTakers[insuranceTaker];
        return !customer.policyInValid;
    }

    // calculates the premium for an insurance taker
    function getPremium(address insuranceTaker) override view public returns (uint256 premium) {
        InsuranceTaker storage customer = insuranceTakers[insuranceTaker];

        if (customer.isDefaulter){
            return (customer.numClaims + 1) * premiumPerClaim + defaulterPenalty;
        }
        return (customer.numClaims + 1) * premiumPerClaim;
    }

    // allows premium to be paid by separate account
    function payPremiumFor(address insuranceTaker) override public payable {
        if (!isACustomer[insuranceTaker]) {
             insuranceTakerIds.push(insuranceTaker);
             isACustomer[insuranceTaker] = true;
         }

        InsuranceTaker storage customer = insuranceTakers[insuranceTaker];

        // check if last payment is overdue, if so -> ban
        update(insuranceTaker);

        // only accept correct amount
        require(msg.value == getPremium(insuranceTaker));

        // only accept payment from valid insurance takers
        require(isInsured(insuranceTaker));

        customer.lastPayment = block.timestamp;
        balance += msg.value;
    }

    function claim() override public payable{
        require(isInsured(msg.sender));

        if (!isACustomer[msg.sender]) {
             insuranceTakerIds.push(msg.sender);
             isACustomer[msg.sender] = true;
         }
        InsuranceTaker storage customer = insuranceTakers[msg.sender];
        payable (msg.sender).transfer(claimPayment);
        balance -= claimPayment;
        customer.numClaims++;
    }

    function audit(string memory pswd, uint256 claimCoeff, uint256 defCoeff) public view returns (bool validity){
        // string memory accessPswd = "government";
        // args: government, 100000000000000000, 200000000000000000
        require(keccak256(abi.encodePacked(pswd)) == keccak256(abi.encodePacked("government")), "Do not have access to audit");
        bool allValid = true;
        for (uint i = 0; i<insuranceTakerIds.length; i++) 
        {
            InsuranceTaker storage customer = insuranceTakers[insuranceTakerIds[i]];
            uint256 premium; 
            
            if (customer.isDefaulter){
                premium = (customer.numClaims + 1) * claimCoeff + defCoeff;
            }
            premium = (customer.numClaims + 1) * claimCoeff;

            if(premium != getPremium(insuranceTakerIds[i])){
                allValid = false;
                break ;
            }

        }
        return allValid;
    }

}