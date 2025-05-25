from django.shortcuts import render

def contact(request):
    return render(request, 'contact.html', {
        'title': 'Contact Us',
        'current_user': request.user if request.user.is_authenticated else None,
        'is_authenticated': request.user.is_authenticated
    })
