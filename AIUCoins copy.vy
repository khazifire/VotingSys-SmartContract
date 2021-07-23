# Record details:
struct Account:
    student_balance: uint256
    studentid: uint256

# Accounts storage:
#MAX_ACCOUNT: constant(uint256) = 1000
accounts_details: HashMap[address, Account]
accounts: address[1000]
index: uint256

contract_owner: public(address)
contract_trader: address
conversion_rate_wei_auc: decimal # Rate to transform 1 ETH to auc.
# R = 15000000000000 Wei/auc
# 1 auc -> R Wei
# From auc to Wei: x auc * R 
# From Wei to auc: x Wei / R

event CreateAUCAccount:
    _from:indexed(address)
    _timestamp:uint256

event WithdrawAUCs:
    _withdrawer:indexed(address)
    _total_amount:uint256
    _timestamp:uint256

event DepositAUCs:
    _from:indexed(address)
    _to:indexed(address)
    _value:uint256
    _timestamp:uint256
    _conversion_rate_wei_auc:decimal

@external
#def __init__(_conversion_rate:decimal):
def __init__():
    self.contract_owner = msg.sender
    self.contract_trader = msg.sender
    self.conversion_rate_wei_auc = 15000000000000.0 # in wei.

@view
@internal
def exists_account(_address:address) -> bool:
    for a in self.accounts:
        if a == _address:
            return True
    return False

@view
@internal
def from_wei_to_auc(amount:uint256) -> uint256:
    return convert(convert(amount,decimal) / self.conversion_rate_wei_auc,uint256)

@view
@internal
def from_auc_to_wei(amount:uint256) -> uint256:
    return convert(convert(amount,decimal) * self.conversion_rate_wei_auc,uint256)

@external
def register_account(_studentid:uint256,_student_address:address):
    assert self.index < 1000
    assert msg.sender == self.contract_owner
    self.accounts_details[_student_address] = Account({
                                         student_balance: 0,
                                         studentid: _studentid
                                       })
    self.accounts[self.index] = _student_address
    self.index += 1
    log CreateAUCAccount(_student_address,block.timestamp)

@payable
@external
def deposit_aucs(_recipient:address):
    assert self.exists_account(_recipient)
    self.accounts_details[_recipient].student_balance += self.from_wei_to_auc(msg.value)
    log DepositAUCs(msg.sender,_recipient, msg.value, block.timestamp, self.conversion_rate_wei_auc)

@external
def withdraw_aucs(_amount_auc:uint256):
    assert self.exists_account(msg.sender), "The address account doesn't exist!"
    _amount_wei:uint256 = self.from_auc_to_wei(_amount_auc)
    assert _amount_wei <= self.balance
    assert _amount_auc <= self.accounts_details[msg.sender].student_balance
    self.accounts_details[msg.sender].student_balance -= _amount_auc
    log WithdrawAUCs(msg.sender,_amount_wei,block.timestamp)
    send(msg.sender, _amount_wei)

@external
def deduct_aucs(_student_address:address, _amount_auc:uint256):
    assert msg.sender == self.contract_owner or msg.sender == self.contract_trader
    assert self.exists_account(_student_address)
    _amount_wei:uint256 = self.from_auc_to_wei(_amount_auc)
    assert _amount_wei <= self.balance
    assert _amount_auc <= self.accounts_details[_student_address].student_balance
    self.accounts_details[_student_address].student_balance -= _amount_auc
    log WithdrawAUCs(_student_address,_amount_wei,block.timestamp)
    send(msg.sender, _amount_wei)

@view
@external
def get_account_student_id(_student_address: address) -> uint256:
    assert msg.sender == self.contract_owner
    return self.accounts_details[_student_address].studentid

@view
@external
def get_student_account_balance(_student_address: address) -> uint256:
    assert msg.sender == self.contract_owner or msg.sender == self.contract_trader
    assert self.exists_account(_student_address)
    return self.accounts_details[_student_address].student_balance

@view
@external
def get_account_balance() -> uint256:
    assert self.exists_account(msg.sender)
    return self.accounts_details[msg.sender].student_balance

@view
@external
def get_accounts_list() -> address[1000]:
    assert msg.sender == self.contract_owner
    return self.accounts

@view
@external
def get_total_weis() -> uint256:
    assert msg.sender == self.contract_owner or msg.sender == self.contract_trader
    return self.balance

@view
@external
def get_total_aucs() -> uint256:
    assert msg.sender == self.contract_owner or msg.sender == self.contract_trader
    return self.from_wei_to_auc(self.balance)

@external
def change_conversion_rate_wei_auc(_conversion_rate_wei_auc:decimal):
    assert msg.sender == self.contract_owner
    self.conversion_rate_wei_auc = _conversion_rate_wei_auc

@external
def change_contract_trader(_contract_trader:address):
    assert msg.sender == self.contract_owner
    self.contract_trader = _contract_trader

@view
@external
def convert_weis_to_aucs(_amount:uint256) -> uint256:
    return self.from_wei_to_auc(_amount)

@view
@external
def convert_aucs_to_weis(_amount:uint256) -> uint256:
    return self.from_auc_to_wei(_amount)