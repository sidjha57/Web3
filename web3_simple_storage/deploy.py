from solcx import compile_standard, install_solc  # <- import the install_solc method!
import json
from web3 import Web3

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

print("compiled_sol")

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
chain_id = 5777
my_address = "0x7Da1857970d86b44a74d32D4dc24361E4112f6C6"
private_key = "0xa0a25561d3cdd8d6e4f18bf04372043a02a9db52be127037259b345d9821a17c"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
print(SimpleStorage)