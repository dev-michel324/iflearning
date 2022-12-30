from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.template import Template
from django.template.loader import get_template

from threading import Thread

EMAIL_NOTIFICATION_TYPES: dict = {
    "NEW_DEVICE_SIGNIN": "notifications/new_device_signin.html",
    "NEW_MODULE": "notifications/new_module.html", # change
    "NEW_DISCIPLINE": "notifications/new_discipline.html",
}

def send_mail_background(function):
    def start_thread(*args, **kwargs) -> None:
        Thread(target=function, args=args,
            kwargs=kwargs).start()
    return start_thread

@send_mail_background
def send_email(subject: str = "", html_content:str = "",
        recipients:list = [], from_email=settings.EMAIL_HOST_USER, message:str = ""):
    try:
        mail = send_mail(subject = subject, html_message=html_content,
            from_email=from_email, recipient_list=recipients, fail_silently=False, message=message)
        return True, {"message": "Email sent"}
    except BadHeaderError as e:
        return False, {"message": str(e)}

def send_email_notification(subject:str, email_type:str, context_data = {}, recipients:list = []) -> bool:
    if email_type in EMAIL_NOTIFICATION_TYPES.keys():
        template = get_template(EMAIL_NOTIFICATION_TYPES[email_type])
        context_data['login_url'] = "http://127.0.0.1:8000/login"
        html = template.render(context_data)
        send_mail(
            subject=subject,
            html_message=html,
            message="Signup successful",
            recipient_list=recipients,
            from_email=settings.EMAIL_HOST_USER
        )
        return True
    return False

@send_mail_background
def send_email_notification_async(subject:str, email_type:str, context_data = {}, recipients: list = []) -> bool:
    try:
        send_mail = send_email_notification(
            subject=subject,
            email_type=email_type,
            context_data=context_data,
            recipients=recipients
        )
        return send_mail
    except Exception as e:
        print("Exception in send_email_notification_async:" + str(e))
        return False