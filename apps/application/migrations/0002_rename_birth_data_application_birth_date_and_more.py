# Generated by Django 5.1 on 2024-09-10 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='birth_data',
            new_name='birth_date',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='password',
            new_name='passport',
        ),
    ]
