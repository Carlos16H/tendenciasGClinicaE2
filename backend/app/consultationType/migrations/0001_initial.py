# Generated by Django 5.1.1 on 2024-09-29 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medicalSpecialties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Tipo de consulta')),
                ('especialidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medicalSpecialties.medicalspecialty', verbose_name='Especialidad')),
            ],
        ),
    ]
