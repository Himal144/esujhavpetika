from django.conf import settings
import threading
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

# Define a function to send email
def send_email(subject, html_content, recipient_list):
    from_email = settings.EMAIL_HOST_USER
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        recipient_list
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
# Define a custom thread class to handle email sending
class EmailThread(threading.Thread):
    def __init__(self, subject, html_context, recipient_list):
        self.subject = subject
        self.html_context = html_context
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        send_email(self.subject, self.html_context, self.recipient_list)