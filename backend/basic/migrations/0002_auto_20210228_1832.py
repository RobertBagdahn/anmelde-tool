# Generated by Django 3.1.5 on 2021-02-28 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postaladdress',
            name='address_addition',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
