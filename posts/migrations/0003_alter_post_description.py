# Generated by Django 4.2 on 2023-09-11 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_description_alter_post_author_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(max_length=200, verbose_name='توضیحات'),
        ),
    ]
