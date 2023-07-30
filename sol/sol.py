import socket

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s1.connect(("127.0.0.1",8877))
s2.connect(("127.0.0.1",8888))

for i in range(0,1000):
    m1 = s1.recv(4000)
    print("BOB: ", m1)
    s2.send(m1)
    m2 = s2.recv(4000)
    print("ALICE: ", m2)
    s1.send(m2)