# Generated by Django 3.1.1 on 2020-09-28 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_doctor', '0005_doctor_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='doctor_password',
        ),
    ]
