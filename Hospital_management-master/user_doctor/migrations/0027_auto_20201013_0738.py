# Generated by Django 3.1.1 on 2020-10-13 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_doctor', '0026_auto_20201013_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='doctor_image',
            field=models.ImageField(blank=True, max_length=10000, null=True, upload_to=''),
        ),
    ]
