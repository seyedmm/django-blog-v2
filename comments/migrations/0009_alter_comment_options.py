# Generated by Django 4.2 on 2023-09-15 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0008_comment_checked'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'permissions': (('accept_comment', 'تایید کامنت'),), 'verbose_name': 'کامنت'},
        ),
    ]
