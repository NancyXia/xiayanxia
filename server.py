#!/usr/bin/env python
import web
import uuid
import os
import chardet
import smtplib
import urllib
import dbOper
import datetime
import shutil
import mymail
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
import traceback
import sys
import importlib
#importlib.reload(sys)


render=web.template.render('templates/')
urls=(
    '/','submit',
    '/submit','submit',    
    '/task','task',
    '/detail','detail',
    '/(.*.ico)', 'StaticFile',
    )
# TaskFile=os.path.join(os.getcwd(),"task.txt")
app=web.application(urls,globals())

def cover_to_gbk(msg):
    __re_str = None
    if isinstance(msg, unicode):
        try:
            __re_str = msg.encode('gbk',"ignore")
        except Exception as e:
            print(e)
            __re_str=msg
    elif isinstance(msg, str):
        try:
            c=chardet.detect(msg)["encoding"]
            __re_str=msg.decode(c).encode('gbk',"ignore")
        except:
            __re_str=msg
    elif isinstance(msg, int):
        __re_str=msg
    else:
        __re_str=msg
    return __re_str
def covert_to_utf8(msg):    
    __re_str = None
    if isinstance(msg, unicode):
        try:
            __re_str = msg.encode('utf-8')
        except Exception as e:
            print (e)
            __re_str=msg
    elif isinstance(msg, str):
        __re_str=msg
    elif isinstance(msg, int):
        __re_str=msg
    else:
        pass
    return __re_str        

class StaticFile():  
    def GET(self, fileName):  
        web.seeother('/static/'+fileName)

class detail():        
    def GET(self):
        ip=web.ctx.ip
        if ip=="10.16.26.91":
            return
        id=web.input().keys()[0]
        dsql='select * from feedbackreport where id="%s"'%id
        dresult=dbOper.Sql().query(dsql)                     
        return  render.detail(dresult)      
    def POST(self):
        ip=web.ctx.ip
        if ip=="10.16.26.91":
            return
        id=""             
        keylist=web.input().keys()
        comment=web.input()['comment']
        commentHtml=comment+"**"        
        for i in keylist: 
                       
            if i!='comment':
                id=i
        usql="update feedbackreport set comment=concat(comment,'%s') where id='%s' "%(commentHtml,id)

        dbOper.Sql().update(usql)
        raise web.seeother('/detail?%s'%id)                
            
class task():  
    def GET(self):        
        ip=web.ctx.ip
        if ip=="10.16.26.91":
            return             
        input=web.input(requestname="",  qa="", important="", feedbackdate="")
        requestname=input.requestname
        qa=input.qa
        important=input.important
        feedbackdate=input.feedbackdate
       
        condition=[]
        conditionStr=sql=''
        if requestname:
            condition.append(" briefdes like '%%%s%%'"%str(requestname)) 
        if qa:
            condition.append(" tester= '%s' "%qa)
        if important:
            condition.append(" priority='%s'"%str(important))
        if feedbackdate:
            condition.append(" subdate = '%s'"%str(feedbackdate))
        if len(condition)>0:
            conditionStr=" and ".join(condition)
            sql=" select * from feedbackreport where %s order by subdate desc "%conditionStr
        else:
            sql="select * from feedbackreport order by subdate desc" 
                   
        result=dbOper.Sql().query(sql)        
        return render.task(result)
    def POST(self):       
        ip=web.ctx.ip
        if ip=="10.16.26.91":            
            return             
        applylist=web.input(applylist=None).applylist                         
        if not applylist:            
            raise web.seeother('/task')
        sql=""                
        applylist=applylist.split(";")
        taskid=applylist[0].encode("utf-8") 
        status=applylist[1].replace('status=','').encode("utf-8")
        resoluton=applylist[2].replace('resoluton=','').encode("utf-8")
        notice=applylist[3].replace('notice=','').encode("utf-8")        
        packageversion=applylist[4].replace('packageversion=','').encode("utf-8")
        reason =applylist[5].replace('reason=','').encode("utf-8")       
        qa=applylist[6].replace('qa=','').encode("utf-8")  
        sql='update feedbackreport set bugstatus="%s",bugresolution="%s",notice="%s",packageversion="%s",reason="%s",tester="%s" where id="%s" '%(status,resoluton,notice,packageversion,reason,qa,taskid)       
        
        dbOper.Sql().update(sql)        
        raise web.seeother('/task')

def copyFile(sourceFile, destFile): 
    if not os.path.exists(sourceFile.encode('gb2312')):
        return False
    else:
        shutil.copy (sourceFile.encode('gb2312'), destFile)
        return True
class submit():
    def GET(self):
        ip=web.ctx.ip
        if ip=="10.16.26.91":
            return
        return  render.submit()      
    def POST(self):
        ip=web.ctx.ip
        if ip=="10.16.26.91":
            return  
        def __format_input__():
            input=web.input()         
            data={}
            for key in input:
                data[key]=covert_to_utf8(input[key])
            return data                 
        taskid=str(uuid.uuid1())       
        data=__format_input__() 

        arr=newarr=[]      
                   
        curdate=datetime.datetime.now().strftime("%Y-%m-%d") 
        sql='''insert into feedbackreport(id,briefdes,detaildes,incidence,bugid,solvestatus,bugstatus,issuetype,feedcount,remarks,tester,priority,subdate,notice,reason,packageversion,comment)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''            
        param = [taskid,data['request'],data['feedbackde'],data['scope'],data['bugid'],data['status'],'',data['type'],data['feedcount'],data['descr'],data['qa'],data['priority'],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'','','','']
        dbOper.Sql().update(sql,param)        
        raise web.seeother('/task')               
if __name__=="__main__":    
   
    try:
        app.run()
    except:
        pass
