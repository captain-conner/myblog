"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
#django内建的处理图像的方法
from django.views.static import serve
from django.conf import settings
from blog.views import *


#rest framework 用到的
from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter


# rest 设置
user_list = UserViewSet.as_view({'get': 'retrieve'})
#logentry_detail = LogEntryViewSet.as_view({'get': 'list'})
#logentry_detail = LogEntryViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy','post':'create'})
logentry_detail = LogEntryViewSet.as_view({'get':'retrieve'})
router = DefaultRouter()
router.register(r'logentrys',LogEntryViewSet)
router.register(r'users',UserViewSet)



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #上传文件地址 传递的参数是path 和默认的参数 document_root
    #url(r'^uploads/(?P<path>.*)$','django.views.static.serve',{"document_root":settings.MEDIA_ROOT,}),
    #博客的主要地址
    url(r'^$',index),
    url(r'^blog/$',blog),
    #这里的id要制定数据类型比如 \d说明是数字,不制定,会匹配不到的(地址已非处,优化了)
    #url(r'^blog/detail/(?P<id>\d+)/$',blog_detail),
    url(r'^logentry/$',logEntry),

    url(r'^about/$',aboutMe),
    url(r'contact/$',contactMe),
    url(r'sendemail/$',sendEmail),

    url(r'^blog_add/$',writeblog,name='blog_add'),
    url(r'^uploadimg/$',uploadImg,name='uploadImg'),
    #实现图片富编辑器的实时预览
    url(r'^uploads/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT,}),
    #管理员中的富编辑器图片显示处理地址.
    url(r'^admin/blog/article/*/change/admin/upload/kindeditor/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT,}),


    #rest 地址和配置
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^users/$', user_list, name='user-list'),

    #url(r'^logentrys/$', logentry_detail, name='logentry_detail'),
    #这里是实现update好的delete必须的，因为update和delete要传递pk码，as_vie函数处理pk码才能删除和更新数据，记住了。
    url(r'^logentrys/(?P<pk>[0-9]+)/$', logentry_detail, name='logentry_detail'),

    #手机网页
    url(r'^app/$', app),

]
