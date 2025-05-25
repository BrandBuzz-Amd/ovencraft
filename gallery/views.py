from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from gallery.models import GalleryItem
from blog.models import BlogCategory  # Correct model name

def index(request):
    gallery_items_list = GalleryItem.objects.all().order_by('-created_at')
    categories = BlogCategory.objects.all()

    paginator = Paginator(gallery_items_list, 9)  # Show 9 items per page
    page = request.GET.get('page')

    try:
        gallery_items = paginator.page(page)
    except PageNotAnInteger:
        gallery_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range, show empty list
        gallery_items = []

    # If no items, show message flag
    show_message = False
    if not gallery_items or (hasattr(gallery_items, '__len__') and len(gallery_items) == 0):
        show_message = True

    return render(request, 'gallery.html', {
        'gallery_items': gallery_items,
        'categories': categories,
        'show_message': show_message,
        'title': 'Gallery',
    })
