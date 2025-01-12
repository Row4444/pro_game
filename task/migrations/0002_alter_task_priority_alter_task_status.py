# Generated by Django 5.1.4 on 2025-01-12 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], db_index=True, default='medium', max_length=20),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('in_progress', 'In_progress'), ('completed', 'Completed')], db_index=True, default='new', max_length=20),
        ),
    ]