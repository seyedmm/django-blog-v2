# Generated by Django 4.2 on 2023-09-13 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_alter_comment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=480, verbose_name='متن'),
        ),
    ]
