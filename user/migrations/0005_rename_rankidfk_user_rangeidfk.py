# Generated by Django 4.2.9 on 2024-05-16 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_rename_dependencyid_user_dependencyidfk_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='rankIdFK',
            new_name='rangeIdFK',
        ),
    ]
