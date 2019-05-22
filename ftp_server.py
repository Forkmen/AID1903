'''
服务端
'''
from socket import *
from threading import Thread
from time import sleep
import sys,os

ADDR = ('0.0.0.0',4546)
FTP_PATH = '/home/tarena/'
#功能类
class FtpServer:
    def __init__(self,connfd,FTP):
        self.connfd = connfd
        self.path = FTP

    def do_look(self):
        files = os.listdir(self.path)
        if not files:
            self.connfd.send('文件内容为空'.encode())
        else:
            self.connfd.send(b'OK')
            sleep(0.01)
        fs = ''
        for i in files:
            if i[0] != '.' or os.path.isfile(self.path + i):
                fs = fs + i +'\n'
        self.connfd.send(fs.encode())
    def do_get(self,filename):
        try:
            f = open(self.path+filename,'rb')
        except Exception as e:
            self.connfd.send('文件不存在'.encode())
            sys.exit(e)
        else:
            self.connfd.send(b'OK')
            sleep(0.01)
        while True:
            data = f.read(1024)
            if not data:
                self.connfd.send(b'##')
                break
            self.connfd.send(1024)
        f.close()


    def do_put(self,filename):
        try:
            f = open(self.path+filename,'wb')
        except Exception:
            self.connfd.send('打开文件失败'.encode())
            return
        else:
            self.connfd.send(b'OK')
            while True:
                data = self.connfd.recv(1024).decode()
                if data == '##':
                    break
                f.write(data)
            f.close()

def handle(connfd):
    while True:
        cls = connfd.recv(1024).decode()
        FTP= FTP_PATH + cls + '/'
        ftp = FtpServer(connfd,FTP)
        while True:
            data = connfd.recv(1024).decode()
            if not data:
                return
            elif data[0] == 'L':
                ftp.do_look()
            elif data[0] == 'G':
                ftp.do_get(data[-1])
            elif data[0] == 'P':
                ftp.do_put(data[-1])

def main():
    sockfd = socket()

    sockfd.bind(ADDR)
    sockfd.listen(3)
    print('Listen the port 4545.....')
    while True:
        try:
            connfd,addr = sockfd.accept()
        except KeyboardInterrupt:
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
        else:
            t = Thread(target=handle,args=(connfd,))
            t.start()
            t.setDaemon(True)

if __name__ == '__main__':
    main()