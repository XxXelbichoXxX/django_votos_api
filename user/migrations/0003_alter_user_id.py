# Generated by Django 4.2.9 on 2024-05-02 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(auto_created=True, blank=True, max_length=30, null=True),
        ),
    ]
