# Generated by Django 4.1.2 on 2023-05-17 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_matchevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchevent',
            name='match',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.matches'),
            preserve_default=False,
        ),
    ]
