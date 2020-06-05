import socket
import os
from threading import Thread
import time
import json
import math
m = 13 #Finger Table max indexes
rangeo = pow(2,m)
# print(rangeo)
print("make sure port is between ", 0, " and ", rangeo)
filesList = []
succ = 0
pred = 0
fingertable = []
ip = 'localhost'
port = int(input("What is your port: "))
friend = int(input("who do you know: "))

def updatefingertable (index, portnumber):
    fingertable[0] = succ
    fingertable[index] = portnumber
    
def updatesucc():
    while(1):
        sendMsg = {"purpose": "whatisyourpred", "message": port}
        sendMessage(sendMsg, succ)
        time.sleep(2)

# s.bind(('localhost', port))
def sendMessage (sendMsg, friend1):
    try:
        # print("sending ", sendMsg, " to ", friend1 )
        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print ("Socket created")
        s.connect(('localhost', friend1))
        sendMsg= json.dumps(sendMsg)
        sendMsg= sendMsg.encode()
        s.send(sendMsg)
        # print("message sent!")
        # time.sleep(1)
            
        return 1
    except ConnectionRefusedError:
        pass
    except ConnectionResetError:
        pass
    finally:
        s.close()

def addNode(friend1, port1):
    sendMsg = {"purpose": "join", "message": port1}
    sendMessage(sendMsg, friend1)
    # time.sleep(1)
    return 1

def succpredStatus():
	print("\nSelf Port: " + str(port) + " \nSuccessor: " + str(succ) + "\nPredecessor: " + str(pred))


if (port == friend):
    pred = port
    succ = port
else:
    pred = port
    succ = port
    addNode(friend, port)


def amisucc(friend1, Pred1, Port1):
    global pred
    global succ
    global port
    global rangeo
    temp = (pred+1)%rangeo
    while (temp != port) :
        temp=(temp+1)%rangeo
        #print("checking: ", temp, " looking for ",friend1)
        if (temp == friend1):
            return True
    return False


def whoissucc (friend1, message):
    global m
    global fingertable
    # for i in range(m-1, -1, -1):
    # for i in range(len(fingertable)):
    #     if amisucc(message["message"], port, fingertable[i]):
    #         sendMessage(message, fingertable[i])
    #         print("checking: ", fingertable[i])
    sendMessage(message, succ)

def faizan(message):
    # print(message)
    global succ
    global pred
    if message["purpose"] == "join":
            print("Joining")
            checkifsucc = amisucc(message["message"], pred, port)
            print(checkifsucc)
            # succpred = succpred + [message["message"]]
            if(checkifsucc == True):
                sendMsg = {"purpose": "newpred", "message": pred, "newsucc": port}
                pred = message["message"]
                sendMessage(sendMsg, message["message"])
            elif(checkifsucc == False):# updatesuccandpred()
                whoissucc(message["message"], message)
            print("joined")
            # friend1 = message["message"]
            # sendsuccpred(friend1, port)
    if message["purpose"] == "leave":
        print("Node has left")
    if message["purpose"] == "whatisyourpred":
        sendMsg = {"purpose": "mypredis", "message": pred}
        sendMessage(sendMsg, message["message"])
        # print("sending pred")
    if message["purpose"] == "mypredis":
        if(message["message"]!=port):
            print("succ changed to", message["message"])
            succ = message["message"]
            print("we are connected, update your pred")
            sendMsg = {"purpose": "newpredinitial", "message": port}
            sendMessage(sendMsg, message["message"])
    if message["purpose"] == "newpredinitial":
        print("updating pred for the first time")
        pred = message["message"]
    if message["purpose"] == "file":
        print("incoming file")
    if message["purpose"] == "newpred":
        # Tell the pred that I am new succ
        succ = message["newsucc"]
        sendMsg = {"purpose": "newsucc", "message": port}
        sendMessage(sendMsg, message["message"])
        # Update your own pred to the new pred just recieved
        pred = message["message"]
        print("updating pred")
    if message["purpose"] == "newsucc":
        # Update own Succ
        succ = message["message"]
        print("updating succ")

        
    # else: 
    #     print("Message ajeeb sa tha")
    #     print(message)
    #     print(message["purpose"])

def threadlisten():
    global succ
    global pred
    global filesList
    global port
    sl= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print ("Socket created")
    sl.bind(('localhost', port))
    sl.listen()
    while True:
        c, addr = sl.accept()
        message= c.recv(1024).decode()
        message = json.loads(message)
        # print(message)
        faizandealer= Thread(target=faizan, args=[message])
        faizandealer.start()
        


def menu():
    while True:
        print("What do you wanna do?\n1. Upload File\n2. Download File\n3. Leave Chord\n4. View files in network\n5. View succpred")
        choice = int(input())
        if choice == 1:
            print("Select a file to upload")
        if choice == 2:
            print("Select a file to upload")
        if choice == 3:
            print("Sending a message to Succ and Pred to update their lists")
            exit()
        if choice == 4:
            print("Select a file to upload")
        if choice == 5:
            succpredStatus()



listenThread= Thread(target=threadlisten, args=[])
listenThread.start()

keepaskingforpredfromsucc= Thread(target=updatesucc, args=[])
keepaskingforpredfromsucc.start()

menu()
