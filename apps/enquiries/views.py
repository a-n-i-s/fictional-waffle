from django.core.mail import send_mail
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import Response

from real_estate.settings.development import DEFAULT_FROM_EMAIL

from .models import EnQuiry


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def send_enquiry_email(request):
    data = request["data"]
    try:
        subject = data["subject"]
        name = data["name"]
        email = data["email"]
        message = data["message"]
        from_email = data["email"]
        recipient_list = data[DEFAULT_FROM_EMAIL]

        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        enquiry = EnQuiry(name=name, subject=subject, email=email, message=message)
        enquiry.save()

        return Response({"success": "Your enquiry was successfully submitted"})
    except Exception:
        return Response({"fail": "Your enquiry was not sent. Please try again"})
