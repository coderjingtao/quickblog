from django.contrib.syndication.views import Feed
from .models import Article

class ArticlesRssFeed(Feed):
    title = "Jingtao's Blog"
    link = "/"
    description= "Welcome to Jingtao's Blog"
    # displayed items on RSS Reader
    def items(self):
        return Article.objects.all()
    # displayed titles of items on RSS Reader
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)
    # displayed descriptions of items on RSS Reader
    def item_description(self, item):
        return item.body