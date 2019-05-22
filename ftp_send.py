'''
发送端
'''
from socket import *
from threading import Thread
import sys,os

ADDR = ('127.0.0.1',4546)
class FtpClient:
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def do_look(self):
        self.sockfd.send(b'L')
        #等待回复
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            data = self.sockfd.recv(1024).decode()
            print(data)
        else:
            print(data)

    def do_get(self,filename):
        self.sockfd.send(('G '+filename).encode())
        #等待回复
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            f = open(filename,'wb')
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                f.write(data)
            f.close()
        else:
            print(data)

    def do_put(self,filename):
        self.sockfd.send(('P'+filename).encode())
        #等待回复
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            f = open(filename,'rb')
            while True:
                data = f.read(1024)
                if not data:
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(1024)
            f.close()
        else:
            print(data)
    def quit(self):
        pass

def request(sockfd):
    ftp = FtpClient(sockfd)
    while True:
        print('''\n=========命令选项==============
              look file            
              get file (eg:get ***.jpg)
              put file (eg:get /***.jpg)            
                quit                       
               ''')
        cmd = input('输入命令')
        if cmd[:4].strip() == 'look':
            ftp.do_look()
        elif cmd[:3].strip() == 'get':
            ftp.do_get(cmd[-1])
        elif cmd[:3].strip() == 'put':
            ftp.do_put(cmd[-1])
        elif cmd == 'quit':
            ftp.quit()

def main():
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception:
        sys.exit('未能成功链接')
    else:
        print('''**************
Data File Images
*****************
        ''')
        cls = input('请输入需要操作的文件:')
        if cls not in ['Data','File','Images']:
            return
        else:
            sockfd.send(cls)
            request(sockfd)

if __name__ == '__main__':
    main()