# Generated by Django 4.0.6 on 2022-07-16 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]