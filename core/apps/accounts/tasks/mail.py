from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@shared_task
def send_verification_email(user_id, domain, mail_subject, email_template):
    User = get_user_model()
    user = User.objects.get(pk=user_id)

    context = {
        "user": user,
        "domain": domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user),
    }

    message = render_to_string(email_template, context)
    mail = EmailMessage(
        mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email]
    )
    mail.content_subtype = "html"
    mail.send()
