import requests
from prettytable import PrettyTable
import sys
import node_locator
from validator_info import Validator


def create_validators_map():
    pub_key_to_validator = {}
    validators_endpoint = "cosmos/staking/v1beta1/validators?pagination.limit=1000&status=BOND_STATUS_BONDED"
    validators_response = requests.get(f"{api_endpoint}/{validators_endpoint}", timeout=5)
    for validator_response in validators_response.json()["validators"]:
        pub_key = validator_response["consensus_pubkey"]["key"]
        moniker = validator_response["description"]["moniker"]
        identity = validator_response["description"]["identity"]
        security_contact = validator_response["description"]["security_contact"]
        pub_key_to_validator[pub_key] = Validator(pub_key, moniker, identity, security_contact)
    return pub_key_to_validator


if __name__ == '__main__':
    if len(sys.argv) == 3:
        rpc_endpoint = sys.argv[1]
        api_endpoint = sys.argv[2]
    else:
        rpc_endpoint = input("enter rpc endpoint\n")
        api_endpoint = input("enter api endpoint\n")

    pub_key_to_validator = create_validators_map()
    rpc_nodes = node_locator.get_public_rpc_nodes(rpc_endpoint)
    print(f'total public rpc nodes found {len(rpc_nodes)}\n')

    table = PrettyTable()
    table.field_names = ["Rpc endpoint", "Is validator", "Validator moniker", "Identity", "Security Contact"]
    for rpc_node in rpc_nodes:
        rpc_endpoint = rpc_node.rpc_endpoint
        pub_key = rpc_node.pub_key
        is_validator = False
        validator_moniker = ""
        identity = ""
        security_contact = ""
        if pub_key in pub_key_to_validator:
            is_validator = True
            validator_moniker = pub_key_to_validator[pub_key].moniker
            identity = pub_key_to_validator[pub_key].identity
            security_contact = pub_key_to_validator[pub_key].security_contact
        table.add_row([rpc_endpoint, is_validator, validator_moniker, identity, security_contact])

    print(table)
