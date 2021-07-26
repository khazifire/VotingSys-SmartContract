from web3 import Web3, HTTPProvider, contract
from vyper import compile_codes as compile
from os import system, name
from time import sleep
import datetime

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

contractInfo = {
    'contract_address':'0x8FaD770CCc24bb74D3b7E49189D14c4e5d217e83',

    'account_address' :'0x807ED97741A1EBc86bC55959b3a0B81b9c399260','account_private_key':'f89946b21eae2d50e1eeadb202496b7bb317652ff3809580ccb3bbfe5ab0d001'}

w3.eth.default_account = contractInfo['account_address'] 

votingsystem = w3.eth.contract(address=contractInfo['contract_address'], abi=abi)


  
def register_voter_acc():
    voter_address = '0x4d3a2Ac27223f990C4333568D641F471555BeD60'
    voter_fname = 'dan'
    voter_lname = 'test'
    voter_age = 6

    transaction = votingsystem.functions.register_voter_account(voter_address,voter_fname,voter_lname, voter_age).buildTransaction({
        'from': contractInfo['account_address'],
        'gas': 3000000,
        'gasPrice': w3.toWei('40', 'gwei'),
        'nonce': w3.eth.getTransactionCount(w3.eth.defaultAccount)
    })
    print(contractInfo['account_private_key'])
    signed = w3.eth.account.signTransaction(transaction, private_key=contractInfo["account_private_key"])

    signed_txn = w3.eth.sendRawTransaction(signed.rawTransaction)

    return w3.eth.waitForTransactionReceipt(signed_txn)

register_voter_acc()

