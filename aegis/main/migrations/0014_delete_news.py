# Generated by Django 4.1.2 on 2023-02-04 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_news_date_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='News',
        ),
    ]
