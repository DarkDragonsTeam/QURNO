# Generated by Django 4.0.6 on 2022-07-13 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=225, unique=True),
        ),
    ]