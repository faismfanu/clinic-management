# Generated by Django 3.1.1 on 2020-10-11 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_doctor', '0023_auto_20201009_1123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='doctor_qualification',
        ),
        migrations.CreateModel(
            name='doctor_qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_degree', models.CharField(max_length=225)),
                ('doctor_college', models.CharField(max_length=225)),
                ('doctor_year', models.CharField(max_length=225)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_doctor.doctor')),
            ],
        ),
    ]
