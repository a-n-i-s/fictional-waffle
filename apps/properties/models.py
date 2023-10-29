from collections.abc import Iterable
import random
import string
from django.db import models
from autoslug import AutoSlugField

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.common.models import TimeStampedUUIDModel


User = get_user_model()


class PropertyPublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(published_status=True)


class Property(TimeStampedUUIDModel):
    class Advertype(models.TextChoices):
        FOR_SALE = "For SALE", _("FOR SALE")
        FOR_RENT = "For Rent", _("FOR Rent")
        AUCTION = "Auction", _("Auction")

    class PropertyType(models.TextChoices):
        HOUSE = "House", _("House")
        APARTMENT = "Apartment", _("Apartment")
        OFFICE = "Office", _("Office")
        WAREHOUSE = "Warehouse", _("Warehouse")
        COMMERCIAL = "Commercial", _("Commercial")
        OTHER = "Other", _("Other")

    user = models.ForeignKey(
        User,
        verbose_name=_("Agent seller or buyer"),
        related_name="agent_buyer",
        on_delete=models.DO_NOTHING,
    )

    title = models.CharField(verbose_name=_("Property title"), max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    ref_code = models.CharField(
        verbose_name=_("Property referrance code"),
        max_length=255,
        unique=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"), default="default description "
    )
    country = CountryField(
        verbose_name=_("Country"), default="BD", blank_label="select country"
    )
    city = models.CharField(verbose_name=_("City"), max_length=180, default="Dhaka")
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=100, default="000"
    )
    street_address = models.CharField(
        verbose_name=_("Street Address"), max_length=150, default="address of street"
    )
    property_number = models.IntegerField(
        verbose_name=_("Property Number"),
        validators=[MinValueValidator(1)],
        default=112,
    )
    price = models.DecimalField(
        verbose_name=_("Price"), decimal_places=2, max_digits=8, default=0.0
    )
    tax = models.DecimalField(
        verbose_name=_("Tax"), decimal_places=2, default=0.15, max_digits=4
    )
    plot_area = models.DecimalField(
        verbose_name=_("Plot Area(m^2)"), max_digits=8, decimal_places=2, default=0.0
    )
    total_floors = models.IntegerField(verbose_name=_("Number of Floors"), default=0)
    bedrooms = models.IntegerField(verbose_name=_("Number of Bedrooms"), default=1)
    bathrooms = models.DecimalField(
        verbose_name=_("Number of Bathrooms"),
        max_digits=4,
        decimal_places=2,
        default=1.0,
    )
    advert_type = models.CharField(
        verbose_name=_("Advert Type"),
        max_length=100,
        choices=Advertype.choices,
        default=Advertype.FOR_SALE,
    )
    property_type = models.CharField(
        verbose_name=_("Property Type"),
        max_length=100,
        choices=PropertyType.choices,
        default=PropertyType.APARTMENT,
    )
    cover_photo = models.ImageField(
        verbose_name=_("Main Photo"), default="/house_sample.jpg", null=True, blank=True
    )
    photo1 = models.ImageField(default="/interior_sample.jpg", null=True, blank=True)
    photo2 = models.ImageField(default="/interior_sample.jpg", null=True, blank=True)
    photo3 = models.ImageField(default="/interior_sample.jpg", null=True, blank=True)
    photo4 = models.ImageField(default="/interior_sample.jpg", null=True, blank=True)
    published_status = models.BooleanField(
        verbose_name=_("Published Status"), default=False
    )
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)
    objects = models.Manager()
    published = PropertyPublishedManager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        return super(Property, self).save(*args, **kwargs)

    @property
    def final_property_price(self):
        tax_percentage = self.tax
        property_price = self.price
        tax_amount = round(tax_percentage * property_price, 2)
        price_after_tax = float(round(tax_amount + property_price))

        return price_after_tax


class PropertyViews(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_("IP Address"), max_length=255)
    property = models.ForeignKey(
        Property, related_name="property_views", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"Total views on - {self.property.title} is: {self.property.views}"

    class Meta:
        verbose_name = " Total View on Property"
        verbose_name = " Total Views on Property"
