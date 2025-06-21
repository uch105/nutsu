import os
import sys
import django
from decouple import config

project_root = config("PROJECT_ROOT")
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prescribemate.settings')
django.setup()

from django.core.mail import EmailMessage
from django.conf import settings

def send_automail(to_email, subject, body, html_body=None):
    """
    Send email with proper headers and formatting
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Plain text content
        html_body: Optional HTML content
    """
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_email,
        reply_to=[settings.DEFAULT_FROM_EMAIL],
    )
    
    if html_body:
        email.content_subtype = "html"
        email.body = html_body
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
'''  
send_automail(
    ['tanvirsaklan3660@gmail.com','only.uch105@gmail.com'],
    'Test Subject both',
    'Test message with django settings',
)
'''