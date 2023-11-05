from django.contrib import admin

from .models import EnQuiry

# Register your models here.


class EnquryAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number", "email", "message"]


admin.site.register(EnQuiry, EnquryAdmin)
