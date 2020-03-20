#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from email.MIMEImage import MIMEImage
import traceback
def sendMailPic(sender, receiver, subject, content, part=None, cc=[]):
    try:
        if type(receiver) == str:
            receiverList=[]
            receiverList=receiver.split(';')
            receiver = receiverList
    
        msgRoot = MIMEMultipart('related')
        msgRoot['From'] = sender
        msgRoot['To'] = ', '.join(receiver)
        if cc:
            if type(cc) == str:
                cc = [cc]
                receiver.extend(cc)
                msgRoot['Cc'] = ', '.join(cc)
        msgRoot['Subject'] = subject
        msgText = MIMEText(content, 'html', 'gbk')
        msgRoot.attach(msgText)
    
        if part and os.path.exists(part):
            att = MIMEText(open(part, 'rb').read(), 'base64', 'gb2312')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(part)
            msgRoot.attach(att)
     
        smtp = smtplib.SMTP() 
        smtp.connect('mail.corp.qihoo.net') 
        smtp.sendmail(sender, receiver, msgRoot.as_string()) 
        smtp.quit()
    except:        
        print (traceback.format_exc())



sendMailPic('xiayanxia@360.cn', ['xiayanxia@360.cn'], '123123123123', '123123123', part=r'd:\GUI自动化测试基础.docx')