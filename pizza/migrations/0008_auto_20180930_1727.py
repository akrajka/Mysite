# Generated by Django 2.1.1 on 2018-09-30 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0007_auto_20180930_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='fotka',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
