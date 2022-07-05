#!/usr/bin/env python3
import socket
import os 
import time

class jogador():
    def __init__(self, nome, conn, ip):
        self.nome = nome
        self.conn = conn
        self.ip = ip
        self.pontos = 0
        self.palavra = ''

def limpar():
	os.system('cls' if os.name == 'nt' else 'clear')

#TRATAMENTO DO SOCKET
HOST = '0.0.0.0'     # Endereco IP do Servidor
PORT = 40000           # Porta que o Servidor escuta

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.bind(serv)
sock.listen(50)

num_jogadores = int(input("Quantidade de jogadores: "))

lista_jogadores = []
lista_vencedores = []

def checarpontos(i):
    if(lista_jogadores[i].pontos <= 0):
        lista_jogadores.pop(i)

#ESPERANDO OS JOGADORES ENTRAREM NO JOGO
for i in range(num_jogadores):
    conn, ip = sock.accept()
    nome = conn.recv(1024)
    lista_jogadores.append(jogador(nome, conn, ip))
    print(lista_jogadores[i].nome.decode() + " se conectou.")

palavra = input("Escolha a palavra: ").lower()

#SETANDO AS CONFIGURAÇÕES DE CADA JOGADOR
branco = ''
for i in range(len(palavra)):
    branco+='_'

for i in range(num_jogadores):
    lista_jogadores[i].palavra = branco
    lista_jogadores[i].pontos = 6;
    
   
for j in range(num_jogadores):
    time.sleep(0.001)
    lista_jogadores[j].conn.send(branco.encode())  # MANDANDO O BRANCO

fim = 1
limpar()

while(fim):
    for i in range(num_jogadores):
        placar ="Placar: \n"
        for jog in range(num_jogadores): #MONTANDO O PLACAR
            placar+= lista_jogadores[jog].nome.decode() + '\t' + str(lista_jogadores[jog].pontos) + '\n'

        print(placar)

        for j in range(num_jogadores):
            time.sleep(0.001)
            lista_jogadores[j].conn.send(placar.encode()) #MANDANDO O PLACAR PARA TODOS OS JOGADORES
            nada = lista_jogadores[j].conn.recv(1024)
            if(j != i):
                time.sleep(0.001)
                lista_jogadores[j].conn.send(lista_jogadores[i].nome.decode() + " está jogando.") #MANDANDO PARA OS JOGADORES QUEM ESTÁ JOGANDO

        print(lista_jogadores[i].nome.decode() + " está jogando.")

        time.sleep(0.001)
        lista_jogadores[i].conn.send("É a sua vez de jogar: ".encode()) #MANDANDO PARA O JOGADOR QUE É SUA VEZ DE JOGAR
        ret = lista_jogadores[i].conn.recv(1024)
        if(len(ret) == 1):
            perdepontos = 1
            novapalavra = ''
            for c in range(len(palavra)):
                if(palavra[c] == ret):
                    perdepontos = 0
                    novapalavra += ret
                else:
                    novapalavra += lista_jogadores[i].palavra[c]


            lista_jogadores[i].palavra = novapalavra
            lista_jogadores[i].pontos -= perdepontos
            time.sleep(0.001)
            lista_jogadores[i].conn.send(lista_jogadores[i].palavra.encode())
            checarpontos(i)
        else:
            perdepontos = 2
            if(palavra == ret):
                fim = 0
                lista_jogadores[i].palavra = palavra
                lista_vencedores.append(lista_jogadores[i])
                perdepontos = 0
            lista_jogadores[i].pontos -= perdepontos
            time.sleep(0.001)
            lista_jogadores[i].conn.send(lista_jogadores[i].palavra.encode())
            checarpontos(i)

        for j in range(num_jogadores):
            if(j != i):
                time.sleep(0.001)
                lista_jogadores[j].conn.send("Fim de turno") #MANDANDO PARA OS JOGADORES QUE ESTAVAM ESPERANDO QUE O TURNO ACABOU

#Determinar um o vencedor
maior = max(i.pontos for i in lista_vencedores)
vencedor = ''

for i in range(len(lista_vencedores)):
    if(lista_vencedores[i].pontos == maior):
        vencedor += '|' + lista_vencedores[i].nome.decode()


#Mandando o sinal que o jogo acabou
for i in range(num_jogadores):
    lista_jogadores[i].conn.send("fim de jogo"+vencedor.encode())

sock.close()

