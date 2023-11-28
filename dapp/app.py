import json
from web3 import Web3, HTTPProvider
import click
 
# truffle development blockchain address
blockchain_address = 'http://172.31.10.78:8000'

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
car_insurance_contract = web3.eth.contract(
    address = deployed_contract_address, abi = contract_abi)
 
# Calling contract function (this is not persisted 
# to the blockchain)
# output = car_insurance_contract.functions.getBalance().call()


# print(output)

##################################### CLI CODE #######################################


# Update these values with your actual contract address and ABI
# contract_address = "0xYourContractAddress"
# contract_abi = [...]  # Replace with your contract ABI

# Connect to the local Ganache node or your blockchain node
# web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Create a contract instance
# car_insurance_contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def wei_to_ether(wei):
    return wei / 1e18

# Function to get the user's balance
def get_balance(user_address):
    return car_insurance_contract.functions.getBalance(user_address).call()

# Function to check if a user is insured
def is_insured(user_address):
    return car_insurance_contract.functions.isInsured(user_address).call()

# Function to get the premium for a user
def get_premium(user_address):
    return car_insurance_contract.functions.getPremium(user_address).call()

# Function to underwrite and pay premium
def underwrite(user_address):
    premium = get_premium(user_address)
    value_to_send = premium
    transaction_hash = car_insurance_contract.functions.underwrite().transact({
        'from': user_address,
        'value': value_to_send
    })  
    return transaction_hash

# Function to make a claim
def claim(user_address):
    transaction_hash = car_insurance_contract.functions.claim().transact({
        'from': user_address
    })
    return transaction_hash

# Function to perform an audit
def audit(user_address, password):
    return car_insurance_contract.functions.audit(password).call({'from': user_address})

@click.command()
@click.option('--user-address', prompt='Enter your Ethereum address', help='Your Ethereum address')
def main(user_address):
    click.echo(f'Connected to Ethereum node: {web3.is_connected()}')
    click.echo(f'User Address: {user_address}')

    while True:
        click.echo("\nOptions:")
        click.echo("1. Get Balance")
        click.echo("2. Check if Insured")
        click.echo("3. Get Premium")
        click.echo("4. Underwrite (Pay Premium)")
        click.echo("5. Make a Claim")
        click.echo("6. Audit")
        click.echo("0. Exit")

        choice = click.prompt("Enter your choice (0-6)", type=int)

        if choice == 0:
            break
        elif choice == 1:
            balance = get_balance(user_address)
            click.echo(f'Balance: {wei_to_ether(balance)} Eth')
        elif choice == 2:
            insured = is_insured(user_address)
            click.echo(f'Is Insured: {insured}')
        elif choice == 3:
            premium = get_premium(user_address)
            click.echo(f'Premium: {wei_to_ether(premium)} Eth')
        elif choice == 4:
            tx_hash = underwrite(user_address)
            click.echo(f'Underwrite Transaction Hash: {tx_hash.hex()}')
        elif choice == 5:
            tx_hash = claim(user_address)
            click.echo(f'Claim Transaction Hash: {tx_hash.hex()}')
        elif choice == 6:
            password = click.prompt("Enter the audit password", type=str)
            result = audit(user_address, password)
            click.echo(f'Audit Result: {result}')
        else:
            click.echo("Invalid choice. Please enter a number between 0 and 6.")

if __name__ == '__main__':
    main()
