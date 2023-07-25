"""
Free-Proxy Client v1.0

"""
import os
import Crypto
import rsa
import sys


class Bob():
    priv_key_path = "./bob_priv"
    pub_key_path = "./bob_pub"
    pub_key = None
    priv_key = None

    def bob_init(self):
        self.load_keys()
        self.hand_shake()

    def load_keys(self):
        if not os.path.exists("./bob_priv"):
            self.gen_keys()
        with open(self.priv_key_path, 'rb') as p:
            self.priv_key = rsa.PrivateKey.load_pkcs1(p.read())
        with open(self.pub_key_path, 'rb') as p:
            self.pub_key = rsa.PublicKey.load_pkcs1(p.read())
    
    def gen_keys(self):
        (pub,priv) = rsa.newkeys(1024)
        with open(self.priv_key_path, 'wb') as p:
            p.write(priv.save_pkcs1())
        with open(self.pub_key_path, 'wb') as p:
            p.write(pub.save_pkcs1())


    def hand_shake(self):
        self.send(self.pub_key.save_pkcs1())
        alice_key = rsa.PublicKey.load_pkcs1(self.recv())
        print(alice_key.save_pkcs1().decode('utf8'))
    def recv(self)->str:
        return sys.stdin.buffer.read()
    def send(self, msg:str):
        sys.stdout.buffer.write(msg)
if __name__ == "__main__":
    bob = Bob()
    bob.bob_init()