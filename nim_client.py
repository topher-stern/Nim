# Christopher Stern
# Purpose: To design a game of Nim that can be played over a network
# Completed On: June 1, 2011
import socket
def checkMove(m,s): # ensure valid numbe of stones are taken
    moveOn = False
    if 0 < m < 4 and m <= s: # check to see if the move is valid
        moveOn = True
    while moveOn == False: # while it is not valid ask for new input
        if m > 3 or m < 1:
            print "That is an invalid move."
            m = int(raw_input("Choose the number of stones you would like to take (1-3)>>"))
        if m >= s:
            print "That is an invalid move."
            m = int(raw_input("Choose the number of stones you would like to take (1-3)>>"))
        if m <= s and (0 < m < 4):
            moveOn = True
    return m # return the new value of the move
from socket import *
print "Game of Nim Client"
print "------------------"
print
print "In this game there are a random number of stones generated."
print "Players will take turns taking between 1 and 3 stones each turn."
print "The object of the game is to not be the player who takes"
print "the last stone from the pile."
IP = raw_input("Enter the IP address of the Game of Nim Server: ")
PORT = 23456
ADS = (IP, PORT)
tcpsocket = socket(AF_INET, SOCK_STREAM)
tcpsocket.connect(ADS) # connect ot server

data = tcpsocket.recv(1024) # receive player number
print data
print
data = tcpsocket.recv(1024) # told whether to go or wait
print data
stones = int(tcpsocket.recv(1024)) # receive number of stones left
while stones > 0:
    if stones > 1:
        print "There are " + str(stones) + " stones left."
    else:
        print "There is 1 stone left."
    move = int(raw_input("Choose the number of stones you would like to take (1-3)>>"))
    m = checkMove(move,stones)
    stones = stones - m
    tcpsocket.send(str(stones))
    print "Waiting for response ....."
    data = tcpsocket.recv(1024)
    print
    if data[0]=="P":
        print data
        stones = int(tcpsocket.recv(1024))
    else:
        print
        print data
        stones = int(tcpsocket.recv(1024))
print
print "Thank you for playing Nim."
raw_input("Press Enter to End Game.")
tcpsoc.close()

