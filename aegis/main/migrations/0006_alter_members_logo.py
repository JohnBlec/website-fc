# Generated by Django 4.1.2 on 2022-11-21 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_members_q_we'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='logo',
            field=models.ImageField(default='main/img/MembersAE/NoLogo.png', upload_to='main/img/MembersAE', verbose_name='Эмблема'),
        ),
    ]
