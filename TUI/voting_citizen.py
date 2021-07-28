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

contractInfo = {'contract_address':'','account_address' :'','account_private_key':''}



votingsystem = w3.eth.contract(address=contractInfo['contract_address'], abi=abi)


def clear_console():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def exit_Program():
    print("")
    print("."*20," Exiting Program ", "."*20)
    sleep(1)
    clear_console()

def success_msg(msg):
    print()
    print(">"*15,f"| {msg} |","<"*15)
    print()
    sleep(3)
    clear_console()

def error_msg(msg):
    print("<"*15,f"| {msg} |",">"*15)
    sleep(2)
    clear_console()

def option_title(title):
    print("\n","="*15,f"| {title} |","="*15,"\n")


def set_default_account():
    clear_console()

    try:
        account_address = str(input("Enter Account Address:")).strip()
        account_private_key = str(input("Please enter the private key: ")).strip()
        contractInfo['account_address'] = account_address
        contractInfo['account_private_key'] = account_private_key
        votingsystem = w3.eth.contract(address=contractInfo['contract_address'], abi=abi)
        success_msg(f"Default Account has been set to {account_address}")
    except:
        error_msg("The address you entered is not in the correct format")
        


def set_contract_account():
    clear_console()
    option_title("Setting up contract account")
    try:
        contract_addr = str(input("Address of the contract: ")).strip()
        contractInfo["contract_address"] = Web3.toChecksumAddress(contract_addr)
        success_msg("The Contract Address has been set")
    except:
        error_msg("The address you entered is not in the correct format")


def get_name_candidate(candidate_index):
    candidate_name = votingsystem.functions.get_candidate_name(candidate_index).call()
    return candidate_name
  


def vote_candidate():
    clear_console()
    option_title("Vote for candidates based on the list below")
    print("")
    for x in range(0,3):
        print(f"{x}. {get_name_candidate(x)}")
    print("To vote simply enter the number of the candidate")
   
    candidate_index = int(input("Candidate Number: "))
    transaction = votingsystem.functions.vote_for_candidate(contractInfo["account_address"],candidate_index).buildTransaction({
        'gas': 100000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': w3.eth.getTransactionCount(w3.eth.defaultAccount)
    })
    sign_transaction(transaction)
    success_msg(f"you successfully votes for {get_name_candidate(candidate_index)}")


def get_vote_sum():
    for x in range(0,3):
        candidate_name = votingsystem.functions.get_candidate_name(x).call()
        candidate_votes= votingsystem.functions.get_result_sum(contractInfo["account_address"],x).call()
        print(f"candidate name: {candidate_name} : number of votes {candidate_votes}")


def get_winner():
    vote_result= votingsystem.functions.get_vote_results(contractInfo["account_address"]).call()
    name = votingsystem.functions.get_leading_candidate_name(contractInfo["account_address"], vote_result[0]).call()
    success_msg(f"Current leading candidate is {name} with {vote_result[1]} votes")
    
   


def sign_transaction(transaction):
    signed = w3.eth.account.signTransaction(transaction, private_key=contractInfo["account_private_key"])
    w3.eth.sendRawTransaction(signed.rawTransaction)


# set_default_account()
# set_contract_account()
# w3.eth.default_account = contractInfo['account_address'] 
# votingsystem = w3.eth.contract(address=contractInfo['contract_address'], abi=abi)


def nav_menu(option):
    menu_option ={
        1: set_default_account,
        2: set_contract_account,
        3: vote_candidate,
        4: get_vote_sum,
        5: get_winner
      
     
    }
    menu_option.get(option, "Invalid Input")()

menu_options = {
    1: "Set an owner default account",
    2: "Set contract account",
    3: "Get the owner account address",
    4: "Register a student account",
    5: "Get the contract’s balance in AUC" ,
}

def welcome():
    print("")
    option_title("Welcome to AIU Coins Smart Contract")
    sleep(2)
    clear_console()

def requirements():
    if  not contractInfo['account_address'] or not contractInfo['account_private_key'] or not contractInfo['contract_address']:
        option_title("Please etnter the following required information")
        sleep(1)
        nav_menu(1)
        nav_menu(2)

welcome()
requirements() 

w3.eth.default_account = contractInfo['account_address'] 
votingsystem = w3.eth.contract(address=contractInfo['contract_address'], abi=abi)

while True:
    option_title("AIU Coin Smart Contract")
    for key, value in menu_options.items():
        print(f"| {key}: {value}")
    
    try:
        print("")
        option = int(input(" What would you like to do (1,2,4...)? :"))
        nav_menu(option)
    except ValueError:
        print("")
        print("<"*10," Invalid Input, enter the number of the option you want to carry out (1-15) ", ">"*10)
        sleep(2)
        clear_console()