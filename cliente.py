#!/usr/bin/env/python3
import socket
import sys

HOST = 'localhost'     # Endereco IP do Servidor
PORT = 40000          # Porta que o Servidor esta

if len(sys.argv) > 1:
    HOST = sys.argv[1]

print('Servidor: ', (HOST, PORT))
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
print( '''
  JOGO DA FORCA
    +------+
    |      |
    |      O
    |     /|\\
    |     / \\
       
===========================

''')
print ('Para sair do jogo use CTRL+C')
while True:
    try:
        msg = input('Mensagem: ')
    except: break
    tcp.send(str.encode(msg))
    msg = tcp.recv(1024)
    if not msg: break
    print ('Recebido: ', msg.decode())

tcp.close()
