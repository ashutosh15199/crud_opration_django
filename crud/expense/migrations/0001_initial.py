# Generated by Django 5.1.6 on 2025-03-07 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
                ('transection_type', models.CharField(choices=[('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')], max_length=100)),
            ],
        ),
    ]
