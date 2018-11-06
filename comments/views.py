from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Article
from .forms import CommentForm

def post_comment(request,article_id):
    # get the article that users will make a comment
    article = get_object_or_404(Article, pk=article_id)
    # only when the request is post, handle comment form from page
    if request.method == 'POST':
        # get one instance of CommentForm via POST 
        form = CommentForm(request.POST)
        # Django will check data format in form automatically
        if form.is_valid():
            # get one instance of Comment but has not saved into database yet
            comment = form.save(commit=False)
            # correlate the article of comment  
            comment.article = article
            # save commnet to database
            comment.save()
            # it will invoke get_absolute_url() method in Article Model and return 
            return redirect(article)
        # data in form is not valid
        else:
            # == Comment.objects.filter(article=article)
            comment_list = article.comment_set.all() 
            context = {'title':article.title,'article':article,'form':form,'comment_list':comment_list}
            return render(request,'blog_content.html',context = context)
    return redirect(article)