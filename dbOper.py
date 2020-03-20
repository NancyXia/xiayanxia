#!/usr/bin/env python
# coding:utf-8
import pymysql
#MYSQL_HOST='10.24.76.182'
#MYSQL_USER='tree'
#MYSQL_PWD='tree'
#MYSQL_DB='game_tree'
#MYSQL_PORT=5002
def createConn(MYSQL_HOST='10.24.76.182',MYSQL_USER='tree',MYSQL_PWD='tree',MYSQL_DB='game_tree',MYSQL_PORT=5002):
    try:
        return pymysql.connect(
                           host=MYSQL_HOST,
                           user=MYSQL_USER,
                           passwd=MYSQL_PWD,
                           db=MYSQL_DB,
                           port=MYSQL_PORT,
                           charset="utf8"
                           )
    except Exception as e:
        
        raise Exception(e)
    pass

class Sql():
    def __init__(self,conn=None,close=True,MYSQL_HOST='10.24.76.182',MYSQL_USER='tree',MYSQL_PWD='tree',MYSQL_DB='game_tree',MYSQL_PORT=5002):
        self.close=close
        self.MYSQL_HOST=MYSQL_HOST
        self.MYSQL_USER=MYSQL_USER
        self.MYSQL_PWD=MYSQL_PWD
        self.MYSQL_DB = MYSQL_DB
        self.MYSQL_PORT = MYSQL_PORT
        print(self.MYSQL_HOST)
        #if not conn:
        self._db_conn=createConn(self.MYSQL_HOST,self.MYSQL_USER,self.MYSQL_PWD,self.MYSQL_DB,self.MYSQL_PORT)
        #else:
        #self._db_conn=conn
    def closedb(self):
        if self._db_conn:
            try:self._db_conn.close()
            except:pass
    def update(self,sql,param=None):
        cursor = None
        data=None
        try:
            cursor = self._db_conn.cursor()
            cursor.execute(sql, param)
            self._db_conn.commit()
        except Exception as e:
            
            raise Exception(e)
        finally:
            if cursor:cursor.close()
            if self.close and self._db_conn:
                try:self._db_conn.close()
                except:pass
            return True
    def query(self,sql, param=None):
        cursor = None
        data=None
        try:
            cursor = self._db_conn.cursor()
            cursor.execute(sql, param)
            data=cursor.fetchall()
        except Exception as e:
            raise Exception(e)
        finally:
            if cursor:cursor.close()
            if self.close and self._db_conn:
                try:self._db_conn.close()
                except:pass
            return data
if __name__=="__main__":
    import datetime
    stime=datetime.datetime.now()-datetime.timedelta(days=5)
    starttime=datetime.datetime.now().strftime('%Y-%m-%d')
    endtime=stime.strftime('%Y-%m-%d') 
    onlinesql="select * from friend_1";         
    print (onlinesql)
    result=Sql().query(onlinesql)
    for i in result:
        for j in i:
            print (j)
    MYSQL_HOST='10.48.201.76';
    MYSQL_USER='player7'
    MYSQL_PWD='player7'
    MYSQL_DB='player7'
    MYSQL_PORT=5002
    onlinesql="select * from player57";         
    print (onlinesql)
    result_1=Sql(None,True,MYSQL_HOST,MYSQL_USER,MYSQL_PWD,MYSQL_DB,MYSQL_PORT).query(onlinesql)
    for m in result_1:
        for n in m:
            print (n)