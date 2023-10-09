class NodeInfo:

    def __init__(self, ip, rpc_port, pub_key):
        self._ip = ip
        self._rpc_port = rpc_port
        self._pub_key = pub_key

    @property
    def ip(self):
        return self._ip

    @property
    def rpc_port(self):
        return self._rpc_port

    @property
    def rpc_endpoint(self):
        return f"http://{self.ip}:{self._rpc_port}"

    @property
    def pub_key(self):
        return self._pub_key

    def __eq__(self, other):
        if not isinstance(other, NodeInfo):
            return False
        return (self.ip == other.ip and
                self.rpc_port == other.rpc_port and
                self.pub_key == other.pub_key)

    def __hash__(self):
        return hash((self.ip, self.rpc_port, self.pub_key))
