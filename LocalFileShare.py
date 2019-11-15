from zipfile import ZipFile
import socket
import time
import sys
import os
s = socket.socket()
port = 65432

def returnLocalIP():
    '''Get this machines local IP Address (ex. 192.168.0.17)'''
    hostName = socket.gethostname()
    hostIP = socket.gethostbyname(hostName)
    return hostIP

def otherMachineIP(filename="otherMachine.ip"):
    '''Returns the other machines IP address as specified in the text file'''
    open(filename, 'a')
    return open(filename, 'r').readline()

def changeIP():
    '''Changes the IP in the otherMachine.ip file'''
    newIP = input("Other computers new IP: ")
    f = open('otherMachine.ip', 'w')
    f.write(newIP);f.close()
    print(f"Other Computers IP: {newIP}\n")	

		
def recv():
    otherHost = open('otherMachine.ip', 'r').readline()
    s.connect((otherHost, port))
    
    filename = s.recv(4096)
    print('Client received', repr(filename))

    # Get the file
    with open(filename.decode("utf-8"), 'wb') as f:
        print('file opened')
        while True:
            data = s.recv(4096)
            if not data:
                break
            f.write(data)
    f.close();s.close()

    # Unzips the files, then delete the zip
    with ZipFile(filename.decode("utf-8"), 'r') as unzipObj:
       unzipObj.extractall()    
    
    print('[✓] Successfully got the file')

    s.close()
    os.remove(filename.decode("utf-8"))
    sys.exit(0)    

	
def send():
    s.bind((returnLocalIP(), port))
    s.listen(5)  
    files = input("Files to transfer (Space Delimited): ").split(' ')
    filename = files[0].split('.')[0] + '.zip'
    print("[!] Waiting for Connection...")
    
    while True:
        conn, clientAddr = s.accept()
        print('[✓] Connected:', clientAddr[0])

        with ZipFile(filename,'w') as zip:
            for file in files:
                try:
                    zip.write(file) 
                except:
                    print(f"{file} was not in the current folder")        

        data = conn.send(bytes('SENT_' + filename, 'utf-8'))

        f = open(filename,'rb')
        l = f.read(4096)
        while (l):
           conn.send(l)
           l = f.read(4096)
        f.close()

        print(f"[✓] {filename} has been sent\n")
        conn.close()
        os.remove(filename)
        sys.exit(0)	
		
while True:
    userInput = input('Send, Recv, NewIP: ').lower()
    actions = {
        'recv': recv,
        'send': send,
        'newip': changeIP,
        }
    actions[userInput]()

    		
