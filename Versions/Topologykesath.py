import socket
import os
from threading import Thread
import time
import json

filesList = []
succ = 0
pred = 0
topology = []
fingertable = []
ip = 'localhost'
port = int(input("What is your port: "))
friend = int(input("who do you know: "))

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
    global topology
    sendMsg = {"purpose": "join", "message": port1}
    # print(topology)
    sendMessage(sendMsg, friend1)
    time.sleep(1)
    return 1

def sendTopology(friend1, port1):
    global topology
    # print("sending topology")
    # print(friend1)
    sendMsg = {"purpose": "recievetopology", "message": topology}
    sendMessage(sendMsg, friend1)
    # print("Topology sent!")
    return 1

def topologyStatus():
	print("\nSelf Port: " + str(port) + " \nSuccessor: " + str(succ) + "\nPredecessor: " + str(pred))

def updatesuccandpred():
    global pred
    global port
    global succ
    global topology
    topology = sorted(topology)
    # print(topology)
    for index in range(len(topology)):
        if (topology[index] == port):
            pred = topology[index-1]
            succ = topology[(index+1)%(len(topology))]
    topologyStatus()

if (port == friend):
    topology = topology + [int(port)]
    pred = port
    succ = port
else:
    topology = topology + [int(port)]
    addNode(friend, port)
    print("Node added")
   # topology = topology + [int(port)] + [int(friend)]
    print(topology)
    updatesuccandpred()

def faizan(message):
    global topology
    # print(message)
    if message["purpose"] == "join":
            print("Joining")
            topology = topology + [message["message"]]
            updatesuccandpred()
            print("joined")
            friend1 = message["message"]
            sendTopology(friend1, port)
    if message["purpose"] == "leave":
        print("Node has left")
    if message["purpose"] == "update":
        print("Updating nodes")
    if message["purpose"] == "file":
        print("incoming file")
    if message["purpose"] == "recievetopology":
        print("recieving updated topology from friend node")
        topology = message["message"]
        print(topology)
        updatesuccandpred()
        
    # else: 
    #     print("Message ajeeb sa tha")
    #     print(message)
    #     print(message["purpose"])

def threadlisten():
    global topology
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
        print("What do you wanna do?\n1. Upload File\n2. Download File\n3. Leave Chord\n4. View files in network\n5. View topology")
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
            topologyStatus()
            print(topology)



listenThread= Thread(target=threadlisten, args=[])
listenThread.start()

menu()
