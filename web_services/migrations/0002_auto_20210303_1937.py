# Generated by Django 3.1.7 on 2021-03-03 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='password',
            field=models.CharField(default=False, max_length=200),
        ),
    ]
