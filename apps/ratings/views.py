from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import Response

from apps.profiles.models import Profile

from .models import Rating

User = get_user_model()


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_agent_review(request, profile_id):
    agent_profile = Profile.objects.get(id=profile_id, is_agent=True)
    data = request.data

    profile_user = User.objects.get(pkid=agent_profile.user.pkid)
    if profile_user.email == request.user.email:
        return Response(
            {"message": "You cannot rate yourself"}, status=status.HTTP_403_FORBIDDEN
        )

    if agent_profile.agent_review.filter(agent_pkid=request.user.pkid):
        return Response(
            {"message": "Profile allready reviewed"}, status=status.HTTP_400_BAD_REQUEST
        )

    elif data["rating"] == 0:
        return Response(
            {"message": "Please select a review"}, status=status.HTTP_400_BAD_REQUEST
        )

    else:
        Rating.objects.create(
            rater=request.user,
            agent=agent_profile,
            rating=data["rating"],
            comment=data["comment"],
        )

        return Response("Review added")
