# Generated by Django 4.1.2 on 2022-11-12 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_orders_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='status',
            field=models.BooleanField(null=True, verbose_name='Завершена ли покупка?'),
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=4, verbose_name='Размер')),
                ('count', models.PositiveSmallIntegerField(verbose_name='Количество')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.orders', verbose_name='Карзина')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.products', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Товар из корзины',
                'verbose_name_plural': 'Товары из корзины',
            },
        ),
    ]
