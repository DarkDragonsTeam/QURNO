# Generated by Django 4.0.5 on 2022-07-08 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_post_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=225, unique=True, verbose_name='اسلاگ URL'),
        ),
    ]
