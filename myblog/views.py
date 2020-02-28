from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import Article,Category,BgImgs,Comments,Tag
from django.forms.models import model_to_dict
import json
import markdown
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime,timedelta
# from smtplib import SMTP_SSL
from smtplib import SMTP_SSL
from PIL import Image
from random import randint
import os
from copy import deepcopy
import re

def message(request):
    article_id=request.POST.get('article_id')
    name=request.POST.get('name')
    comment=request.POST.get('comment')
    comment_time=request.POST.get('comment_time')
    # comment_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    Comments.objects.create(name=name,content=comment,article_id=article_id,comment_time=comment_time)
    # ret={
    # 'name':name,
    # 'comment':comment,
    # 'comment_time':comment_time,
    # }
    return JsonResponse(1,safe=False)

def handler404(request,exception,template_name="myblog/rsblock.html"):
    return render(request,template_name,{"error":404})

def handler500(request):
    return render(request,"myblog/rsblock.html",{"error":500})
def test(request):
    name=request.GET.get('id')
    # year=request.GET.get('year')
    return HttpResponse(name)

def base_gen():
    categories=Category.objects.raw("select b.id as id,b.name as name, count(*) as sum\
        from articles a,categories b \
        where a.category_id=b.id\
        group by b.name\
        order by sum desc")
    bgs=BgImgs.objects.raw("select id,image as url from bgimgs")
    tags=Tag.objects.raw("select a.id as id,name,count(*) as sum from\
                            tags a,articles_tags b\
                             where a.id=b.tag_id\
                             group by name\
                             order by sum desc\
                             ")
    context={
        'categories': categories,
        'backgrounds':[i.url for i in bgs],
        'tags':tags,
    }
    return context

def index(request):
    context={
        'baseContext':base_gen(),
    }
    response=render(request,"myblog/index.html",context)
    return response

def getArticlesIdByCate(request,category_id):
    article_ids = Article.objects.values("id").filter(category_id=category_id)
    category_name=Category.objects.values("name").filter(id=category_id).first()['name']
    context={
        'baseContext':base_gen(),
        "article_ids":list(article_ids),
        "category_name":category_name,
    }
    return render(request,"myblog/list.html",context)

def getTagsOfArticle(article_id):#返回字典数组
    tags=Tag.objects.raw(
        "select a.id as Tag_id, a.name as Tag_name,b.id\
         from tags a, articles b, articles_tags c\
         where a.id=c.tag_id and b.id=c.article_id and b.id=%s\
        ",[article_id])
    ret=[]
    for tag in tags:
        dc={}
        dc['Tag_id']=tag.Tag_id
        dc['Tag_name']=tag.Tag_name
        ret.append(dc)
    return ret

def getArticleById(request):
    article_id=request.POST.get('article_id')
    # print(article_id)
    #使用id查询文章的相关信息
    articles=Article.objects.raw(
        "select a.*,b.name as category_name \
        from articles a,categories b\
        where a.category_id=b.id and a.id=%s",[article_id])
    # values().filter(id=article_id).first()
    # print(type(article))
    # _data=article
    # # print(type(_data))
    # _data['post']=str(_data['post'])
    # _data['body']=markdown.markdown(_data['body'],
    #         extensions=[
    #                          'markdown.extensions.extra',
    #                          'markdown.extensions.codehilite',
    #                          'markdown.extensions.toc',
    #                 ]
    #     )
    # _data['created_time']=_data['created_time'].strftime('%Y-%m-%d')
    # _data['modified_time']=_data['modified_time'].strftime('%Y-%m-%d')
    # _data['tag_info']=getTagsOfArticle(article_id)
    # print(type(_data))
    _data={}
    for article in articles:
        _data['id']=article.id
        _data['title']=article.title
        _data['comment']=article.comment
        _data['views']=article.views
        _data['category_id']=article.category_id
        _data['category_name']=article.category_name
        _data['post']=str(article.post)
        _data['body']=markdown.markdown(article.body,
                extensions=[
                                 'markdown.extensions.extra',
                                 'markdown.extensions.codehilite',
                                 'markdown.extensions.toc',
                        ]
            )
        _data['created_time']=article.created_time.strftime('%Y-%m-%d')
        _data['modified_time']=article.modified_time.strftime('%Y-%m-%d')
        _data['tag_info']=getTagsOfArticle(article_id)
    return JsonResponse(_data)

def getArticlesByCate(request,category):
    articles = Article.objects.values().filter(category_id=category)
    category_name = Category.objects.filter(id=category).first().name
    bookList=list(articles)
    for i in bookList:
        i['created_time']=i['created_time'].strftime('%Y-%m-%d')
        i['modified_time']=i['modified_time'].strftime('%Y-%m-%d')
        i['body']=markdown.markdown(i['body'],
            extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                     # 'markdown.extensions.math'
                    ]
        )
    # for i in bookList:
    #     print(i['created_time'])
    context={
        'baseContext':base_gen(),
        'articles':bookList,
        'category': categoryName,
    }
    return render(request,"myblog/list.html",context)

def getArticlesIdByTag(request,tag_id):
    query = Tag.objects.raw(
                "select a.id as article_id,b.id\
                from articles a, tags as b, articles_tags as c\
                where a.id=c.article_id and b.id=c.tag_id and b.id=%s\
                ",[tag_id])
    tag_name=Tag.objects.values('name').filter(id=tag_id).first()['name']
    article_ids=[]
    for i in query:
        dc={}
        dc['id']=i.article_id
        article_ids.append(dc)
    context={
        'baseContext':base_gen(),
        "article_ids":article_ids,
        "tag_name":tag_name,
    }
    return render(request,"myblog/tag.html",context)

