import socket
import os
from threading import Thread
import time
import json
import math
import hashlib

sockforfiles = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

exit1 = False
m = 13 #Finger Table max indexes
rangeo = pow(2,m)
# print(rangeo)
print("make sure port is between ", 0, " and ", rangeo)
filesList = []
succ = 0
succofsucc = 0
pred = 0
fingertable = []
ip = 'localhost'
port = int(input("What is your port: "))
friend = int(input("who do you know: "))
counterforsucc = 0
counter = 0

def updatefingertable (index, portnumber):
    fingertable[0] = succ
    fingertable[index] = portnumber
    
def updatesucc():
    while(exit1==False):
        sendMsg = {"purpose": "whatisyourpred", "message": port}
        sendMessage(sendMsg, succ)
        time.sleep(2) # THIS ALSO does failiure resistence by making sure the succ of succ is updated and 3 times not responding will kick the node
        sendMsg = {"purpose": "whatisyoursucc", "message": port}
        sendMessage(sendMsg, succ)
    exit()

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
        # time.sleep(3)
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

def faizan(message, sockold):
    # print(message)
    global succ
    global pred
    global counterforsucc
    global succofsucc
    global sockforfiles
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
    if message["purpose"] == "whatisyoursucc":
        sendMsg = {"purpose": "mysuccis", "message": succ}
        sendMessage(sendMsg, message["message"])
        # print("sending succ")
    if message["purpose"] == "mysuccis":
        succofsucc = message["message"]
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
    if message["purpose"] == "testcounter":
        a = message["message"] + 1
        sendMsg = {"purpose": "testcounterreturn", "message": a }
        sendMessage(sendMsg, message["from"])
    if message["purpose"] == "recievefile":
        filehere = amisucc(message["message"],pred,port)
        if filehere == True:
            print("file is for me")
            sockforfiles = sockold
            recieveFile(message["from"], message, sockforfiles)
            # RECIEVE FILE FUNCTION SHOULD START HERE
        elif(filehere == False):
            sendMessage(message, succ)
    if message["purpose"] == "sendhere":
        sendFile(message["filename"],message["message"], 8193)
    if message["purpose"] == "downloadrequest":
        sendFile(message["filename"],message["message"], message["from"])
        filehere = amisucc(message["message"],pred,port)
        if filehere == True:
            print("I have the file and I will send rn!")
            sockforfiles = sockold
            sendFile(message["filename"], message["message"], 8193)
            # RECIEVE FILE FUNCTION SHOULD START HERE
        elif(filehere == False):
            sendMessage(message, succ)

def threadlisten():
    global succ
    global pred
    global filesList
    global port
    sl= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print ("Socket created")
    sl.bind(('localhost', port))
    sl.listen()
    while exit1==False:
        c, addr = sl.accept()
        try:
            message= c.recv(1024).decode()
            message = json.loads(message)
            # print(message)
            faizandealer= Thread(target=faizan, args=[message, c])
            faizandealer.start()
            checkifsuccresponding= Thread(target=checkforsucccounteronly, args=[message])
            checkifsuccresponding.start()
        except UnicodeDecodeError:
            pass
    exit()
        
def checkforsucccounteronly(message):
    global counter
    global succofsucc
    if message["purpose"] == "testcounterreturn":
        # print("still connected to succ")
        counter = 0
    elif message["purpose"] != "testcounterreturn":
        counter = counter+1
    if counter == 9:
        succ = succofsucc
        counter = 0
        #sendMsg = {"purpose": "newpredinitial", "message": port}
        sendMsg = {"purpose": "join", "message": port}
        sendMessage(sendMsg, succofsucc)
        succofsucc = succ
        time.sleep(1)

def giveHash(filename):
	hash_object = hashlib.md5(filename.encode())
	hexHash= hash_object.hexdigest()
	value= int(hexHash, 16)
	value= value%rangeo
	return value

