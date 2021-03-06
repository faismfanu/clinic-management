# Generated by Django 3.1.1 on 2020-10-14 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_doctor', '0029_remove_doctor_pat_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor_patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.IntegerField(null=True)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_doctor.doctor')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_doctor.patient')),
            ],
        ),
    ]
