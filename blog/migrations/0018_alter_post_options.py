# Generated by Django 4.0.6 on 2022-07-13 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_alter_post_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-datetime_modified',), 'verbose_name': 'پست', 'verbose_name_plural': 'پست ها'},
        ),
    ]
