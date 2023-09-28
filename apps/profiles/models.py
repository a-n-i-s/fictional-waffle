from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedUUIDModel

User=get_user_model()

class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")

class Profile(TimeStampedUUIDModel):
    user=models.OneToOneField(User,related_name="profile",on_delete=models.CASCADE)
    phonenumber=PhoneNumberField(verbose_name=_("Phone Number"), max_length=14, default="+8801234567")
    about_me=models.TextField(verbose_name=_("About Me"),default="Say something about yourself")
    license=models.CharField(verbose_name=_('Real Estate License'), max_length=20, blank=True, null=True)
    profile_photo=models.ImageField(verbose_name=_('Profile Photo'), default='/profiles/profile_defautlt.png')
    gender=models.CharField(verbose_name=_('Gender'),choices=Gender.choices,default=Gender.MALE, max_length=20)
    country=CountryField(verbose_name=_('Country'),default="BD",blank=False,null=False)
    city=models.CharField(verbose_name=_('city'),max_length=180,default='Dhaka',blank=False,null=False)
    is_buyer=models.BooleanField(verbose_name=_('Buyer'),default=False,help_text='Are You looking to buy a property?')
    is_seller=models.BooleanField(verbose_name=_('Seller'),default=False,help_text='Are You looking to sell a property?')
    is_agent=models.BooleanField(verbose_name=_('Agent'),default=False,help_text='Are You an agent?')
    top_agent=models.BooleanField(verbose_name=_('Top Agent'),default=False)
    top_seller=models.BooleanField(verbose_name=_('Top Agent'),default=False)
    rating=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    num_reviews=models.IntegerField(verbose_name=_('Number of Reviews'),default=0,null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"
    