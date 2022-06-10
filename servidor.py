#!/usr/bin/env/python3
import socket
import os

HOST = ''              # Endereco IP do Servidor
PORT = 40000          # Porta que o Servidor esta

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
tcp.bind(serv)
tcp.listen(50)
while True:
    try:
        con, cliente = tcp.accept()
    except: break
    pid = os.fork()
    if pid == 0:
        tcp.close()
        print ('Conectado por', cliente)
        while True:
            msg = con.recv(1024)
            if not msg: break
            print ('Recebido: ', msg.decode())
            con.send(msg)
        print ('Finalizando conexao do cliente', cliente)
        con.close()
        break
    else:
      con.close()
tcp.close()