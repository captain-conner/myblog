from django.test import TestCase
from django.db import connection
from blog.models import *
from blog.form import *
from django.core.mail import send_mail
# Create your tests here.

import smtplib,sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from blog.sendEmail import *
#send_mail('test','this is the django mail','captain2conner@163.com',['1665506061@qq.com'],fail_silently=False)
from django.db.models import Count
a = Article.objects.values('date_publish').count()
print (a)
