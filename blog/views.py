from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse
from django.db import connection
from blog.models import *
import json
import os
import time
#添加日志文件
import logging
#使用setting中自定义的项
from django.conf import settings
#csrf的解决文件
from django.views.decorators.csrf import csrf_exempt
#分页类,实现分页的功能.
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

#发送邮件模块
from django.core.mail import send_mail
from blog.sendEmail import *
from blog.form import *
#实现了预处理函数之后,每个页面都能够以变量的形式调用给数值
def personalMesage(request):
    print("运行了预处理函数")
    return {'siteName':settings.SITE_NAME,'myEmail':settings.MY_EMAIL,}

#解决模板参数的重复,可以直接定义预处理函数
def global_proxy(request):
    #这里定义模板需要的标签参数,然后就可以在模板中使用了,不需要在view中的url处理函数中频繁传递.
    return locals()

#主页
#主要的版块是(从左到右 三块):
#最近博文 , 主要兴趣, 微薄记录

def index(request):

    latest_blog = Article.objects.order_by('-date_publish')[0:1]
    return render(request,'index.html',{'latest_blog':latest_blog[0]})

#博客
def blog(request):

    '''
    先获取数据库文章的数量,
    然按照最新的文章,选出然虎按照最新的文章,选出5篇进行选出
    传递数据为:标题 和文章内容,存放在字典数组中.{'title':,'content':}
    点击blog标题会跳转到博客的具体页面.
    实现分页显示的功能.

    以?分割URL和传输数据，多个参数用&连接；例如：login.action?name=hyddd&password=idontknow&verify=%E4%BD%A0 %E5%A5%BD。
    get 方法获取的参数主要是:
    1 page页数 2 archive 归档 3 cat分类 4 id 具体某一页
    然后根据参数,传递设置分页管理器的数据
    '''
    #分类栏
    categorys = Category.objects.all()
    cate = request.GET.get('cat','')


    #归档数据
    sql = "SELECT DATE_FORMAT(date_publish,'%Y-%m') From blog_article ORDER BY  blog_article.date_publish DESC LIMIT 21;"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
     #归档去重复(本来可以在mysql实现,妈蛋语不行)
    s = set(rows)
    archives = {}

    for x in s:
        #某一列归档的文章数量
        #count = len(Article.objects.filter(date_publish__contains=x[0])) 这个方法已经优化,下面是心方法
        count = Article.objects.filter(date_publish__contains=x[0]).values('date_publish').count()
        archives.setdefault(x[0],count)

    archives_date = request.GET.get('archive','')

    blog_id = request.GET.get('id','')




    #接受分页的参素,然后根据参数来进行内容的定义和分页显示.
    #右边功能的判断

    if blog_id != '' :
        articles = Article.objects.filter(id=int(blog_id))
    elif archives_date == '' and cate == '':
        articles = Article.objects.order_by('-date_publish')

    elif archives_date != '':
        articles = Article.objects.filter(date_publish__contains = archives_date).order_by('-date_publish')
    else:
        articles = Article.objects.filter((category__name) = cate).order_by('-date_publish')

    paginator = Paginator(articles,5)

    try:
        #获取用户当前页面,这里的http://127.0.0.1:8000/blog/?page=2,>?page=是页面参数

        page = int(request.GET.get('page',1))
        #根据页面(数字),得到当前页的(数据)
        articles = paginator.page(page)
    except (EmptyPage,InvalidPage,PageNotAnInteger):
        #出现异常,默认显示第一页的数据
        articles = paginator.page(1)

    #可以使用locals()函数将方法中的所有变量都传递到render的模板中
    return render(request,'blog.html',locals())





