# Generated by Django 4.1.7 on 2023-03-20 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forgery', '0002_rename_upimage_images_uploaded_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='ela_image',
            field=models.ImageField(default=' ', upload_to='upload/'),
        ),
    ]