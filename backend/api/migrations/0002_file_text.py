# Generated by Django 3.0.4 on 2021-03-12 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='text',
            field=models.CharField(default='hello', max_length=30),
            preserve_default=False,
        ),
    ]