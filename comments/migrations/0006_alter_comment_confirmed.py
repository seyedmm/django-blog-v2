# Generated by Django 4.2 on 2023-09-13 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_comment_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='confirmed',
            field=models.CharField(choices=[('y', 'بله'), ('n', 'خیر')], default='n', max_length=1, verbose_name='تایید شده'),
        ),
    ]
