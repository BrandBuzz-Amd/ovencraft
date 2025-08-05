from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import json
import re
from .models import Contact, VisitorTracking, Newsletter

def get_client_ip(request):
    """Get the client's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_device_type(user_agent):
    """Determine device type from user agent"""
    user_agent = user_agent.lower()
    if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
        return 'mobile'
    elif 'tablet' in user_agent or 'ipad' in user_agent:
        return 'tablet'
    else:
        return 'desktop'

def get_browser(user_agent):
    """Extract browser from user agent"""
    user_agent = user_agent.lower()
    if 'chrome' in user_agent:
        return 'Chrome'
    elif 'firefox' in user_agent:
        return 'Firefox'
    elif 'safari' in user_agent:
        return 'Safari'
    elif 'edge' in user_agent:
        return 'Edge'
    else:
        return 'Other'

def track_visitor(request):
    """Track visitor information"""
    try:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        page_visited = request.path
        referrer = request.META.get('HTTP_REFERER', '')
        session_key = request.session.session_key
        
        # Check if this visitor has already been tracked for this session
        if not VisitorTracking.objects.filter(
            ip_address=ip_address,
            session_key=session_key,
            page_visited=page_visited
        ).exists():
            VisitorTracking.objects.create(
                ip_address=ip_address,
                user_agent=user_agent,
                page_visited=page_visited,
                referrer=referrer,
                session_key=session_key,
                device_type=get_device_type(user_agent),
                browser=get_browser(user_agent)
            )
    except Exception as e:
        # Log error but don't break the page
        print(f"Visitor tracking error: {e}")

def contact(request):
    # Track visitor
    track_visitor(request)
    
    if request.method == 'POST':
        try:
            # Handle form submission
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            phone = request.POST.get('City', '').strip()
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()
            newsletter = request.POST.get('newsletter') == 'on'
            
            # Validate required fields
            if not all([name, email, subject, message]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please fill in all required fields.'
                })
            
            # Validate email format
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please enter a valid email address.'
                })
            
            # Create contact entry
            contact_entry = Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
                newsletter_subscription=newsletter
            )
            
            # Handle newsletter subscription
            if newsletter:
                Newsletter.objects.get_or_create(
                    email=email,
                    defaults={'name': name}
                )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for your message! We will get back to you soon.'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred while sending your message. Please try again.'
            })
    
    return render(request, 'contact.html', {
        'title': 'Contact Us',
        'current_user': request.user if request.user.is_authenticated else None,
        'is_authenticated': request.user.is_authenticated
    })

# Admin AJAX Views
@staff_member_required
def contact_detail_ajax(request, contact_id):
    """AJAX view to get contact details for modal"""
    contact = get_object_or_404(Contact, id=contact_id)
    
    if request.method == 'GET':
        html = render_to_string('admin/contact/contact/detail_modal.html', {
            'contact': contact
        })
        return JsonResponse({
            'success': True,
            'html': html
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@staff_member_required
@csrf_exempt
@require_http_methods(["POST"])
def mark_contact_read(request, contact_id):
    """AJAX view to mark contact as read"""
    try:
        contact = get_object_or_404(Contact, id=contact_id)
        contact.is_read = True
        contact.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Contact from {contact.name} marked as read'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@staff_member_required
@csrf_exempt
@require_http_methods(["POST"])
def mark_contact_unread(request, contact_id):
    """AJAX view to mark contact as unread"""
    try:
        contact = get_object_or_404(Contact, id=contact_id)
        contact.is_read = False
        contact.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Contact from {contact.name} marked as unread'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@staff_member_required
def contact_stats_ajax(request):
    """AJAX view to get updated contact statistics"""
    from django.utils import timezone
    
    today = timezone.now().date()
    
    stats = {
        'total_count': Contact.objects.count(),
        'unread_count': Contact.objects.filter(is_read=False).count(),
        'today_count': Contact.objects.filter(created_at__date=today).count(),
        'newsletter_count': Contact.objects.filter(newsletter_subscription=True).count(),
    }
    
    return JsonResponse({
        'success': True,
        'stats': stats
    })

@csrf_exempt
@require_http_methods(["POST"])
def contact_api(request):
    """API endpoint for contact form submission"""
    try:
        data = json.loads(request.body)
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
        newsletter = data.get('newsletter', False)
        
        # Validate required fields
        if not all([name, email, subject, message]):
            return JsonResponse({
                'status': 'error',
                'message': 'Please fill in all required fields.'
            })
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return JsonResponse({
                'status': 'error',
                'message': 'Please enter a valid email address.'
            })
        
        # Create contact entry
        contact_entry = Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
            newsletter_subscription=newsletter
        )
        
        # Handle newsletter subscription
        if newsletter:
            Newsletter.objects.get_or_create(
                email=email,
                defaults={'name': name}
            )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Thank you for your message! We will get back to you soon.'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid data format.'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'An error occurred while sending your message. Please try again.'
        })
