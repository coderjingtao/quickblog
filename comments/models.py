from django.db import models

class Comment(models.Model):
    name = models.CharField(max_length=100) # username
    email = models.EmailField(max_length=255) # email address
    url = models.URLField(blank=True) # personal website address
    text = models.TextField() # comment content
    created_time = models.DateTimeField(auto_now_add=True) # comment time

    #relationship with Article: Many to One
    article = models.ForeignKey('blog.Article',on_delete=models.PROTECT)

    objects = models.Manager()

    def __str__(self):
        return self.text