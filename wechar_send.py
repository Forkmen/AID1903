from socket import *
import os,sys

#服务器地址
ADDR = ('176.215.155.11',4567)

#创建网络链接
def main():
    s = socket(AF_INET,SOCK_DGRAM)
    while True:
        name = input("请输入姓名注册:")
        msg = "L " + name
        s.sendto(msg.encode(),ADDR)
        #等待回应
        data,addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print("欢迎来到蔡徐坤的聊天室")
            break
        else:
            print(data.decode())
    #创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit('Error')
    elif pid == 0:
        send_msg(s,name)
    else:
        recv_msg(s,name)
 #发送消息
def send_msg(s,name):
    while True:
        try:
            text = input("有啥话想对蔡徐坤说:")
        except KeyboardInterrupt:
            text == 'quit'
        if text == 'quit':
            msg = 'Q' + name
            s.send(msg.encode(),ADDR)
            sys.exit("退出聊天")
        msg = 'C %s %s'%(name,text)
        s.sendto(msg.encode(),ADDR)
 #接受消息
def recv_msg(s,name):
    while True:
        data,addr = s.recvfrom(1024)
        #发送端退出后服务器删除姓名后
        # 给接收端发送退出指令从而退出接收端进程
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode()+"\n发言",end='')
if __name__ == '__main__':
    main()