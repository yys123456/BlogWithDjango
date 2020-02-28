from django.urls import path
from myproject import settings 
from . import views
app_name="blog"
urlpatterns = [
	path('test/',views.test,name='test'),
    path('index/',views.index,name='index'),
    # path('category/<int:category>',views.getArticlesByCate,name='category'),
    path('category/<int:category_id>',views.getArticlesIdByCate,name="category"),
    path('getArticle/',views.getArticleById,name="getArticleById"),
    path('article/<int:article_id>',views.readArticle,name='article'),
    path('advice/',views.advice,name="advice"),
    path('l4d2/',views.l4d2,name="l4d2"),
    path('message/',views.message,name="message"),
    path('search/',views.search,name="search"),
    path('tag/<int:tag_id>',views.getArticlesIdByTag,name="tag"),
    path('about/',views.about,name="about"),
    path('getAsc/',views.getAsc,name="getAsc")
]

