# Generated by Django 2.2.4 on 2019-08-11 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0006_auto_20190811_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='Product',
            field=models.ManyToManyField(blank=True, null=True, to='product.Product', verbose_name='Sản Phẩm'),
        ),
    ]
