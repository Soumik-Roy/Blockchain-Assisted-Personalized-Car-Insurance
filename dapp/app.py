import sys
import json
from web3 import Web3, HTTPProvider
import click
import keyboard
 
# truffle development blockchain address
blockchain_address = 'http://172.31.10.78:8000'
# blockchain_address = 'http://localhost:8000'

# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address)) 
 
web3.eth.defaultAccount = web3.eth.accounts[0]
 
# Path to the compiled contract JSON file
compiled_contract_path = '../smartcontract/build/contracts/CarInsurance.json'
 
# Deployed contract address (see `migrate` command output: `contract address`).
deployed_contract_address = '0xB6f1c380280C02C671FC011134c5Ba3d6099c613'
 
# load contract info as JSON
with open(compiled_contract_path) as file:
    contract_json = json.load(file)  
     
    # fetch contract's abi - necessary to call its functions
    contract_abi = contract_json['abi']
 
# Fetching deployed contract reference
car_insurance_contract = web3.eth.contract(
    address = deployed_contract_address, abi = contract_abi)

def wei_to_ether(wei):
    return wei / 1e18

def ether_to_wei(eth):
    return eth * 1e18

# Function to get the user's balance
def get_balance(user_address):
    # print(user_address)
    return car_insurance_contract.functions.getBalance().call({
        'from': user_address
    })

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
    return (premium, transaction_hash)

# Function to make a claim
def claim(user_address):
    transaction_hash = car_insurance_contract.functions.claim().transact({
        'from': user_address
    })
    return transaction_hash

# Function to perform an audit
def audit(user_address, password, claim_penalty, defaulter_penalty):
    return car_insurance_contract.functions.audit(password, int(ether_to_wei(claim_penalty)), int(ether_to_wei(defaulter_penalty))).call({'from': user_address})

@click.command()
@click.option('--user-address', prompt='Enter your Ethereum address', help='Your Ethereum address')

def main(user_address):
    if user_address not in web3.eth.accounts:
        click.echo('Invalid user address provided!')
        sys.exit(0)
    click.echo(f'Connected to Ethereum node: {web3.is_connected()}')
    click.echo(f'User Address: {user_address}')

    while True:
        click.clear()
        click.echo("\nOptions:")
        click.echo("1. Check Balance")
        click.echo("2. Check Insurance Status")
        click.echo("3. Check Monthly Premium")
        click.echo("4. Pay Premium (Underwrite)")
        click.echo("5. Make a Claim")
        click.echo("6. Audit")
        click.echo("0. Exit")

        choice = click.prompt("Enter your choice (0-6)", type=int)

        if choice == 0:
            break
        elif choice == 1:
            balance = get_balance(user_address)
            click.secho(f'Your balance is ', fg = "yellow", nl = False)
            click.secho(f'{wei_to_ether(balance)} ETH', fg = "green")
        elif choice == 2:
            insured = is_insured(user_address)
            if insured:
                click.secho('You are insured', fg = "yellow")
            else:
                click.secho('You are not insured', fg = "red")
        elif choice == 3:
            premium = get_premium(user_address)
            click.echo(click.style(f'Your monthly insurance premium: ', fg = "yellow"), nl = False)
            click.secho(f'{wei_to_ether(premium)} ETH', fg = "green")
        elif choice == 4:
            premium, tx_hash = underwrite(user_address)
            click.echo(click.style(f'Paid Premium to Insurance Company : ', fg = "yellow"), nl = False)
            click.secho(f'{wei_to_ether(premium)} ETH', fg = "green")
            click.echo(click.style(f'Underwrite Transaction Hash: ', fg = "yellow"), nl = False)
            click.secho(f'{tx_hash.hex()}', fg = "green")
        elif choice == 5:
            tx_hash = claim(user_address)
            click.echo(click.style(f'Claim Transaction Hash: ', fg = "yellow"), nl = False)
            click.secho(f'{tx_hash.hex()}', fg = "green")
            click.echo(click.style(f'Received Insurance Claim of ', fg = "yellow"), nl = False)
            click.secho(f'1 ETH', fg = "green")

        elif choice == 6:
            password = click.prompt("Enter the audit password", type=str)
            claim_penalty = click.prompt("Enter the premium added per claim:", type = float)
            defaulter_penalty = click.prompt("Enter the defaulter penalty:", type = float)
            try:
                result = audit(user_address, password, claim_penalty, defaulter_penalty)
                click.secho(click.style(f'Audit Result: ', fg = "yellow"), nl = False)
                click.secho(f'{result}', fg = "green")
            except:
                click.secho("Access Denied!", fg = "red")
        else:
            click.secho("Invalid choice! Please enter a number between 0 and 6.", fg = "magenta")

        click.secho("\nPress any key to continue...", fg = "cyan", blink = True)
        click.getchar()

if __name__ == '__main__':
    main()



'''
Addresses:-
- Contract : 0x7435FDa0c91c1eFD489e6704ac5845F36a6bD535
- Deployer (Admin) : 0xA582Bb26b75CC41A316b8F8354B2736E3119d165

 Users :- 
- 0x3Ff76d9655fc005D9A3DB74a232a7798A0fA61C9
- 0x79831523B4CD3344b2aD755F070337BA5B4ffAb8
- 0x7E101bf1Ca3f2C9Ae09329D2a519a8FF09c4f898
- 0xB619e3A79526570fC6a010CBe63cc6560A928361
- 0xDCfF0A8950Ba5848157aba3C562968Adc6701c97

'''

