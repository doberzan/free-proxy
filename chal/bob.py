#!/usr/bin/env python
"""
Free-Proxy Bob Client v1.0
To be executed and handled with socat
"""
import os
import rsa
import sys
from hashlib import md5
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class Bob():
    def __init__(self):
        self.priv_key_path = "./bob_priv"
        self.pub_key_path = "./bob_pub"
        self.pub_key = None
        self.priv_key = None
        self.alice_pub = None
        self.shared_key = None

    def run(self):
        self.load_keys()
        self.hand_shake()
        self.msg_loop()

    def recv(self)->str:
        return b64decode(input())
    
    def send(self, msg:bytes):
        sys.stdout.buffer.write(b64encode(msg))
        sys.stdout.buffer.flush()

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
        try:
            # Send Public Key to Alice
            self.send(self.pub_key.save_pkcs1())
            # Receive Public Key from Alice
            self.alice_pub = rsa.PublicKey.load_pkcs1(self.recv())
        
            # Propose Symmetric Encryption Key
            self.shared_key = md5(os.urandom(16)).digest()
            self.send(rsa.encrypt(self.shared_key, self.alice_pub))
        except Exception as e:
            print(e)
    
    def msg_loop(self):
        msg = open("freedom.txt", 'r').readlines()
        for i in range(0, len(msg)):
            if (i % 2) == 0:
                self.send(self.encrypt(msg[i]))
            elif self.decrypt(self.recv()) != msg[i]:
                exit()

    def encrypt(self, data:str):
        iv = os.urandom(AES.block_size)
        cipher = AES.new(self.shared_key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

    def decrypt(self, data:bytes):
        cipher = AES.new(self.shared_key, AES.MODE_CBC, data[:AES.block_size])
        return unpad(cipher.decrypt(data[AES.block_size:]), AES.block_size)

if __name__ == "__main__":
    bob = Bob()
    bob.run()