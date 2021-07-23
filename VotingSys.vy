#citizen_Details
struct VoterAccount:
    citizen_id: uint256
    #citizen_firstNname: Bytes[32]
    #citizen_lastName: Bytes[32]
    citizen_firstNname: String[25]
    citizen_lastName: String[25]
    citizen_age: uint256
    citizen_voting_status: bool 

struct Candidates:
    candidate_id: uint256
    candidate_name: String[50]
    candidate_voteCount: uint256



# citizen Accounts:
accounts_details: HashMap[address, VoterAccount]
accounts: address[1000]

nominee_details: HashMap[uint256, Candidates]
candidate: uint256[10]

#to auto increment thier position in the arrays
citizen_index: uint256
nominee_index: uint256

contract_owner: public(address)
time_limit: public(uint256)   #number of days


event CreateCitizenAccount:
    _from: indexed(address)
    _timestamp:uint256


event AddCandidates:
    _from: uint256
    _timestamp:uint256

@external
def __init__():
    self.contract_owner = msg.sender
    self.time_limit = 1 #in days

@view
@internal
def exists_account(_address:address) -> bool:
    for a in self.accounts:
        if a == _address:
            return True
    return False

@external
def register_Citizen_account(_citizen_id: uint256,_citizen_firstNname: String[25],_citizen_lastName: String[25],_citizen_age: uint256, _citizen_address:address):
    assert self.citizen_index < 1000
    assert msg.sender == self.contract_owner
    assert self.exists_account(_citizen_address) != True
    self.accounts_details[_citizen_address] = VoterAccount({
                                                        citizen_id: _citizen_id,
                                                        citizen_firstNname: _citizen_firstNname,
                                                        citizen_lastName: _citizen_lastName,
                                                        citizen_age: _citizen_age,
                                                        citizen_voting_status: True
                                                        })
    self.accounts[self.citizen_index] = _citizen_address
    self.citizen_index += 1
    log CreateCitizenAccount(_citizen_address,block.timestamp)

@external
def generate_canditate_list(_candidate_id:uint256,_candidate_name: String[50]):
    assert self.nominee_index < 10
    assert msg.sender == self.contract_owner
    self.nominee_details[_candidate_id] = Candidates({
                                                        candidate_id: _candidate_id,
                                                        candidate_name: _candidate_name,
                                                        candidate_voteCount: 0
                                                        })
    self.candidate[self.nominee_index] = _candidate_id
    self.nominee_index += 1
    log AddCandidates(_candidate_id,block.timestamp)

@view
@external
def get_citizen_list() -> address[1000]:
    assert msg.sender == self.contract_owner
    return self.accounts

@view
@external
def get_canidate_list() -> uint256[10]:
    assert msg.sender == self.contract_owner
    return self.candidate

# def get_vote_count() uint256:
#     candidate_index: uint256: 0
#     candidate_vote_count: uint256: 0



# def viewResult() -> bytes32:
#     return self.nominee_details[self.get_vote_count()].name

