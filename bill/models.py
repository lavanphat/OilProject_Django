from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from product.models import Product, Service


# Create your models here.
class Bill(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Người Tạo')
    Date_Create = models.DateTimeField(auto_now_add=True, verbose_name='Ngày Tạo')
    Total_Money = models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Tổng Tiền', default=0)
    Sale = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)], default=0,
                               verbose_name='Giảm Giá')
    Active = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.User

    class Meta:
        verbose_name_plural = 'Hóa Đơn'

class Bill_Product(models.Model):
    Bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Sản Phẩm')
    Quality = models.IntegerField(default=1, verbose_name='Số Lượng')

    class Meta:
        verbose_name_plural = 'Hóa Đơn Sản Phầm'


class Bill_Service(models.Model):
    Bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    Service = models.ForeignKey(Service, on_delete=models.CASCADE)
    Quality = models.IntegerField(default=1, verbose_name='Số Lượng')

    class Meta:
        verbose_name_plural = 'Hóa Đơn Dịch Vụ'
