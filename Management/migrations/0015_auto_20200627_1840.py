# Generated by Django 2.1.5 on 2020-06-27 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0014_auto_20200627_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profilePic',
            field=models.ImageField(default='Default.jpg', upload_to=''),
        ),
    ]
