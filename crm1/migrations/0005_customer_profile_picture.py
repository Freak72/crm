# Generated by Django 3.0.7 on 2021-03-15 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm1', '0004_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
