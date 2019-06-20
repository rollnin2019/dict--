"""
dict 客户端
功能:根据用户输入 发送请求 得到结果
结构 : 一级界面 -->注册 登录 退出
二级界面 --> 查单词 历史记录 注销
"""
from socket import *
from getpass import getpass  # 运行使用终端
import sys

sockfd = socket()  # 参数默认
server_addr = ('127.0.0.1', 2020)
sockfd.connect(server_addr)  # 发起连接


def do_register():
    while 1:
        name = input('plz input User name:')
        passwd = getpass()
        passwd_ = getpass('Again:')
        if (' ' in name) or (' ' in passwd):
            print('用户名或密码不能有空格')
            continue
        if passwd != passwd_:
            print('两次密码不一致')
            continue
        msg = 'R %s %s' % (name, passwd)
        sockfd.send(msg.encode())
        data = sockfd.recv(1024).decode()  # 接受反馈信息
        if data == 'OK':
            print('注册成功')
            q2(name)
            return 1
        else:
            print('注册失败')
            return False


def do_login():
    name = input('plz input User name:')
    passwd = getpass()
    msg = 'L %s %s' % (name, passwd)
    sockfd.send(msg.encode())
    data = sockfd.recv(1024).decode()  # 接受反馈信息
    if data == 'OK':
        print('登录成功')
        q2(name)
    else:
        print(data)


def do_query(name):
    """
    单词查找
    :param name:
    :return:
    """
    while 1:
        word = input('单词:')
        if word == '##':  # 结束单词查询
            break
        msg = 'Q %s %s' % (name, word)
        sockfd.send(msg.encode())
        data = sockfd.recv(2048).decode()
        print(data)   # 得到查询结果


def do_hist(name):
    msg = 'H %s' % name
    sockfd.send(msg.encode())
    data = sockfd.recv(128).decode()
    if data == 'OK':
        while 1:
            data = sockfd.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print('没有历史记录')


def main():
    while 1:
        print("""
        =================welcome=====================
        1.注册       2.登录       3.退出
        =============================================
        """)
        cmd = input('输入选项:')
        if cmd == '1':
            do_register()

        elif cmd == '2':
            do_login()

        elif cmd == '3':
            sockfd.send(b'E')
            sys.exit("谢谢使用")
        else:
            print('请输入正确选项')


def q2(name):
    while 1:
        print("""
        =================welcome=====================
        1.查单词       2.历史记录       3.注销
        =============================================
        """)
        cmd = input('输入选项:')
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_hist(name)
        elif cmd == '3':
            return
        else:
            pass


if __name__ == '__main__':
    main()
