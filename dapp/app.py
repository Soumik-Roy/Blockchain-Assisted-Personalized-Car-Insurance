import json
from web3 import Web3, HTTPProvider
 
# truffle development blockchain address
blockchain_address = 'http://localhost:8000'
 
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address)) 
 
web3.eth.defaultAccount = web3.eth.accounts[0]
 
# Setting the default account (so we don't need 
#to set the "from" for every transaction call)
 
# Path to the compiled contract JSON file
compiled_contract_path = '../smartcontract/build/contracts/CarInsurance.json'
 
# Deployed contract address (see `migrate` command output: 
# `contract address`)
# Do Not Copy from here, contract address will be different 
# for different contracts.
deployed_contract_address = '0x7435FDa0c91c1eFD489e6704ac5845F36a6bD535'
 
# load contract info as JSON
with open(compiled_contract_path) as file:
    contract_json = json.load(file)  
     
    # fetch contract's abi - necessary to call its functions
    contract_abi = contract_json['abi']
 
# Fetching deployed contract reference
contract = web3.eth.contract(
    address = deployed_contract_address, abi = contract_abi)
 
# Calling contract function (this is not persisted 
# to the blockchain)
output = contract.functions.getBalance().call()

print(output)