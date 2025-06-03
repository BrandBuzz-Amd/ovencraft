from django.shortcuts import render, get_object_or_404
from .models import Blog

def index(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-created_at')
    context = {
        'blogs': blogs,
        'title': 'Blogs',
    }
    return render(request, 'blogs.html', context)

def detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    # Fetch related posts, popular posts, categories, tags as needed
    related_posts = Blog.objects.filter(is_published=True).exclude(id=blog.id)[:3]
    popular_posts = Blog.objects.filter(is_published=True).order_by('-views')[:5]
    categories = []  # Add category fetching logic if applicable
    tags = []  # Add tag fetching logic if applicable
    prev_blog = Blog.objects.filter(is_published=True, created_at__lt=blog.created_at).order_by('-created_at').first()
    next_blog = Blog.objects.filter(is_published=True, created_at__gt=blog.created_at).order_by('created_at').first()
    context = {
        'blog': blog,
        'related_posts': related_posts,
        'popular_posts': popular_posts,
        'categories': categories,
        'tags': tags,
        'prev_blog': prev_blog,
        'next_blog': next_blog,
    }
    return render(request, 'blog_detail.html', context)
