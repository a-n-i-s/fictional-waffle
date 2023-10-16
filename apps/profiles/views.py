from rest_framework import generics, permissions, status

from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptioons import ProfileNotFound,NotYourProfile
from .serializers import ProfileSerializer,UpdateProfileSerializer
from .renderers import ProfileJsonRenderer
from .models import Profile

class AgentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(is_agent=True)
    serializer_class = ProfileSerializer

class TopAgentsListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(top_agent=True)
    serializer_class = ProfileSerializer


class GetProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJsonRenderer]

    def get(self, request):
        user=self.request.user
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile,context={"request":request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJsonRenderer]
    serializer_class = UpdateProfileSerializer

    def patch(self, request,username):
        
        if not Profile.objects.exists(user__username=username):
            raise ProfileNotFound
        user_name=request.user.username

        if user_name!=username:
            raise NotYourProfile
        data = request.data
        serializer = UpdateProfileSerializer(instance=request.user.profile, data=data,  partial = True)

        serializer.is_valid()
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    