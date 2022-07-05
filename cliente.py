#!/usr/bin/env python3
import socket
import sys
import os
import time

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 40000           # Porta que o Servidor esta

def flush_input():
	try:
		import sys, termios
		termios.tcflush(sys.stdin, termios.TCIOFLUSH)
	except ImportError:
		import msvcrt
		while msvcrt.kbhit():
			msvcrt.getch()

def limpar():
	os.system('cls' if os.name == 'nt' else 'clear')
 
def comando_usuario(cmd_usr):
  cmd_map = {
    'sair': 'quit',
    'jogar': 'play',
    'chutar' : 'kick',
  }
  
  tokens = cmd_usr.split()
  if tokens[0].lower() in cmd_map:
    tokens[0] = cmd_map[tokens[0].lower()]
    return " ".join(tokens)
  else:
    return False    
    
if len(sys.argv) > 1:
  HOST = sys.argv[1]
  
print('Servidor: ', (HOST, PORT))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.connect(serv)

nome = input("Nome: ")
time.sleep(0.001)
sock.send(nome.encode())

print('#############################################################')
print('\t\t\tJOGO DA FORCA')
print('#############################################################')
print('Para começar o jogo digite "play"')
print('Para encerrar o jogo digite "quit"')

minhapalavra = sock.recv(1024)

fim = 1;
while(fim):
  limpar()
  placar = sock.recv(1024)
  if(placar.startswith("fim de jogo".encode())):
    break


  print('\n'+placar.decode())
  time.sleep(0.001)
  sock.send('nada'.encode())

  print("Sua palavra: \n")
  for c in minhapalavra:  # printa sua a palavra
    print("{}".format(c) + ' '),

  print ('\n')

  ret = sock.recv(1024)
  if(ret.decode() == "É a sua vez de jogar: "):
    time.sleep(0.001)
    flush_input()
    sock.send(input("\nEscolha uma letra ou chute a palavra: ".encode())).lower()
    minhapalavra = sock.recv(1024)

  else:
    print("\n"+ret.decode())
		
    fimdeturno = sock.recv(1024)

vencedores = []
vencedores = placar.split('|')

if(len(vencedores)== 2):
	print("O jogo acabou, o vencedor foi "+vencedores[1]+".")
elif(len(vencedores) > 2):
	print("O jogo acabou empatado, os vencedores foram:")
	for i in range(1, len(vencedores)):
		print (vencedores[i])


sock.close()