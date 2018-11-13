from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path("",views.ArticleListView.as_view(),name="index"), 
    path("detail/<int:pk>",views.ArticleDetailView.as_view(),name='detail'), # [name] value must be pk if using class generic view
    path("category/<int:pk>",views.CategoryView.as_view(),name="category"), # [name] value must be consistent with views.py
    path("tag/<int:pk>",views.TagView.as_view(),name="tag"), # [name] value must be consistent with views.py
]