# Generated by Django 4.2.16 on 2024-11-15 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_options_user_image_alter_user_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='image',
            new_name='avatar',
        ),
    ]
