import markdown
from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from comments.forms import CommentForm

def article_list(request):
    article_list = Article.objects.all()
    return render(request, 'blog_list.html', context={'title':'Jingtao Blog List','article_list':article_list})

def article_detail(request,id):
    article =  get_object_or_404(Article, pk=id)
    # make article body to support markdown language
    article.body = markdown.markdown(article.body,extensions=['markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',] )
    form = CommentForm()
    #get all the comments of this article
    comment_list = article.comment_set.all() # == Comment.objects.filter(article=article)
    # pass article, form and comments to render the detail page
    context = {'title':article.title,'article':article,'form':form,'comment_list':comment_list}
    return render(request, 'blog_content.html', context=context)

def category(request,id):
    category = get_object_or_404(Category, pk=id)
    article_list = Article.objects.filter(category=category)
    return render(request, 'blog_list.html',context={'title':category.name+' BLOG LIST','article_list':article_list})

