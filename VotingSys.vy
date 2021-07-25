struct Voter:
    voter_firstName: bytes32
    voter_lastName: bytes32
    voter_age:uint256
    voting_status: bool

    voted_candidate_index: uint256

struct Candidate:
    candidate_name: bytes32
    candidate_voteCount: uint256

voters: public(HashMap[address, Voter])
voter_accounts:address[1000]

candidates: public(HashMap[uint256, Candidate])
voterCount: public(uint256)
contract_owner: public(address)
num_candidates: public(uint256)
num_voters: public(uint256)

event CreateVoterAccount:
    _from:indexed(address)
    _timestamp:uint256


event VotedForCandidate:
    _from:indexed(address)
    _candidate_index:uint256
    _timestamp:uint256

@external
def __init__():
    self.contract_owner = msg.sender
    self.voterCount = 0
    self.num_candidates = 0
    self.num_voters = 0


@view
@internal
def exists_account(_address:address) -> bool:
    for a in self.voter_accounts:
        if a == _address:
            return True
    return False

@external
def register_voter_account(_voter_account:address, _voter_firstName:bytes32, _voter_lastName:bytes32,_voter_age:uint256):
    assert msg.sender == self.contract_owner
    assert not self.exists_account(_voter_account)
    self.voters[_voter_account] = Voter({
                                        voter_firstName: _voter_firstName,
                                        voter_lastName: _voter_lastName,
                                        voter_age:_voter_age,
                                        voting_status: True,
                                        voted_candidate_index: 0
                                        })
    self.voter_accounts[self.num_voters] = _voter_account
    self.num_voters += 1
    log CreateVoterAccount(_voter_account,block.timestamp)


@external
def generate_canditate_list(_candidate_name: bytes32[5]):
    assert msg.sender == self.contract_owner
    for i in range(1,6):
        self.candidates[i] = Candidate({
                                    candidate_name: _candidate_name[i],
                                    candidate_voteCount: 0
                                    })
        self.num_candidates +=1
    
@view
@external
def get_candidate_name(_candidate_index: uint256) ->bytes32:
    assert self.num_candidates > _candidate_index
    return self.candidates[_candidate_index].candidate_name


@external
def vote_for_candidate(_voter:address, _candidate_index: uint256):
    assert self.voters[_voter].voting_status != True
    assert self.num_candidates > _candidate_index

    self.voters[msg.sender].voted_candidate_index = _candidate_index
    self.voters[msg.sender].voting_status = True
    self.candidates[_candidate_index].candidate_voteCount +=1
    log VotedForCandidate(_voter,_candidate_index,block.timestamp)

@view
@internal
def get_results() -> uint256:
    leading_vote_count: uint256 = 0
    leading_candidate_index:uint256 = 0

    for x in range(1,6):
        if self.candidates[x].candidate_voteCount > leading_vote_count:
            leading_vote_count = self.candidates[x].candidate_voteCount
            leading_candidate_index = x
    return leading_candidate_index

@view
@external
def get_vote_results(_voter:address) -> uint256:
    assert self.voters[_voter].voting_status 
    return self.get_results()

@view
@external
def get_leading_candidate_name(_voter:address) -> bytes32:
    assert self.voters[_voter].voting_status 
    return self.candidates[self.get_results()].candidate_name

