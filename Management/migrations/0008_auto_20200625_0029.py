# Generated by Django 2.1.5 on 2020-06-24 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0007_auto_20200622_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='profilePic',
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]