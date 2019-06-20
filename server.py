from socket import *
import multiprocessing as mp
from operation_db import DataBase
import signal, sys
from time import sleep

db = DataBase()

# 创建套接字
HOST = '0.0.0.0'
PORT = 2020
ADDR = (HOST, PORT)


def do_register(c, data):
    """
    注册处理
    """
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.register(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')


def do_login(c, data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.checklogin(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'wrong login')


def do_query(c, data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]
    db.insert_history(name, word)
    mean = db.query(word)
    if not mean:
        c.send('没有找到'.encode())
    else:
        msg = "%s : %s" % (word, mean)
        c.send(msg.encode())


def do_hist(c, data):
    name = data.split(' ')[1]
    r = db.history(name)
    if not r:
        c.send(b'Fail')
        return
    c.send(b'OK')

    for i in r:
        msg = "%s   %-16s    %s" % i
        sleep(0.1)
        c.send(msg.encode())
    sleep(0.1)
    c.send(b'##')


def handle(c):
    """
    接受客户端请求 分配处理函数
    :param c:
    :return:
    """
    db.create_cursor()  # 生成数据库游标
    while 1:  # 第一层界面
        data = c.recv(1024).decode()
        print(c.getpeername(), ':', data)
        if not data or data[0] == 'E':
            sys.exit()
        elif data[0] == 'R':
            do_register(c, data)
        elif data[0] == 'L':
            do_login(c, data)
        elif data[0] == 'Q':
            do_query(c, data)
        elif data[0] == 'H':
            do_hist(c, data)
    # 第二层界面



def main():
    s = socket()  # TCP套接字
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while 1:
        try:
            c, addr = s.accept()
            print('connect from', addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit('server quit')
        except Exception as e:
            print(e)
            continue
        p = mp.Process(target=handle, args=(c,))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
