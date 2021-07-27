from re import template
from web3 import Web3,WebsocketProvider, HTTPProvider
from django.shortcuts import redirect, render, reverse
from django.views import generic
from django.http import JsonResponse
from time import sleep
from django.contrib import messages


abi = '''[
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "name": "_from",
          "type": "address"
        },
        {
          "indexed": false,
          "name": "_timestamp",
          "type": "uint256"
        }
      ],
      "name": "CreateVoterAccount",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "name": "_from",
          "type": "address"
        },
        {
          "indexed": false,
          "name": "_candidate_index",
          "type": "uint256"
        },
        {
          "indexed": false,
          "name": "_timestamp",
          "type": "uint256"
        }
      ],
      "name": "VotedForCandidate",
      "type": "event"
    },
    {
      "inputs": [],
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "gas": 1467159,
      "inputs": [
        {
          "name": "_voter_account",
          "type": "address"
        },
        {
          "name": "_voter_firstName",
          "type": "string"
        },
        {
          "name": "_voter_lastName",
          "type": "string"
        },
        {
          "name": "_voter_age",
          "type": "uint256"
        }
      ],
      "name": "register_voter_account",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "gas": 128869,
      "inputs": [
        {
          "name": "_candidate_name",
          "type": "string"
        }
      ],
      "name": "generate_canditate_list",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "gas": 7657,
      "inputs": [
        {
          "name": "_candidate_index",
          "type": "uint256"
        }
      ],
      "name": "get_candidate_name",
      "outputs": [
        {
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 96313,
      "inputs": [
        {
          "name": "_voter",
          "type": "address"
        },
        {
          "name": "_candidate_index",
          "type": "uint256"
        }
      ],
      "name": "vote_for_candidate",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "gas": 13047,
      "inputs": [
        {
          "name": "_voter",
          "type": "address"
        }
      ],
      "name": "get_vote_results",
      "outputs": [
        {
          "name": "",
          "type": "uint256[2]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 8034,
      "inputs": [
        {
          "name": "_voter",
          "type": "address"
        },
        {
          "name": "_index",
          "type": "uint256"
        }
      ],
      "name": "get_leading_candidate_name",
      "outputs": [
        {
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 2645,
      "inputs": [
        {
          "name": "_voter",
          "type": "address"
        },
        {
          "name": "_index",
          "type": "uint256"
        }
      ],
      "name": "get_result_sum",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 16628,
      "inputs": [
        {
          "name": "arg0",
          "type": "address"
        }
      ],
      "name": "voters",
      "outputs": [
        {
          "name": "voter_firstName",
          "type": "string"
        },
        {
          "name": "voter_lastName",
          "type": "string"
        },
        {
          "name": "voter_age",
          "type": "uint256"
        },
        {
          "name": "voting_status",
          "type": "bool"
        },
        {
          "name": "voted_candidate_index",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 8152,
      "inputs": [
        {
          "name": "arg0",
          "type": "uint256"
        }
      ],
      "name": "candidates",
      "outputs": [
        {
          "name": "candidate_name",
          "type": "string"
        },
        {
          "name": "candidate_voteCount",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1358,
      "inputs": [],
      "name": "voterCount",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1388,
      "inputs": [],
      "name": "contract_owner",
      "outputs": [
        {
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1418,
      "inputs": [],
      "name": "num_candidates",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1448,
      "inputs": [],
      "name": "num_voters",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]

'''


w3 = Web3(HTTPProvider('http://localhost:7545'))

contract_address = '0x0af609011749c8E1E65648119bD666D0Db5C89A8'            
votingsystem = w3.eth.contract(address=contract_address, abi=abi)


class IndexView(generic.TemplateView):
    template_name = 'voting/home.html'

    def get(self, *args, **kwargs):
        candidate_num = votingsystem.functions.num_candidates().call()
        
        candidate_names = []

        for candidate in range(0,candidate_num):
            publick = self.request.session['account_address']
            names = str(votingsystem.functions.get_candidate_name(candidate).call())
            candidate_votes= int(votingsystem.functions.get_result_sum(publick,candidate).call())

            candidate_names.append(tuple([names,candidate_votes]))

        context ={
            'candidates':candidate_names,
          
        }
        return render(self.request,self.template_name,context)


class setDefaultAccount(generic.TemplateView):
    template_name = 'voting/simpleLogin.html'
    
    def post(self, *args, **kwargs):
        clearSession(self.request)
        if self.request.is_ajax and self.request.method == "POST":
            public_key = w3.toChecksumAddress(self.request.POST.get("public_key", None))
            private_key = self.request.POST.get("private_key", None)

            if (len(public_key)) and (len(private_key)):
                self.request.session['account_address'] = public_key
                self.request.session['account_private_key'] = private_key
                w3.eth.default_account = public_key
                messages.info(self.request, "Login completed!")
                return redirect('voting:voteCandidate')
            else:
                messages.warning(self.request, "Login failed, please try again")
                return JsonResponse({}, status = 400)


class voteCandidate(generic.View):
    template_name = 'voting/vote.html'

    def get(self, *args, **kwargs):
        candidate_num = votingsystem.functions.num_candidates().call()
        candidate_names = []

        for candidate in range(0,candidate_num):
            candidate_names.append(votingsystem.functions.get_candidate_name(candidate).call())

        context ={
            'candidates':candidate_names
        }
        return render(self.request,self.template_name,context)

    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":

            voted_option = int(self.request.POST.get("candidate", None))
          
            publicK = str(self.request.session['account_address'])
            transaction = votingsystem.functions.vote_for_candidate(publicK,voted_option).buildTransaction({
                    'gas': 100000,
                    'gasPrice': w3.toWei('1', 'gwei'),
                    'nonce': w3.eth.getTransactionCount(publicK)
             })

            pk = self.request.session['account_private_key']
            run_transaction(transaction,pk)  
            return JsonResponse({"status":True}, status = 200)
        return JsonResponse({}, status = 400)


def run_transaction(tx, pk):
    signed_tx = w3.eth.account.signTransaction(tx,pk)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    count = 1
    while tx_receipt is None and (count < 30):
        sleep(10)
        result = tx_receipt
        tx_receipt = w3.eth.getTransactionReceipt(result)
        count = count + 1
    print(tx_receipt)
    return tx_receipt

def clearSession(request):
    try:
        del request.session['account_address']
        del request.session['account_private_key']
    except KeyError:
        pass
    messages.info(request, "Sign out completed")
    return redirect('voting:login')
