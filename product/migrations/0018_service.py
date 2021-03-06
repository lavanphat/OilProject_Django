# Generated by Django 2.2.4 on 2019-08-11 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Tên Dịch Vụ')),
                ('Price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Giá')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Từ Khóa Dịch Vụ')),
                ('Active', models.BooleanField(verbose_name='Kích Hoạt')),
            ],
            options={
                'verbose_name_plural': 'Dịch Vụ',
            },
        ),
    ]
