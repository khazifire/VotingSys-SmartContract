import pytest, brownie

@pytest.fixture(scope="module",autouse=True)
def Vote(vote,accounts):
    Vote_contract = vote.deploy({'from':accounts[0]})
    yield Vote_contract

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def register_voter_account(Vote, accounts, _voter_account, _voter_firstName, _voter_lastName, _voter_age,index=0):
    Vote.register_voter_account(
        _voter_account,
        _voter_firstName,
        _voter_lastName,
        _voter_age,
        {'from':accounts[index]}
    )
    # assert not Vote.exists_account(_voter_account)

def generate_canditate_list(Vote, accounts, _vote_candidate_name,index=0):
    Vote.generate_canditate_list(
        _vote_candidate_name,
        {'from':accounts[index]}
    )

def get_candidate_name(Vote,accounts,_candidate_index,index=0):
    Vote.get_candidate_name(
        _candidate_index,
        {'from':accounts[index]}
    )


def vote_for_candidate(Vote,accounts, _voter,_candidate_index, index=1):
    Vote.vote_for_candidate(
        _voter,
        _candidate_index,

        {'from':accounts[index]}
    )

def get_vote_results(Vote,accounts, _voter, index=1):
    Vote.get_vote_results(
        _voter,
        {'from':accounts[index]}
    )


def test_contract_owner_interaction(Vote,accounts):
    register_voter_account(
        Vote,
        accounts,
        '0x6867d29206F68C5318d9143cb72671a63397222D',
        'Dan',
        'khazifire',
        18     
    )

    generate_canditate_list(
        Vote,
        accounts,
        'Tarun'
    )

    get_candidate_name(
        Vote,
        accounts,
        0
    )


def test_citizen_interaction(Vote,accounts):
    register_voter_account(
        Vote,
        accounts,
        '0x48Dba1a7880a246708fd278dBFcF3e4B3F4eCE71',
        'Dan',
        'khazifire',
        18     
    )
    generate_canditate_list(
        Vote,
        accounts,
        'Tarun'
    )
    get_candidate_name(
        Vote,
        accounts,
        0
    )
    vote_for_candidate(
        Vote,
        accounts,
        '0x48Dba1a7880a246708fd278dBFcF3e4B3F4eCE71',
        0
    )
    get_vote_results(
        Vote,
        accounts,
        '0x48Dba1a7880a246708fd278dBFcF3e4B3F4eCE71'
    )

