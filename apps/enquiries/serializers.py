from rest_framework import serializers

from .models import EnQuiry


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnQuiry
        fields = "__all__"
