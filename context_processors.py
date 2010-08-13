from django.conf import settings

def jagom_settings(request):
    return {
        "VERSION": settings.VERSION,
    }

