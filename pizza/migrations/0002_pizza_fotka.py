# Generated by Django 2.1.1 on 2018-09-30 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='fotka',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
    ]
