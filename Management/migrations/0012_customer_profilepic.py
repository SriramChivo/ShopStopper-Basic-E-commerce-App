# Generated by Django 2.1.5 on 2020-06-27 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0011_auto_20200626_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profilePic',
            field=models.ImageField(blank=True, null=True, upload_to='Profile_Pics'),
        ),
    ]
