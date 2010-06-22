from django.http import HttpResponse
from subprocess import Popen, PIPE

from django.conf import settings

def get_fortune(request):

    msg = Popen([settings.FORTUNE_BIN, settings.FORTUNE_PATH], stdout=PIPE).communicate()[0]
    #FIXME: to be split and passed to template as context
    msg = '<div class="italic">' + msg
    msg = msg.replace("-- ", '</div><div class="author">')
    msg += '</div>'
    msg = msg.replace("\n","<br />")
    return HttpResponse(msg)
