from web3 import Web3, EthereumTesterProvider

provider_url = "https://mainnet.infura.io/v3/83bc13f26ace458d999ff5e28b2b4154"

# w3 = Web3(EthereumTesterProvider())
w3 = Web3(Web3.HTTPProvider(provider_url))

def getLatestBlock():
    return w3.eth.get_block('latest')

def isAddressValid(address):
    return w3.is_address(address)

def getBalance(address):
    wallet = w3.to_checksum_address(address)
    return w3.eth.get_balance(wallet)

