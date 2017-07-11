import smtplib,sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def sendContactEmail(name,email,subject,comments):
    body = subject+'\n' + comments + '\n' +'send from '+name+'\n'+ 'Email:' +email
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['from'] = 'captain2conner@163.com'
    msg['to'] = '1665506061@qq.com'
    msg['Subject'] = subject

    from_addr = 'captain2conner@163.com'
    # 输入Email地址和口令:
    password = 'captain138297'
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.163.com'
    # 输入收件人地址:
    to_addr = '1665506061@qq.com'


    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    print("邮件发送成功")
