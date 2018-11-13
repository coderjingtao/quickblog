from django import template
from ..models import Article, Category, Tag
from django.db.models.aggregates import Count

register = template.Library()

# use method name to register a tag name, so that template pages can import {% get_recent_article %} to use it
@register.simple_tag
def get_recent_article(num=3):
    return Article.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def get_categories():
    #return Category.objects.all()
    # for count the total number of articles under each category
    return Category.objects.annotate(num_articles = Count('article')).filter(num_articles__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_articles = Count('article')).filter(num_articles__gt=0)

