from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.ratings.serializers import RatingSerializer

from .models import Profile


class ProfileSerializer(ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    country = CountryField(name_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "id",
            "phonenumber",
            "profile_photo",
            "about_me",
            "license",
            "gender",
            "country",
            "city",
            "is_buyer",
            "is_seller",
            "is_agent",
            "rating",
            "num_reviews",
            "reviews",
        ]

    def get_full_name(self, obj):
        return f"{obj.user.first_name.title()} {obj.user.last_name.title()}"

    def get_reviews(self, obj):
        reviews = obj.agent_review.all()
        serializers = RatingSerializer(reviews, many=True)
        return serializers.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.top_agent:
            representation["top_agent"] = True
        return representation


class UpdateProfileSerializer(ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "phonenumber",
            "profile_photo",
            "about_me",
            "license",
            "gender",
            "country",
            "city",
            "is_buyer",
            "is_seller",
            "is_agent",
        ]
