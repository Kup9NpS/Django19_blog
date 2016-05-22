# coding=utf-8
from django.core.mail import send_mail
from django.template.loader import render_to_string
from src import settings


def lks_send_email(email, subject, content, plain_content=''):
    return send_mail(subject, plain_content, settings.EMAIL_HOST_USER, [email], html_message=content,
                     fail_silently=True)


def confirm_email(email, activation_key):
    body = render_to_string('mail/email_confirm.html',
                            {'activation_key': activation_key, 'current_host': settings.CURRENT_HOST})
    return lks_send_email(email, u'Подтверждение адреса электронной почты', body)


def resetpass_email(email, new_pass):
    body = render_to_string('mail/email_resetpass.html',
                            {'new_pass': new_pass, 'current_host': settings.CURRENT_HOST})
    return lks_send_email(email, u'Смена пароля', body)
