# Generated by Django 2.1.5 on 2020-06-27 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0013_auto_20200627_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profilePic',
            field=models.ImageField(blank=True, default='Default.jpg', null=True, upload_to=''),
        ),
    ]
