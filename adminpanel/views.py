from django.http import HttpResponse

def index(request):
    return HttpResponse("Adminpanel app index page")
