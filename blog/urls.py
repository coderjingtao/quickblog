from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path("",views.article_list,name="index"), 
    path("detail/<int:id>",views.article_detail,name='detail'),
    path("category/<int:id>",views.category,name="category"),
]