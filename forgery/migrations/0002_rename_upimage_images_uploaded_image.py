# Generated by Django 4.1.7 on 2023-03-19 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forgery', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='upimage',
            new_name='uploaded_image',
        ),
    ]
