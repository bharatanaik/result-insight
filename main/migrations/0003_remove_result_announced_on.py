# Generated by Django 5.1.1 on 2024-10-01 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_student_branch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='announced_on',
        ),
    ]
