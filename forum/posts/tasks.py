from application import celery_app
from django.core import mail
import json
from application import settings


@celery_app.task()
def send_dict_mail(subject, dict):
    message = str(json.dumps(dict, indent=4))
    return mail.send_mail(subject, message, settings.EMAIL_HOST_EMAIL, settings.ADMINS)
