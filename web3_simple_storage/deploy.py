from solcx import compile_standard, install_solc  # <- import the install_solc method!
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
install_solc("0.6.0")  # <- Add this line and run it at least once!

with open("SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compiling sol file
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

#print("compiled_sol")

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode 
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
    ]["object"]

# get abi

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x2bf460e66FaA9056290363676feC317806723458"
#private_key = "0xb9b824cde38c2abfdf9a447803f48d8201433f57976e0473f7c4171185d7f515"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
#print(SimpleStorage)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
#print(nonce)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
#print(transaction)

signed_tcn = w3.eth.account.sign_transaction(transaction, private_key = private_key)
print(private_key)