#航海日志
'''
方法和上面的blog一样,只是简化了功能
功能栏目:
最近一周
最近一月
按照年归档,年里面有按月份
'''
def logEntry(request):


    #归档
    sql = "SELECT DATE_FORMAT(date_publish,'%Y') From blog_logentry ORDER BY  blog_logentry.date_publish DESC;"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    s = set(rows)
    archives = {}
    for x in s:
        #count = len(Article.objects.filter(date_publish__contains=x[0]))
        count = LogEntry.objects.filter(date_publish__contains=x[0]).values('date_publish').count()
        archives.setdefault(x[0],count)




    archives_year = request.GET.get('archive','')
    month = request.GET.get('monthly','')
    print("************archives_year %s  month %s" %(archives_year,month))
    log_id = request.GET.get('id','')
    #根据get参数赋值
    if log_id != '':
        articles = LogEntry.objects.filter(id=int(log_id))
    elif archives_year == '' and month == '':
        articles = LogEntry.objects.order_by('-date_publish')[0:7]

    elif archives_year != '' and month == '':
        articles = LogEntry.objects.filter(date_publish__contains = archives_year).order_by('-date_publish')
    elif month != '' and month !='onemonth':
        #查找的格式是: year-month
        year_month = archives_year +'-'+month
        articles = LogEntry.objects.filter(date_publish__contains = year_month).order_by('-date_publish')[0:30]
        print('年 + 月 : %s' %year_month)
    else:
        articles = LogEntry.objects.order_by('-date_publish')[0:30]

    paginator = Paginator(articles,5)

    try:
        #获取用户当前页面,这里的http://127.0.0.1:8000/blog/?page=2,>?page=是页面参数

        page = int(request.GET.get('page',1))
        #根据页面(数字),得到当前页的(数据)
        articles = paginator.page(page)
    except (EmptyPage,InvalidPage,PageNotAnInteger):
        #出现异常,默认显示第一页的数据
        articles = paginator.page(1)
    return render(request,'logentry.html',locals())




#关于我的介绍
def aboutMe(request):
    return render(request,'about.html')


#留言界面
def contactMe(request,success=False):
    return render(request,'contact.html',{'success':success})
#发送邮件 利用python库
def sendEmail(request):
    print('**************运行了sendemail*********************')
    if request.method =='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            f = form.clean() #clean(方法将所有form成员变成字典)
            print('name:'+f['name'])
            print('subject:'+f['subject'])
            print('email:'+f['email'])

            print('comments:'+f['comments'])
            sendContactEmail(f['name'],f['email'],f['subject'],f['comments'])

    #django 自带发送还没成功,慢慢琢磨吧
    #send_mail('test','this is the django mail','clover_duo@126.com',['captain2conner@yahoo.com'],fail_silently=True)
    return render(request,'contact.html',{'success':True})

#测试,博客的方法
#//////////////////////
def writeblog(request):
    return render(request,'writeblog.html')
#新建存储的路径
def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)

#根据路径存储图片
def save_file(path,file_name,data):
    if data == None:
        return
    mkdir(path)
    if(not path.endswith("/")):
        path = path +'/'
        file = open(path+file_name,"wb")
        file.write(data)
        file.flush()
#上传图片
@csrf_exempt
def uploadImg(request):
    if request.method == 'POST':

        #从request获取文件上传的文件数据
        buf = request.FILES.get('imgFile',None)                                   #获取的图片文件
        file_buff = buf.read()
        #按时间新建文件名字
        time_format=str(time.strftime("%Y-%m-%d-%H%M%S",time.localtime()))
        file_name = "img"+time_format+".jpg"
        #参数是 (存储路路径,文件名,文件数据)
        #需要添加完实时现实,要在url中对存储路径添加规则,方便处理.url(r'^uploads/(?P<path>.*)$'
        save_file("uploads/image", file_name,file_buff)

        dict_tmp = {}
        dict_tmp['error']=0
        dict_tmp['url']="/uploads/image/"+file_name
        return HttpResponse(json.dumps(dict_tmp))

#/////////////////////// rest
#具体rest页面的显示内容, 1 数据源 2 序列化显示的东西 3 权限
from django.contrib.auth.models import User
from blog.serializers import *
from rest_framework import permissions, viewsets, renderers
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = Userserializer
    permission_classes = (permissions.IsAuthenticated,)

class LogEntryViewSet(viewsets.ModelViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)



#手机网页
def app(request):
    return render(request,'app.html')
