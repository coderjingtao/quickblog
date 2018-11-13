import markdown
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags

# Model must inherit models.Model

# Aricle Category
class Category(models.Model):
    name = models.CharField(max_length=100)
    objects = models.Manager()

    def __str__(self):
        return self.name

# Aricle Tag
class Tag(models.Model):
    name = models.CharField(max_length=100)
    objects = models.Manager()

    def __str__(self):
        return self.name

# Aricle published
class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    summary = models.CharField(max_length=200, blank=True)
    views = models.PositiveIntegerField(default=0)
    # Relationships with other classes
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag,blank=True)
    author = models.ForeignKey(User,on_delete=models.PROTECT)
    objects = models.Manager()
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.pk)])

    def add_views(self):
        self.views +=1
        self.save(update_fields=['views'])
    
    #override save() of Model for generating article summary
    def save(self, *args, **kwargs):
        if not self.summary:
            # instantiate a markdown class
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # md converts article body into HTML
            # stripe_tags clean up all the HTML tags
            self.summary = strip_tags(md.convert(self.body))[:54]
        # invoke save() in its parent class to save it into database 
        super(Article,self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']