###############################################################################################################################
#     hashValue= giveHash(filename)
#     sendFile(filename,hashValue)
#     fileHash= int(fileInfo[0])
#     fileName= fileInfo[1]
#     targetNode= findNodeForHash(fileHash)
#     requestFile(targetNode,fileName)

###############################################################################################################################

def sendFile(filename, hashValue, port2send2): 
    global sockforfiles
    try:
        sockforfiles.connect(('localhost', port2send2))
        print("snedinh")
        with open(filename, 'rb') as f:
            sent = sockforfiles.sendfile(f,0)
            print("bytes sent: ", sent)
        if(exit1==True):
            exit()
    except ConnectionRefusedError:
        pass
    except ConnectionResetError:
        pass
    finally:
        print("closing file transfer socket")
        # time.sleep(3)
        sockforfiles.close()
#######################################################################################################################

def recieveFile(port1, message, sock):
    global sockforfiles
    sockforfiles = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockforfiles.bind(('localhost', 8193))
    sendMsg = {"purpose": "sendhere", "message": message["message"], "from": 8193, "filename": message["filename"]}

    filename = message["filename"]
    try:

        # sockforfiles.connect(('localhost', port1))
        
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Flag socket to close port immediately after disconnection
        sockforfiles.listen(1)
        print("listening!")
        sendMessage(sendMsg, port1)
        inSock = sockforfiles.accept()[0]
        f= open(filename,'wb')
        i=0
        while exit1 == False:
            # print("writing to file!")
            l= inSock.recv(1024)
            # print("chunk recieved ", l)
            f.write(l)
            if not l:
                break
            i=i+1
        time.sleep(3)
        f.close()
        print("downloaded")
    # except ConnectionRefusedError:
    #     pass
    # except ConnectionResetError:
    #     pass
    finally:
        time.sleep(3)
        inSock.close()
        print("closed")

def menu():
    global exit1
    while exit1==False:
        print("What do you wanna do?\n1. Upload File\n2. Download File\n3. Leave Chord\n4. View files in network\n5. View succpred")
        choice = int(input())
        if choice == 1:
            print("Select a file to upload")
            os.system("DIR")
            try:
                filename= str(input("Out of these files, which one do you want to upload? Enter q to go back: "))
                if(filename=="q"):
                    continue
                pass
            except EOFError:
                os._exit(1)
            hashValue= giveHash(filename)
            filehere = amisucc(hashValue,pred,port)
            if filehere == True:
                print("file need not move")
            elif filehere == False:
                sendMsg = {"purpose": "recievefile", "message": hashValue, "from": port, "filename": filename}
                sendMessage(sendMsg, succ)
        if choice == 2:
            filename = str(input("Enter name of the file you wish to download. Enter q to go back: "))
            if(filename=="q"):
                    continue
            hashValue= giveHash(filename)
            filehere = amisucc(hashValue,pred,port)
            if filehere == True:
                print("file hashes to your port and either you have it or it doesn't exist")
            elif filehere == False:
                sendMsg = {"purpose": "downloadrequest", "message": hashValue, "from": port, "filename": filename}
                sendMessage(sendMsg, succ)
        if choice == 3:
            print("Sending a message to Succ and Pred to update their lists")
            exit1 = True
            exit()
            return
        if choice == 4:
            print("Select a file to upload")
        if choice == 5:
            succpredStatus()
            print ("succofsucc is ", succofsucc)
    exit()

def failiureResistance(): #Doing this by making a test counter that will send an int to the succ and expect an int+1 back everytime, if failiure to recieve then will remove node
    global counterforsucc
    global succ
    sendMsg = {"purpose": "testcounter", "message": counterforsucc, "from": port}
    while(exit1==False):
        sendMessage(sendMsg,succ)
        time.sleep(1)
    exit()
    

        
print (succofsucc)
    

listenThread= Thread(target=threadlisten, args=[])
listenThread.start()

keepaskingforpredfromsucc= Thread(target=updatesucc, args=[])
keepaskingforpredfromsucc.start()


failsafe= Thread(target=failiureResistance, args=[])
failsafe.start()

menu()
exit()