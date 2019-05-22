'''
Chat room
env:python3.6
socket fork
聊天室服务端程序
'''
from socket import *
import os,sys
#创建网络连接
ADDR = ('0.0.0.0',4567)

#存储用户信息
user = {}
#接受各种客户端请求
def do_request(s):
    while True:
        data,addr = s.recvfrom(1024)
        msg = data.decode().split(' ')
        #区分请求类型
        if msg[0] == "L":
            do_login(s,msg[1],addr)
        elif msg[0] =='C':
            do_chat(s,msg[1],''.join(msg[2:]))
        elif msg == "Q":
            if msg[1] not in user:
                s.sendto(b'EXIT',addr)
                break
            do_quit(s,msg[1])

#聊天
def do_chat(s,name,test):
    msg = '%s :%s'%(name,test)
    for i in user:
        if i !=name:
            s.sendto(msg.encode(),user[i])

#退出处理
def do_quit(s,name):
    msg = '\n%s退出了聊天室'%name
    for i in user:
        if i !=name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b'EXIT',user[i])
    #删除用户信息
    del user[name]

#处理登录是姓名处理
def do_login(s,name,addr):
    if name in user or "管理员" in name:
        s.sendto('该用户以存在'.encode(),addr)
        return

    s.sendto(b'OK',addr)
    #通知其他人
    msg = '\n欢迎%s进入聊天室'%name
    for i in user:
        s.sendto(msg.encode(),user[i])
    #将用户加入
    user[name] = addr

def main():
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)
    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        while True:
            msg = input('管理员消息:')
            msg = 'C 管理员消息 '+ msg
            s.sendto(msg.encode(),ADDR)#将信息发给父进程通过父进程发送给所有人
    else:
        #请求处理
        do_request(s)#处理客户端请求

if __name__ == '__main__':
    main()