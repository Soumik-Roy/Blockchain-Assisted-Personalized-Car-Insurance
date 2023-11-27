// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.4.15;

// abstract base contract for insurances
abstract contract Insurance {
    // fallback function accepts premium payment for msg.sender;
    fallback() external payable {
        payPremiumFor(msg.sender);
    }

    receive() external payable {
        // custom function code
    }


    function underwrite() virtual  payable public;

    function update(address insuranceTaker) virtual public;

    function isInsured(address insuranceTaker) virtual public returns (bool insured);

    function getPremium(address insuranceTaker) virtual public returns (uint256 premium);


    function payPremiumFor(address insuranceTaker) virtual public payable;

    function claim() virtual public payable;
}
