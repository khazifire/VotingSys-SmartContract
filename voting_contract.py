from web3 import Web3, HTTPProvider
from vyper import compile_codes as compile

votesys = open("./vote.vy", 'r')
contract_source_code = votesys.read()
votesys.close()


smart_contract = {}
smart_contract['votesys'] = contract_source_code

format = ['abi', 'bytecode']
compiled_code = compile(smart_contract,format, 'dict')

abi = compiled_code['votesys']['abi']
bytecode = compiled_code['votesys']['bytecode']

w3 = Web3(HTTPProvider('http://localhost:7545'))

#for creation of the contract
votingsystem = w3.eth.contract(bytecode=bytecode, abi=abi)

try:
    account_address = Web3.toChecksumAddress(str(input("Account Address to Initiate contract: ")))
    tx_hash = votingsystem.constructor().transact({
        'from': account_address
    })
    print("\n","-------creation of contract completed ------","\n")
except:
    print("\n","-------creation of contract failed----------","\n")

