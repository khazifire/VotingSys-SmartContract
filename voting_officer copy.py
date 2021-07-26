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

contractInfo = {'contract_address':'0x487716bF0DBb841e969a34d4B47180215A94feC4','account_address' :'0x3805260C3a0E7Ced95142cc2bD0519130a69c2b6','account_private_key':'e70a15578a5d582d2ec937b200edfd4e57a6020d38b3de05fe0108ca7b64d422'}

w3.eth.default_account = contractInfo['account_address'] 

votingsystem = w3.eth.contract(address=contractInfo['contract_address'], abi=abi)


def register_voter_acc():
    voter_address = '0x5a63fCcf8C5e881381aC7f839Af15C22CdC1fd23'
    voter_fname = '0x64616e'
    voter_lname = '0x64616e'
    voter_age = 15

    transaction = votingsystem.functions.register_voter_account(voter_address,voter_fname,voter_lname, voter_age).buildTransaction({
        'gas': 1000000,  
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': w3.eth.getTransactionCount(w3.eth.defaultAccount)
    })
    signed = w3.eth.account.signTransaction(transaction, private_key=contractInfo["account_private_key"])
    w3.eth.sendRawTransaction(signed.rawTransaction)
  


register_voter_acc()

    
    