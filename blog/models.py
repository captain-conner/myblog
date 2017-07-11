from django.db import models

from django.core.urlresolvers import reverse
# Create your models here.


# 用户,
# user表采用数据库默认的表格,导入的是项目的默认用户数据表
from django.contrib.auth.models import AbstractUser

# 这个是继承了django默认用户数据表的类
#参数 verbose_name 就是admin的页面标题
#file 类的一些参数
#verbose_name=None   #显示名
'''
verbose_name=None   #显示名
name=None           #域名
primary_key=False   #是否为主键
max_length=None     #在CharFiled中用到
unique=False        #是否唯一
blank=False
null=False          #是否允许为空
db_index=False
rel=None
default=NOT_PROVIDED
editable=True       #是否可编辑
serialize=True
unique_for_date=None
unique_for_month=None
unique_for_year=None
choices=None
help_text=''
db_column=None
db_tablespace=None
auto_created=False
validators=[]
error_messages=None
'''

class User(AbstractUser):
    #头像图片
    painted = models.ImageField(verbose_name="头像",upload_to='photos/%Y/%m/%d',blank=True,null=True)
    def show(self):
        return 'detail'



# 标签
class Tag(models.Model):
    name = models.CharField(max_length=30,verbose_name='标签名')

    def __str__(self):
        return self.name

# 分类
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名')
    index = models.IntegerField(default=999, verbose_name='分类索引')
    def __str__(self):
        return self.name


#文章
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=50, verbose_name='摘要')
    content = models.TextField(verbose_name='内容')
    click_count = models.IntegerField(default=0, verbose_name='点击数量')
    likes = models.IntegerField(default=0, verbose_name='点赞')
    is_recommend = models.BooleanField(default=False, verbose_name='推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发表时间')
    modified_time = models.DateTimeField(
        auto_now_add=True, verbose_name='最近修改时间')
    # 文章的外键
    user = models.ForeignKey(User, verbose_name='发布者')
    category = models.ForeignKey(Category,blank=True,null=True,verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    # 根据查找到的文章生成具体访问文章的地址 逆向查询方法get_absolute_url
    # 后面再实现

#航海日志(可以是文字和图片)
class LogEntry(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')
    #user = models.ForeignKey(User, verbose_name='发布者')
# 评论
class Blog_Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    # 外键

    user = models.ForeignKey(User, blank=True, null=True, verbose_name='评论者',)
    article = models.ForeignKey( Article,blank=True,null=True,verbose_name='评论的文章')
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='上级评论')

#航海日志
