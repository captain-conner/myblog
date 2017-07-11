from django.contrib import admin
from blog.models import *
# Register your models here.

#文本编辑器


#设置要显示的东西
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email')



class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
   # list_display要显示的东西
   # list_display_links 是否可一点击链接
   # list_filter()添加过滤器
   #


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','index')

class ArticleAdmin(admin.ModelAdmin):
   list_display = ('user','category','title')
   #要使用富编辑器,需要在admin.py中添加Media类,指定地址

   class Media:
       js = (
               '/static/js/kindeditor-4.1.10/kindeditor-all.js',
               '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
               '/static/js/kindeditor-4.1.10/config.js',
           )


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('date_publish','title')
    class Media:
        js = (
                '/static/js/kindeditor-4.1.10/kindeditor-all.js',
                '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
                '/static/js/kindeditor-4.1.10/config.js',
            )



class Blog_CommentAdmin(admin.ModelAdmin):
    list_display = ('article','user','date_publish')

#先添加一些管理表的界面,加入测试的数据
admin.site.register(User,UserAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Blog_Comment,Blog_CommentAdmin)
admin.site.register(LogEntry,LogEntryAdmin)
