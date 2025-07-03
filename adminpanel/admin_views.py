from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import json

from product.models import Product, ProductCategory
from blog.models import Blog, BlogCategory
from gallery.models import GalleryItem, GalleryCategory
from users.models import User
from contact.models import Contact, VisitorTracking, Newsletter

@staff_member_required
def admin_dashboard(request):
    # Get counts for dashboard
    product_count = Product.objects.count()
    blog_count = Blog.objects.count()
    gallery_count = GalleryItem.objects.count()
    user_count = User.objects.count()
    contact_count = Contact.objects.count()
    newsletter_count = Newsletter.objects.filter(is_active=True).count()
    
    # Get visitor statistics
    visitor_stats = VisitorTracking.get_visitor_stats()
    
    # Get recent items
    recent_products = Product.objects.order_by('-created_at')[:5]
    recent_blogs = Blog.objects.order_by('-created_at')[:5]
    recent_gallery = GalleryItem.objects.order_by('-created_at')[:5]
    recent_contacts = Contact.objects.order_by('-created_at')[:5]
    
    # Get visitor analytics data for charts
    device_stats = (VisitorTracking.objects
        .values('device_type')
        .annotate(count=Count('id'))
        .order_by('-count'))
    
    browser_stats = (VisitorTracking.objects
        .values('browser')
        .annotate(count=Count('id'))
        .order_by('-count'))
    
    # Get page visit statistics
    page_stats = (VisitorTracking.objects
        .values('page_visited')
        .annotate(count=Count('id'))
        .order_by('-count')[:10])
    
    # Get daily visitor trend for the last 7 days
    daily_visitors = []
    for i in range(7):
        date = timezone.now().date() - timedelta(days=i)
        count = VisitorTracking.objects.filter(visited_at__date=date).values('ip_address').distinct().count()
        daily_visitors.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    daily_visitors.reverse()
    
    context = {
        'product_count': product_count,
        'blog_count': blog_count,
        'gallery_count': gallery_count,
        'user_count': user_count,
        'contact_count': contact_count,
        'newsletter_count': newsletter_count,
        'visitor_stats': visitor_stats,
        'recent_products': recent_products,
        'recent_blogs': recent_blogs,
        'recent_gallery': recent_gallery,
        'recent_contacts': recent_contacts,
        'device_stats': json.dumps(list(device_stats)),
        'browser_stats': json.dumps(list(browser_stats)),
        'page_stats': json.dumps(list(page_stats)),
        'daily_visitors': json.dumps(daily_visitors),
    }
    
    return render(request, 'admin/index.html', context)
