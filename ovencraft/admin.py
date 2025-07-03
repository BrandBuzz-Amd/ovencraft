from django.contrib import admin
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import json

class CustomAdminSite(admin.AdminSite):
    site_header = 'OvenCraft Admin'
    site_title = 'OvenCraft Admin Portal'
    index_title = 'Welcome to OvenCraft Administration'

    def index(self, request, extra_context=None):
        """
        Display the main admin index page with custom dashboard.
        """
        try:
            from product.models import Product, ProductCategory
            from blog.models import Blog, BlogCategory
            from gallery.models import GalleryItem, GalleryCategory
            from users.models import User
            from contact.models import Contact, VisitorTracking, Newsletter
            
            # Get counts for dashboard with safe defaults
            product_count = Product.objects.count() if Product.objects.exists() else 0
            blog_count = Blog.objects.count() if Blog.objects.exists() else 0
            gallery_count = GalleryItem.objects.count() if GalleryItem.objects.exists() else 0
            user_count = User.objects.count() if User.objects.exists() else 0
            contact_count = Contact.objects.count() if Contact.objects.exists() else 0
            newsletter_count = Newsletter.objects.filter(is_active=True).count() if Newsletter.objects.exists() else 0
            
            # Get visitor statistics with safe defaults
            try:
                visitor_stats = VisitorTracking.get_visitor_stats()
            except:
                visitor_stats = {'today': 0, 'week': 0, 'month': 0, 'total': 0}
            
            # Get recent items with safe defaults
            recent_products = list(Product.objects.order_by('-created_at')[:5]) if Product.objects.exists() else []
            recent_blogs = list(Blog.objects.order_by('-created_at')[:5]) if Blog.objects.exists() else []
            recent_gallery = list(GalleryItem.objects.order_by('-created_at')[:5]) if GalleryItem.objects.exists() else []
            recent_contacts = list(Contact.objects.order_by('-created_at')[:5]) if Contact.objects.exists() else []
            
            # Get visitor analytics data for charts with safe defaults
            try:
                device_stats = list(VisitorTracking.objects
                    .values('device_type')
                    .annotate(count=Count('id'))
                    .order_by('-count'))
                
                browser_stats = list(VisitorTracking.objects
                    .values('browser')
                    .annotate(count=Count('id'))
                    .order_by('-count'))
                
                page_stats = list(VisitorTracking.objects
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
            except:
                device_stats = []
                browser_stats = []
                page_stats = []
                daily_visitors = []
            
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
                'device_stats': json.dumps(device_stats),
                'browser_stats': json.dumps(browser_stats),
                'page_stats': json.dumps(page_stats),
                'daily_visitors': json.dumps(daily_visitors),
            }
            
            if extra_context:
                context.update(extra_context)
                
            return render(request, 'admin/index.html', context)
        except Exception as e:
            # Fallback to default admin index if there are any errors
            return super().index(request, extra_context)

# Create custom admin site instance
admin_site = CustomAdminSite(name='custom_admin')

# Register all models with the custom admin site
try:
    from product.models import Product, ProductCategory, ProductImage, ProductSpecification
    from product.admin import ProductCategoryAdmin, ProductAdmin, ProductImageAdmin, ProductSpecificationAdmin
    admin_site.register(Product, ProductAdmin)
    admin_site.register(ProductCategory, ProductCategoryAdmin)
    admin_site.register(ProductImage, ProductImageAdmin)
    admin_site.register(ProductSpecification, ProductSpecificationAdmin)
except:
    pass

try:
    from blog.models import Blog, BlogCategory, Comment
    from blog.admin import BlogCategoryAdmin, BlogAdmin, CommentAdmin
    admin_site.register(Blog, BlogAdmin)
    admin_site.register(BlogCategory, BlogCategoryAdmin)
    admin_site.register(Comment, CommentAdmin)
except:
    pass

try:
    from gallery.models import GalleryItem, GalleryCategory
    from gallery.admin import GalleryCategoryAdmin, GalleryItemAdmin
    admin_site.register(GalleryItem, GalleryItemAdmin)
    admin_site.register(GalleryCategory, GalleryCategoryAdmin)
except:
    pass

try:
    from contact.models import Contact, VisitorTracking, Newsletter
    from contact.admin import ContactAdmin, VisitorTrackingAdmin, NewsletterAdmin
    admin_site.register(Contact, ContactAdmin)
    admin_site.register(VisitorTracking, VisitorTrackingAdmin)
    admin_site.register(Newsletter, NewsletterAdmin)
except:
    pass

try:
    from users.models import User
    from users.admin import UserAdmin
    admin_site.register(User, UserAdmin)
except:
    pass

try:
    from core.models import *
    from core.admin import *
except:
    pass

try:
    from about.models import *
    from about.admin import *
except:
    pass

try:
    from faq.models import *
    from faq.admin import *
except:
    pass
