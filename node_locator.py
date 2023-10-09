import requests

from node_info import NodeInfo

DEFAULT_DEPTH = 2
TIMEOUT_SECONDS = 2


def get_public_rpc_nodes(rpc_endpoint, depth=DEFAULT_DEPTH):
    if depth == 0:
        return set()
    net_info_response = __get(rpc_endpoint, "net_info")
    if net_info_response is None:
        return set()

    peers = net_info_response.json()['result']['peers']
    result = set()
    for peer in peers:
        ip = peer['remote_ip']
        rpc = peer['node_info']['other']['rpc_address']
        rpc = str(rpc).replace("tcp", "http").replace("0.0.0.0", ip)
        status_response = __get(rpc, "status")
        if status_response:
            pub_key = status_response.json()["result"]["validator_info"]["pub_key"]["value"]
            rpc_port = rpc.split(":")[-1]
            result.add(NodeInfo(ip, rpc_port, pub_key))

    for node_info in result:
        result = result.union(get_public_rpc_nodes(node_info.rpc_endpoint, depth - 1))
    return result


def __get(rpc_endpoint, path):
    try:
        response = requests.get(f"{rpc_endpoint}/{path}", timeout=TIMEOUT_SECONDS)
        return response if response.status_code == 200 else None
    except:
        return None
