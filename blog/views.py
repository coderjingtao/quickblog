from django.shortcuts import render, get_object_or_404
from .models import Article, Category, Tag
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView

import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

class ArticleListView(ListView):
    model = Article
    template_name = 'blog_list.html'
    context_object_name = 'article_list'
    paginate_by = 3
    title = 'Jingtao Blog List'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # paginate attributes
        paginator =  context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        # invoke customized my_pagination()
        paginate_data = self.my_pagination(paginator,page,is_paginated)
        context.update(paginate_data)
        context.update({'title':self.title})
        return context

    def my_pagination(self,paginator,page,is_paginated):
        if not is_paginated:
            return {}
        range_num = 2
        left_of_current = []
        right_of_current = []
        left_has_more = False
        right_has_more = False
        display_first = False
        display_last = False
        current_page_no = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if current_page_no == 1:
            right_of_current = page_range[1:1+range_num]
            if right_of_current[-1] < total_pages -1:
                right_has_more = True
            if right_of_current[-1] < total_pages:
                display_last = True
        elif current_page_no == total_pages:
            left_of_current = page_range[-1-range_num:-1]
            if left_of_current[0] > 2:
                left_has_more = True
            if left_of_current[0] > 1:
                display_first = True
        else:
            right_of_current = page_range[current_page_no:current_page_no+range_num]
            left_of_current = page_range[-total_pages+current_page_no-range_num-1:-total_pages+current_page_no-1]
            if right_of_current[-1] < total_pages -1:
                right_has_more = True
            if right_of_current[-1] < total_pages:
                display_last = True
            if left_of_current[0] > 2:
                left_has_more = True
            if left_of_current[0] > 1:
                display_first = True
        
        ret = {
            'left': left_of_current,
            'right': right_of_current,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':display_first,
            'last':display_last,
        }
        return ret

"""
def article_list(request):
    article_list = Article.objects.all()
    return render(request, 'blog_list.html', context={'title':'Jingtao Blog List','article_list':article_list})
"""

class CategoryView(ArticleListView):
    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        self.title = category.name + ' BLOG LIST'
        return super(CategoryView,self).get_queryset().filter(category=category)
"""
def category(request,id):
    category = get_object_or_404(Category, pk=id)
    article_list = Article.objects.filter(category=category)
    return render(request, 'blog_list.html',context={'title':category.name+' BLOG LIST','article_list':article_list})
"""

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog_content.html'
    context_object_name = 'article'
    
    #override get() to increase the number of browsing article 
    def get(self,request,*args,**kwargs):
        response = super(ArticleDetailView,self).get(request,*args,**kwargs)
        self.object.add_views()
        return response

    #override get_object() to render article body to support markdown language
    def get_object(self, queryset=None):
        article = super(ArticleDetailView,self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        article.body = md.convert(article.body)
        article.toc = md.toc
        return article

    #override get_context_data() to pass other objects to template such as form and comments except article (defined above)
    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({'form':form,'comment_list':comment_list,'title':self.object.title})
        return context
"""
def article_detail(request,id):
    article =  get_object_or_404(Article, pk=id)
    # increase the number of article views
    article.add_views()
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
"""

class TagView(ArticleListView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        self.title = tag.name + ' BLOG LIST'
        return super(TagView,self).get_queryset().filter(tags=tag)
