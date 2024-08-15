# Generated by Django 4.2.9 on 2024-08-07 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ForgetPasswordRequest',
            fields=[
                ('requestId', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=128, unique=True)),
                ('email', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=128)),
            ],
        ),
    ]
