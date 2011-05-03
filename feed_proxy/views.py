# Create your views here.

from django.http import HttpResponse
import urllib2
import socket

# timeout in seconds
timeout = 5
socket.setdefaulttimeout(timeout)

def get_feed(request):

    req = urllib2.Request(request.GET["url"], headers={
            'Accept-Language' : request.META['HTTP_ACCEPT_LANGUAGE'],
    })
    resp = urllib2.urlopen(req)
    content = resp.read()
    mimetype = resp.info()['Content-Type']

    return HttpResponse(content, mimetype=mimetype)
