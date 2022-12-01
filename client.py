import socket
import pickle

HEADER_SIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

a = {
    1: 'a',
    2: 'b',
    3: 'c'
}

s.send(pickle.dumps(a))

# while True:
#     full_msg = b''
#     new_msg = True
#     while True:
#         msg = s.recv(16)
#         if new_msg:
#             print("new msg len:", msg[:HEADER_SIZE])
#             msg_len = int(msg[:HEADER_SIZE])
#             new_msg = False
#
#         print(f"full message length: {msg_len}")
#
#         full_msg += msg
#
#         print(len(full_msg))
#
#         if len(full_msg)-HEADER_SIZE == msg_len:
#             print("full msg recvd")
#             print(full_msg[HEADER_SIZE:])
#             print(pickle.loads(full_msg[HEADER_SIZE:]))
#             new_msg = True
#             full_msg = b""