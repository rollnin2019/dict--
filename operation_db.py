import pymysql
import hashlib


class DataBase:
    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 passwd='123456',
                 charset='utf8',
                 database='dict'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db()  # 连接数据库

    def register(self, name, passwd):
        sql = 'select * from user where name = "%s"' % name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return False
        # 密码加密处理
        hash = hashlib.md5((name + '&&&').encode())
        hash.update(passwd.encode())
        passwd = hash.hexdigest()
        sql = 'insert into user (name,password) values (%s,%s)'
        try:
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def checklogin(self, name, passwd):
        hash = hashlib.md5((name + '&&&').encode())
        hash.update(passwd.encode())
        passwd = hash.hexdigest()
        sql = "select * from user where name ='%s' and password ='%s'" % (name, passwd)
        try:
            self.cur.execute(sql)
        except Exception:
            self.db.rollback()
            return False
        r = self.cur.fetchone()
        if r:
            self.db.commit()
            return True
        else:
            return False

    def query(self, word):
        sql = "select mean from words where word ='%s'" % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]

    def insert_history(self, name, word):
        sql = "insert into history (name,word) values (%s,%s)"
        try:
            self.cur.execute(sql, [name, word])
            self.db.commit()
        except Exception:
            self.db.rollback()

    def history(self, name):
        sql = "select name,word,time from history where name = '%s' order by time desc limit 10" % name
        self.cur.execute(sql)
        return self.cur.fetchall()


    def create_cursor(self):
        self.cur = self.db.cursor()

    def connect_db(self):
        self.db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            database=self.database,
            charset=self.charset
        )

    def close(self):
        """
        关闭数据库
        :return:
        """
        self.db.close()
