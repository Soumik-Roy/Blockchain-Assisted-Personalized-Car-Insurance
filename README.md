# Blockchain-Assisted-Personalized-Car-Insurance

A simplified Proof-of-Concept Implementation for a [Blockchain-Assisted Personalized Car Insurance With Privacy Preservation and Fraud Resistance](https://ieeexplore.ieee.org/document/9924540). 

## Running The Application

### Pre-Requisites:
The following are the pre-requisitesthat need to be installed to run the project.
- Node JS (>16.0.0)
- Python
- Ganache

Further Clone the Repository locally using : 
```
git clone https://github.com/Soumik-Roy/Blockchain-Assisted-Personalized-Car-Insurance.git
```

### Set Up

First set up a Virtual Environment (using pipenv). You can skip this and do follow corresponding steps if using some other method to create Virtual Environment: 
```
mkdir .venv
pipenv shell
```

Install Dependancies
```
pip install -r requirements.txt
```

Install Truffle
```
npm install -g truffle
```

Now open Ganache and do the following : 
- Create New Workspace
- Setup current project's smart contract folder as truffle directory

Compile Smart Contracts 
```
cd smartcontract
truffle compile
```

Deploy Contract (If you act as the the Main Node)
```
npx truffle migrate --network develop
cd ..
```

Run the Decentralised App
```
cd dapp
python app.py
```
