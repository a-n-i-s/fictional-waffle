from django.contrib import admin

# Register your models here.
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "user", "gender", "phonenumber", "country", "city"]
    list_filter = ["gender", "country", "city"]
    list_display_links = ["id", "pkid", "user"]


admin.site.register(Profile, ProfileAdmin)
