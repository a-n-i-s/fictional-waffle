# Generated by Django 3.2.7 on 2023-09-19 04:39

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+8801234567', max_length=14, region=None, verbose_name='Phone Number'),
        ),
    ]
