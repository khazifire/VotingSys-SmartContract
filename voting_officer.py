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

w3.eth.default_account = contractInfo['account_address'] 

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

def register_voter_acc():
    clear_console()
    option_title("Registring Student Account")
  
    voter_address = '0x2A39E5dD730010dA3a9185f6437d139e18B01Bcd'
    voter_fname = 'dan'
    voter_lname = 'kazim'
    print("gas balnce: ", w3.eth.getBalance(contractInfo["account_address"]))
    birtYear = 2002
    year_now = datetime.datetime.now().year
    voter_age = year_now - birtYear

    transaction = votingsystem.functions.register_voter_account(voter_address,voter_fname,voter_lname, voter_age).buildTransaction({
        'gas': 1000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': w3.eth.getTransactionCount(w3.eth.defaultAccount)
    })
    signed = w3.eth.account.signTransaction(transaction, private_key=contractInfo["account_private_key"])
    w3.eth.sendRawTransaction(signed.rawTransaction)
    
# def register_voter_acc():
#     clear_console()
#     option_title("Registring Student Account")
#     try:
#         voter_address = Web3.toChecksumAddress(str(input("What is the address of the citizen: ")).strip())
#         voter_fname = str(input("Voter FirstName: ")).strip()
#         voter_lname = str(input("Voter LastName: ")).strip()
#         print(contractInfo)
#         birtYear = int(input("Birth Year: "))
#         year_now = datetime.datetime.now().year
#         voter_age = year_now - birtYear
#         print(birtYear,year_now,voter_age) 

#         transaction = votingsystem.functions.register_voter_account(voter_address,voter_fname,voter_lname, voter_age).buildTransaction({
#             'gas': 100000,
#             'gasPrice': w3.toWei('1', 'gwei'),
#             'nonce': w3.eth.getTransactionCount(w3.eth.defaultAccount)
#         })
#         signed = w3.eth.account.signTransaction(transaction, private_key=contractInfo["account_private_key"])
#         w3.eth.sendRawTransaction(signed.rawTransaction)
#         success_msg("citizen registration was successful")
#     except:
#         error_msg("citizen Registration Failed, please try agai")

def create_candidate_list():
    clear_console()
    option_title("generating candidate list (3 candidates)")

    try:
        for x in range(1,4):
            candidate_name = str(input("Voter FirstName: ")).strip()
            transaction = votingsystem.functions.generate_canditate_list(candidate_name).buildTransaction({
                'gas': 100000,
                'gasPrice': w3.toWei('1', 'gwei'),
                'nonce': w3.eth.getTransactionCount(w3.eth.defaultAccount)
            })
            sign_transaction(transaction)
            success_msg(f"{x}. {candidate_name} was added to the list")
        success_msg("3 candidates were succesully added to the candidate list")
    except:
        error_msg("citizen Registration Failed, please try again")

def get_name_candidate():
    option_title("Getting candidate name from index")
    try:
        candidate_index = int(input("Candidate Number (index #): "))
        candidate_name = votingsystem.functions.get_candidate_name(candidate_index).call()
        print(f"{candidate_name}")
    except:
        error_msg("candidate name could not be retrived, please enter the correct index")

def sign_transaction(transaction):
    signed = w3.eth.account.signTransaction(transaction, private_key=contractInfo["account_private_key"])
    w3.eth.sendRawTransaction(signed.rawTransaction)


def nav_menu(option):
    menu_option ={
        1: set_default_account,
        2: set_contract_account,
        3: register_voter_acc,
        4: create_candidate_list,
        5: get_name_candidate
      
     
    }
    menu_option.get(option, "Invalid Input")()

menu_options = {
    1: "Set an owner default account",
    2: "Set contract account",
    3: "Register citizen",
    4: "create voting candidate list",
    5: "get name of candidate in list using index" ,
}

def welcome():
    print("")
    option_title("Welcome to  smart voting system")
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
    
    # try:
    #     print("")
    #     option = int(input(" What would you like to do (1,2,4...)? :"))
    #     nav_menu(option)
    # except ValueError:
    #     print("")
    #     print("<"*10," Invalid Input, enter the number of the option you want to carry out (1-15) ", ">"*10)
    #     sleep(2)
    #     clear_console()

      
    print("")
    option = int(input(" What would you like to do (1,2,4...)? :"))
    nav_menu(option)
    
       