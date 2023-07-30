#!/usr/bin/env python
"""
Free-Proxy Alice Client v1.0
To be executed and handled with socat
"""
import os
import rsa
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class Alice():
    def __init__(self):
        self.priv_key_path = "./alice_priv"
        self.pub_key_path = "./alice_pub"
        self.pub_key = None
        self.priv_key = None
        self.bob_pub = None
        self.shared_key = None

    def run(self):
        self.load_keys()
        self.hand_shake()
        self.msg_loop()

    def recv(self)->str:
        return sys.stdin.buffer.read()
    
    def send(self, msg:str):
        sys.stdout.buffer.write(msg)

    def load_keys(self):
        if not os.path.exists(self.priv_key_path):
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
        # Receive Bob's Public Key
        self.bob_pub = rsa.PublicKey.load_pkcs1(self.recv())
        # Send Public Key to Bob
        self.send(self.pub_key.save_pkcs1())
    
        # Receive Symmetric Encryption Key
        self.shared_key = self.recv(rsa.decrypt(self.shared_key, self.priv_key))
    
    def msg_loop(self):
        msg = open("freedom.txt", 'r').readlines()
        for i in range(0, len(msg)):
            if (i % 2) != 0:
                self.send(self.encrypt(msg[i]))
            elif self.decrypt(self.recv()) != msg[i]:
                exit()

    def encrypt(self, data:str):
        iv = os.urandom(AES.block_size)
        self.cipher = AES.new(self.shared_key, AES.MODE_CBC, iv)
        return iv + self.cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

    def decrypt(self, data:bytes):
        self.cipher = AES.new(self.shared_key, AES.MODE_CBC, data[:AES.block_size])
        return unpad(self.cipher.decrypt(data[AES.block_size:]), AES.block_size)

if __name__ == "__main__":
    bob = Alice()
    bob.msg_loop()