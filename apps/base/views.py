from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404

def get_messages(request):
    context = { 'messages' : messages.get_messages(request) }
    return render_to_response("base/messages.html", context)
