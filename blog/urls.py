from django.urls import path
from .views import index, detail

urlpatterns = [
    path('', index, name='blogs'),
    path('<slug:slug>/', detail, name='blog_detail'),
]
