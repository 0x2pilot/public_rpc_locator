
class Validator:

    def __init__(self, pub_key, moniker, identity, security_contact):
        self.pub_key = pub_key
        self.moniker = moniker
        self.identity = identity
        self.security_contact = security_contact

    @property
    def get_pub_key(self):
        return self.pub_key

    @property
    def get_moniker(self):
        return self.moniker

    @property
    def get_identity(self):
        return self.identity

    @property
    def get_security_contact(self):
        return self.security_contact