def getArticleByTag(request,tag_id):
    tagname=Tag.objects.values('name').filter(id=tag).first()['name']
    articles=Article.objects.raw("select a.*,b.id as tid,d.name as cname\
                            from articles a,tags b,articles_tags c,categories d\
                            where a.id=c.article_id and b.id=c.tag_id\
                            and a.category_id=d.id\
                            and c.tag_id=%s",[tag_id])
    articles_tag=[]
    data=[]
    for article in articles:
        tmp=Article.objects.raw("select name,a.id as id from tags a,articles_tags b where b.article_id=%s and a.id=b.tag_id",[article.id])
        _data={}
        _data['id']=article.id
        _data['title']=article.title
        _data['comment']=article.comment
        _data['post']=str(article.post)
        _data['body']=article.body
        _data['views']=article.views
        _data['created_time']=article.created_time.strftime('%Y-%m-%d')
        _data['modified_time']=article.modified_time.strftime('%Y-%m-%d')
        _data['category_id']=article.category_id
        # _data['user_id']=article.user_id
        _data['cname']=article.cname
        data.append(_data)
        t=[]
        for i in tmp:
            ap={}
            ap['tname']=i.name
            ap['id']=i.id
            t.append(ap)
        articles_tag.append(t)
    context={
        'baseContext':base_gen(),
        'data':data,
        'tagInfo':articles_tag,
        'tag':tagname,
    }
    return render(request,"myblog/tag.html",context)


def readArticle(request,article_id):

    article = Article.objects.filter(id=article_id).first()
    # print(article.body)
    comments = Comments.objects.values("name","content","comment_time").filter(article_id=article_id)
    commentsList=list(comments)
    article.body=markdown.markdown(article.body,
            extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                    ]
        ).replace("\n",'<br>')
    # print(article.body)
    for i in commentsList:
        i['comment_time']=i['comment_time'].strftime('%Y-%m-%d %H:%M:%S')
    context={
        'baseContext':base_gen(),
        'article':article,
        'comments':commentsList,
    }
    response=render(request,"myblog/article.html",context)
    if request.COOKIES.get(str(article_id),None)==None:
        #增加一次浏览量
        art_obj=Article.objects.get(id=article_id)
        art_obj.views+=1
        art_obj.save()
        response.set_cookie(str(article_id),'1',expires=datetime.now()+timedelta(0.1))
    return response


def advice(request):
    sender=request.POST.get('sender')
    adv=request.POST.get('advice')
    adcode=request.POST.get('adcode')
    host_server = 'smtp.qq.com'
    receiver='l4d2server_admin@126.com'#我的邮箱189300944@qq.com
    mail_content="<strong>发送者：</strong>"+sender+"<br>"+"<p><b>建议：</b>"+adv+"</p>"
    mail_title="l4d2意见信息@"+sender
    # smtp = smtplib.SMTP()
    # smtp.connect(host_server)
    smtp = SMTP_SSL(host_server)
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    # smtp.starttls()
    smtp.login(sender, adcode)
    msg = MIMEText(mail_content, "html", 'utf-8')
    msg["Subject"] = mail_title
    msg["From"] = sender
    msg["To"] = receiver
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    smtp.close()
    return HttpResponse("success！")
def l4d2(request):
    return render(request,"myblog/l4d2.html",{})

def search(request):
    keyWords=request.POST.get('keyWords').split(' ')
    # ,title,body,created_time,name as cname,post,views,comment,category_id 
    sql="select a.id as id from articles a, categories b where a.category_id=b.id and "
    title=""
    body=""
    lt=len(keyWords)
    for i in range(0,lt):
        if keyWords[i]=='':
            continue
        title=''.join([title,"title like '%",keyWords[i],"%'"])
        body=''.join([body,"body like '%",keyWords[i],"%'"])
        if i<lt-1:
            title=' '.join([title,'or '])
            body=' '.join([body,'or '])
    sql=' '.join([sql,title,'or',body])
    # print(sql)
    articles=Article.objects.raw(sql)
    _data=[]
    for article in articles:
        dc={}
        dc['id']=article.id
        _data.append(dc)
    # print(articles[0])
    # data=serialize(articles)
    # print(data)
    return JsonResponse(_data,safe=False) #,safe=False

def getAsc(request):
    return JsonResponse(Asc_gen(25,6),safe=False)

def about(request):
    context={
        'baseContext':base_gen(),
    }
    # print (os.getcwd()) #打印出当前工作路径
    return render(request,"myblog/about.html",context)

ascii_char=list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
def Asc_gen(w,h):
    IMG=".\\myblog\\static\\myblog\\img\\head.png"
    length=len(ascii_char)
    im = Image.open(IMG)
    im = im.resize((w,h), Image.NEAREST)
    txt=""
    for i in range(h):
        for j in range(w):
            cr=ascii_char[randint(0,length-1)]
            color=list(im.getpixel((j,i)))
            if len(color)==4:
                color[3]/=255
            else:
                if color[0]==color[1] and color[1]==color[2] and color[2]==255:
                    cr='&nbsp;&nbsp'
                color.append(1)

            txt = ''.join([txt,"<span style='color:rgba("+str(color[0])+","+str(color[1])+","+str(color[2])+","+str(color[3])+")'>"+cr+"</span>"])
        txt+='<br />'
    # print(txt)
    return txt
