# Generated by Django 3.1.7 on 2021-03-03 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=70)),
                ('username', models.CharField(default='', max_length=200)),
                ('password', models.BooleanField(default=False)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsStories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=64)),
                ('category', models.CharField(max_length=60)),
                ('region', models.CharField(max_length=60)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('details', models.CharField(max_length=512)),
                ('aurthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_services.author')),
            ],
        ),
    ]
