# Generated by Django 3.2.19 on 2024-06-07 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='current_offer',
            field=models.DecimalField(decimal_places=2, default=models.DecimalField(decimal_places=2, max_digits=10), max_digits=10),
        ),
    ]
