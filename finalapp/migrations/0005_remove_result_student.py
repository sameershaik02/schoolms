# Generated by Django 4.2.7 on 2023-12-18 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0004_alter_student_co'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='student',
        ),
    ]
