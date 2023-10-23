from django.db import models
from apps.common.models import TimeStampedUUIDModel
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class EnQuiry(TimeStampedUUIDModel):
    name = models.CharField(verbose_name=_('Your Name'), max_length=100)
    phone_number = PhoneNumberField(_('Phone Number'), max_length=15, default='+880123456789')
    email = models.EmailField(_('Email'))
    subject = models.CharField(_('Subject'), max_length=100)
    message = models.TextField(_('message'))

    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name_plural = 'Enquiries'