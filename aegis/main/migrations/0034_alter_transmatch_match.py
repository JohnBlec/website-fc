# Generated by Django 4.1.2 on 2023-05-21 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_transmatch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transmatch',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.matches', unique=True),
        ),
    ]
