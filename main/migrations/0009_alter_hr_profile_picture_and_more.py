# Generated by Django 5.0.4 on 2024-07-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_userprofile_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hr',
            name='profile_picture',
            field=models.ImageField(default='default_user.png', upload_to='pfp/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='default_user.png', upload_to='pfp/'),
        ),
    ]