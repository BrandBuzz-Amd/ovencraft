from django.shortcuts import render
from blog.models import Blog
from gallery.models import GalleryItem

def index(request):
    recent_posts = Blog.objects.filter(is_published=True).order_by('-created_at')[:3]
    gallery_items = GalleryItem.objects.all().order_by('-created_at')[:6]

    return render(request, 'home.html', {
        'title': 'Home',
        'recent_posts': recent_posts,
        'gallery_items': gallery_items,
        'current_user': request.user if request.user.is_authenticated else None,
        'is_authenticated': request.user.is_authenticated
    })

def about(request):
    return render(request, 'about.html', {
        'title': 'About Us',
        'current_user': request.user if request.user.is_authenticated else None,
        'is_authenticated': request.user.is_authenticated
    })

def products(request):
    return render(request, 'products.html', {
        'title': 'Products',
        'current_user': request.user if request.user.is_authenticated else None,
        'is_authenticated': request.user.is_authenticated
    })

def faq(request):
    return render(request, 'faq.html', {
        'title': 'FAQ',
        'current_user': request.user if request.user.is_authenticated else None,
        'is_authenticated': request.user.is_authenticated
    })

def privacy_policy(request):
    return render(request, 'privacy_policy.html', {
        'title': 'Privacy Policy',
        'current_user': request.user if request.user.is_authenticated else None,
        'is_authenticated': request.user.is_authenticated
    })

def product_details(request):
    return render(request, 'product-details.html', {
        'title': 'Product Details',
        'current_user': request.user if request.user.is_authenticated else None,
        'is_authenticated': request.user.is_authenticated
    })
