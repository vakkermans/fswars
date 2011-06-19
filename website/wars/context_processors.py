from django.conf import settings

def extra_settings(context):
    return {'COMET_URL': settings.COMET_URL}
