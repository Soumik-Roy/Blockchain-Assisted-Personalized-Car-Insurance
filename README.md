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

1. First set up a Virtual Environment (using pipenv). You can skip this and do follow corresponding steps if using some other method to create Virtual Environment: 
    ```
    mkdir .venv
    pipenv shell
    ```

2. Install Dependancies
    ```
    pip install -r requirements.txt
    ```

3. Install Truffle
    ```
    npm install -g truffle
    ```

4. Now open Ganache and do the following : 
    - Create New Workspace
    - Setup current project's smart contract folder as truffle directory
    - Set the following configurations in Settings->Server


    ![image](https://github.com/Soumik-Roy/Blockchain-Assisted-Personalized-Car-Insurance/assets/77190361/3fa6a8a7-17db-4f98-b188-5d1355feaa07)

    Here, the 0.0.0.0 endpoint reflects that the blockchain will be deployed locally and thus will listen for connections on all IP addresses that the machine supports.
    Hence it will be accessible by any device connected to the same wifi network.
   
    Or if you need different configurations, then reflect the same in network section (develop) of `./smartcontracts/truffle-config.js`.


6. Compile the Smart Contracts 
    ```
    cd smartcontract
    truffle compile
    ```

7. Deploy Contract (If you act as the the Main Node). 
    ```
    npx truffle migrate --network develop
    cd ..
    ```
    
    By default the blockchain uses the `develop` network. You can configure stuff differently if required, and use `npx truffle --network <network-name>` correspondingly.

8. Set proper contract address and deployment url by changing the `blockchain_address` and `deployed_contract_address` variables in `./dapp/app.py` to respective values.

   Open Canache, go to Contracts->CarInsurance, and copy the value of its address into `deployed_contract_address`. Whenever you re-deploy your contract, update the value of this variable to corresponding address.

   If running on the machine, where the blockchain is deployed (on ganache), then set blockchain_address to `http://localhost:8000`. If running on a seperate device on same wifi network, then run the following command in your command prompt, and copy the value of your network's ipv4 address (eg 192.55.44.01):
   ```
   ipconfig
   ```
   Then set blockchain_address to `http://<ip-address>:8000`

10. Run the Decentralised App CLI
    ```
    cd dapp
    python app.py
    ```

## Using the D-App
A simple CLI dapp has been made, where the user is first asked their etherium account address (can be found in Ganache->Accounts section). Then the user can select any of the available options to interact with the Car Insurance company's blockchain.

![image](https://github.com/Soumik-Roy/Blockchain-Assisted-Personalized-Car-Insurance/assets/77190361/796e7781-a888-46d8-a9d4-34f68ee030a2)

![image](https://github.com/Soumik-Roy/Blockchain-Assisted-Personalized-Car-Insurance/assets/77190361/d931513f-8984-4df4-9a58-3d01d0e6518e)

![image](https://github.com/Soumik-Roy/Blockchain-Assisted-Personalized-Car-Insurance/assets/77190361/a98309e1-8bee-4443-b80e-7183a2df8fa8)
