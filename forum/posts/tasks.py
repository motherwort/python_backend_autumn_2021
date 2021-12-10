from django.core.mail import message
from application import celery_app
from django.core import mail
import json
from application import settings
import smtplib
import ssl


@celery_app.task()
def _send_dict_mail(subject, dict, from_email):
    message = str(json.dumps(dict, indent=4))
    return mail.send_mail(subject, message, from_email, settings.ADMINS)

def send_dict_mail(subject, dict, from_email):
    return _send_dict_mail.delay()