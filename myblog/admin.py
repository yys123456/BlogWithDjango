from django.contrib import admin
from .models import Article,Tag,Category,BgImgs,Comments
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'user', 'views','comment','created_time','post')
    # 文章列表里显示想要显示的字段
    list_per_page = 30
    # 满50条数据就自动分页
    ordering = ('-created_time',)
    #后台数据列表排序方式
    list_display_links = ('id', 'title')
    # 设置哪些字段可以点击进入编辑界面
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index')
    list_per_page = 30
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_per_page = 30

@admin.register(BgImgs)
class BgImgsAdmin(admin.ModelAdmin):
	list_display = ('id','image','upload_time')
	list_per_page = 30
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name','content','comment_time','article_id')
    list_per_page = 50