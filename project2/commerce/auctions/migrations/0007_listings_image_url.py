# Generated by Django 4.1.3 on 2022-11-18 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listings_status_listings_user_alter_bids_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='image_url',
            field=models.CharField(default=0, max_length=2083),
            preserve_default=False,
        ),
    ]
