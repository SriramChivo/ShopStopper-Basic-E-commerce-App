# Generated by Django 2.1.5 on 2020-06-27 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0012_customer_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profilePic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
