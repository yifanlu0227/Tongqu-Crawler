from socket import *
import ssl
import base64
import os
import time

class Email():
    # default use SJTU mail server
    def __init__(self,recipient="yifan_lu@sjtu.edu.cn",text="TEST!"):
        _username = "yifan_lu@sjtu.edu.cn"
        _recipient = recipient # or other mailbox
        _passwd = "不告诉你"
        context = ssl.create_default_context()
        mailserver = ("smtp.sjtu.edu.cn",465)
        self.clientSocket = socket(AF_INET,SOCK_STREAM)
        self.clientSocketSSL = context.wrap_socket(self.clientSocket,server_hostname="smtp.sjtu.edu.cn")
        self.clientSocketSSL.connect(mailserver)
        recv = self.clientSocketSSL.recv(1024).decode()
        print("[Message] connection request:" + recv)
        if(recv[:3]!="220"):
            print("220 reply not received from SJTU server.")

        heloCommand = b"HELO smtp.sjtu.edu.cn\r\n"
        self.clientSocketSSL.send(heloCommand)
        recv = self.clientSocketSSL.recv(1024).decode()
        print("[Message] Helo request:" + recv)
        if(recv[:3]!="250"):
            print("250 reply not received from SJTU server.")

        loginCommand = b"AUTH login\r\n"
        self.clientSocketSSL.send(loginCommand)
        recv = self.clientSocketSSL.recv(1024).decode()
        print("[Message] Login request:" + recv)
        if(recv[:3]!="334"):
            print("334 reply not received from SJTU server.")


        self.clientSocketSSL.send(b"%s\r\n" % base64.b64encode(_username.encode()))
        recv = self.clientSocketSSL.recv(1024).decode()
        print("[Message] sending username:" + recv)
        self.clientSocketSSL.send(b"%s\r\n" % base64.b64encode(_passwd.encode()))
        recv = self.clientSocketSSL.recv(1024).decode()
        print("[Message] sending passwd:" + recv)   
        if(recv[:3]!="235"):
            print("235 reply not received from SJTU server. Check username or passwd.") 


        senderCommand = b"MAIL FROM:<%s>\r\n" % _username.encode()
        self.clientSocketSSL.send(senderCommand)
        recv = self.clientSocketSSL.recv(1024).decode()
        print("[Message] MAIL FROM:" + recv) 

        rcptCommand = b"RCPT TO:<%s>\r\n" % _recipient.encode()
        self.clientSocketSSL.send(rcptCommand)
        recv = self.clientSocketSSL.recv(1024).decode()
        print("[Message] RCPT TO:" + recv)   
        if(recv[:3]!="250"):
            print("250 reply not received from SJTU server. recipient error.") 

        dataCommand = b"DATA\r\n"
        self.clientSocketSSL.send(dataCommand)
        recv = self.clientSocketSSL.recv(1024).decode()
        print("[Message] DATA:" + recv)   
        if(recv[:3]!="354"):
            print("354 reply not received from SJTU server.")
        

        header = "From: tongqu\r\nTo: Subscriber <%s>\r\nSubject: Subject: Tongqu Activities Reminders <%s>\r\n" % (_recipient ,time.strftime("%Y-%m-%d"))
        mimeHeader = '\r\n'.join(['MIME-Version: 1.0',
                          'Content-Type: multipart/mixed; boundary="BOUNDARY"',
                          '\r\n'])
        textHeader = '\r\n'.join(['\r\n',
                          '--BOUNDARY',
                          'Content-Type: text/html; charset="UTF-8"',
                          'Content-transfer-encoding: 7bit',
                          '\r\n'])    
        endmsg = b"\r\n.\r\n"

        self.clientSocketSSL.send(header.encode())
        self.clientSocketSSL.send(mimeHeader.encode())
        self.clientSocketSSL.send(textHeader.encode())

        msg = (text+'\r\n').encode()  
        self.clientSocketSSL.send(msg)
        self.clientSocketSSL.send("<h3>THIS EMAIL IS SEND AUTOMATICALLY. DO NOT REPLY.</h3>\r\n\r\n".encode())
        self.clientSocketSSL.send(endmsg)
        recv = self.clientSocketSSL.recv(1024).decode()
        print("[Message] Sending Message:" + recv)  

        quitCommand = b"QUIT\r\n"
        self.clientSocketSSL.send(quitCommand)
        recv = self.clientSocketSSL.recv(1024).decode()
        print("[Message] Quit:" + recv)  

        self.clientSocketSSL.close()



if __name__ == "__main__":
    email = Email("TEST.")


