# Generated by Django 3.1.1 on 2020-10-14 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_doctor', '0027_auto_20201013_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='pat_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_doctor.patient'),
        ),
    ]
