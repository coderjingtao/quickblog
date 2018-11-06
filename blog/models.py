from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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

    class Meta:
        ordering = ['-created_time']
