# Generated by Django 2.2.4 on 2019-08-11 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0007_auto_20190811_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='Service',
            field=models.ManyToManyField(blank=True, null=True, to='product.Service', verbose_name='Dịch Vụ'),
        ),
    ]
