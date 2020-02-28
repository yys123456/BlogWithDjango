from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User 
from DjangoUeditor.models import UEditorField #头部增加这行代码导入UEditorField
from mdeditor.fields import MDTextField
#导入Django自带用户模块

#标签
class Tag(models.Model):
    name = models.CharField('标签',max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "tags"
        verbose_name = '标签'
        verbose_name_plural = verbose_name

# 文章分类
class Category(models.Model):
    name = models.CharField('文章分类', max_length=100)
    index = models.IntegerField(default=999, verbose_name='分类排序')

    class Meta:
        db_table = "categories"
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#文章
class Article(models.Model):
    title = models.CharField('标题', max_length=70)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='分类', blank=True, null=True)
     #使用外键关联分类表与分类是一对多关系
    tags = models.ManyToManyField(Tag,verbose_name='标签', blank=True)
    comment = models.IntegerField(default=0,verbose_name='评论数')
    #使用外键关联标签表与标签是多对多关系
    # body = UEditorField('内容', width=800, height=500, 
    #                 toolbars="full", imagePath="upimg/", filePath="upfile/",
    #                 upload_settings={"imageMaxSize": 1204000},
    #                 settings={}, command=None, blank=True
    #                 )
    #此处文章上传图片未设定路径
    post = models.ImageField(upload_to='posts')
    body = MDTextField(
        )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    views = models.PositiveIntegerField('阅读量', default=0)
    
    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = "articles"
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.title

class BgImgs(models.Model):
    image = models.ImageField(upload_to="bg")
    upload_time = models.DateTimeField('上传时间',auto_now_add=True)
    class Meta:
        db_table = "bgImgs"
        verbose_name = '背景图片'
        verbose_name_plural = verbose_name

class Comments(models.Model):
    name = models.CharField('评论者标识',max_length=20)
    content = models.CharField('评论内容',max_length=1000)
    comment_time = models.DateTimeField('评论时间',auto_now_add=False)
    article = models.ForeignKey('Article',on_delete=models.CASCADE)
    class Meta:
        db_table = "comments"
        verbose_name = '评论'
        verbose_name_plural = verbose_name
