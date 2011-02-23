from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, redirect

def get_messages(request):
    context = { 'messages' : messages.get_messages(request) }
    return render_to_response("base/messages.html", context)

def home(request):
    if request.user:
        rv = redirect("your_projects")
    else:
        rv = render_to_response("intro.html")
    return rv
        
