# Generated by Django 4.2.6 on 2023-11-09 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DIP', '0006_sprint_sprint_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('user_FName', models.CharField(max_length=250)),
                ('user_LName', models.CharField(max_length=250)),
                ('user_Password', models.CharField(max_length=250)),
                ('user_LoginName', models.CharField(max_length=250)),
                ('user_Type', models.CharField(max_length=1)),
            ],
        ),
    ]
