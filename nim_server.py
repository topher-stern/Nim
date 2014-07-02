# Christopher Stern
# Purpose: To design a game of Nim that can be played over a network
# Completed On: June 1, 2011

import socket
import random
def checkStones(numLeft,client):
    if numLeft == 0 and client == "1":
        return "Player 2 Wins"
    elif numLeft == 0 and client == "2":
        return "Player 1 Wins"
    else:
        return("Continue")
    
print "Game of Nim Server"
print
IP = socket.gethostbyname(socket.gethostname())
print "The IP address of the Nim Server is: " + IP
PORT = 23456
ADS = (IP, PORT)
from socket import *
tcpsoc = socket(AF_INET, SOCK_STREAM)
tcpsoc.bind(ADS)
tcpsoc.listen(5)

print "Waiting for connection from Player 1"
tcpclient1, addr = tcpsoc.accept()
print "connected from:", addr
tcpclient1.send("You're connected as Player 1. Wait for Player2 to connect.")
print "Waiting for connection from Player 2"
tcpclient2, addr = tcpsoc.accept()
print "connected from:", addr
tcpclient2.send("You're connected as Player 2. Wait for Player 1 to make a move.")

stones = random.randint(15,30)
tcpclient1.send("Player 1 - Please make your move.")
tcpclient1.send(str(stones))
gameover = False
while gameover == False:
    stones = int(tcpclient1.recv(1024))
    print "From Player 1: " + str(stones)
    result1 = checkStones(stones,"1")
    print result1
    if result1 == "Continue":
        tcpclient2.send("Player 2 - Please make your move.")
        if stones > 0:
            tcpclient2.send(str(stones))
        stones = int(tcpclient2.recv(1024))
        print "From Player 2: " + str(stones)
        result2 = checkStones(stones,"2")
        print result2
        if result2 == "Continue":
            tcpclient1.send("Player 1 - Please make your move.")
            if stones > 0:
                tcpclient1.send(str(stones))
        else:
            gameover = True
            if result2 == "Player 1 Wins":
                tcpclient1.send("Congratulations! You Won the Game of Nim!")
                tcpclient1.send(str(stones))
                tcpclient2.send("You were forced to take the last stone. Sorry. You Lose.")
            if result2 == "Player 2 Wins":
                tcpclient1.send("You were forced to take the last stone. Sorry. You Lose.")            
                tcpclient2.send("Congratulations! You Won the Game of Nim!")
                tcpclient2.send(str(stones))
    else:
        gameover = True
        if result1 == "Player 1 Wins":
            tcpclient1.send("Congratulations! You Won the Game of Nim!")
            tcpclient1.send(str(stones))
            tcpclient2.send("You were forced to take the last stone. Sorry. You Lose.")
        if result1 == "Player 2 Wins":
            tcpclient1.send("You were forced to take the last stone. Sorry. You Lose.")            
            tcpclient2.send("Congratulations! You Won the Game of Nim!")
            tcpclient2.send(str(stones))
print "Game Over."
tcpclient1.close()
tcpclient2.close()
tcpsoc.close()

