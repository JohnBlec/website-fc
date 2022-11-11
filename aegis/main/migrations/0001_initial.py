# Generated by Django 4.1.2 on 2022-10-24 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('number', models.PositiveSmallIntegerField(verbose_name='Игровой номер')),
                ('photo', models.ImageField(upload_to='main/img/PlayersAE', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Игрок',
                'verbose_name_plural': 'Игроки',
            },
        ),
    ]
