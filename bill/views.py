import datetime
import json
from calendar import monthrange

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from bill.models import Bill, Bill_Product, Bill_Service
from product.models import Product, Service


# Create your views here.


@login_required
def bill(request):
    bill_list = Bill.objects.all().order_by('-Date_Create')[:50]
    context = {
        'bill': bill_list,
        'product_select': Product.objects.filter(Active=True),
        'service_select': Service.objects.filter(Active=True)
    }
    return render(request, 'bill.html', context)


@login_required
def details_bill(request, id):
    product_bill = Bill_Product.objects.filter(Bill=id).values('Bill', 'Product__title', 'Quality',
                                                               'Product__Price_New', 'Product_id')
    service_bill = Bill_Service.objects.filter(Bill=id).values('Bill', 'Service__title', 'Quality', 'Service__Price',
                                                               'Service_id')
    context = {
        'product': list(product_bill),
        'service': list(service_bill),
        'status': True
    }
    return JsonResponse(context)


@login_required
def load_details(request, id):
    bill = Bill.objects.filter(id=id).values()
    context = {
        'bill': list(bill),
        'status': True
    }
    return JsonResponse(context)


@login_required
def add_bill(request):
    data = {}
    if request.is_ajax():
        total_price = request.POST.get('total', None)
        bill = Bill.objects.create(User=request.user, Total_Money=total_price, Sale=0)
        bill.save()

        product = request.POST['product']
        data_product = json.loads(product)

        service = request.POST['service']
        data_service = json.loads(service)

        for x in data_product:
            bill_product = Bill_Product.objects.create(Bill_id=bill.id, Product_id=x['id'], Quality=x['quality'])
            bill_product.save()

            # tru so luong san pham ton
            quality_product = Product.objects.filter(id=x['id'])[0].Quality
            product = Product.objects.filter(id=x['id']).update(Quality=quality_product - int(x['quality']))

        for x in data_service:
            bill_service = Bill_Service.objects.create(Bill_id=bill.id, Service_id=x['id'], Quality=x['quality'])
            bill_service.save()

        # load danh sach bill
        # bill = Bill.objects.all()
        # data['bill'] = render_to_string('bill.html', {'bill': bill})

    data['status'] = True
    return JsonResponse(data)


@login_required
def update_bill(request, id):
    if request.is_ajax():
        id_bill = request.POST.get('id', None)
        status = request.POST.get('status', None)
        if (status == 'true'):
            status = 1
        else:
            status = 0
        bill = Bill.objects.filter(id=id_bill).update(Active=status)
    context = {
        'status': True
    }
    return JsonResponse(context)


# day
class BillDay(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        labels = ['0:00 - 4:00', '4:00 - 8:00', '8:00 - 12:00', '12:00 - 16:00', '16:00 - 20:00', '20:00 - 24:00']
        # labels = ['0:00','4:00', '8:00', '12:00', '16:00', '20:00']
        day = timezone.now().day
        hour_first = 0
        hour_last = 4
        bill = []
        bills = Bill.objects.filter(Date_Create__month=timezone.now().month, Date_Create__year=timezone.now().year,
                                    Active=True)
        for item in bills:
            if hour_last <= 24:
                bill.append(
                    bills.filter(Date_Create__day=day, Date_Create__hour__gte=hour_first,
                                 Date_Create__hour__lt=hour_last, Active=True).count())
                hour_first += 4
                hour_last += 4
        data = {
            'labels': labels,
            'data': bill,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class BillDayCustom(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        labels = ['0:00 - 4:00', '4:00 - 8:00', '8:00 - 12:00', '12:00 - 16:00', '16:00 - 20:00', '20:00 - 24:00']
        # labels = ['0:00','4:00', '8:00', '12:00', '16:00', '20:00']
        day = request.GET.get('day')
        month = request.GET.get('month')
        year = request.GET.get('year')
        hour_first = 0
        hour_last = 4
        bill = []
        bills = Bill.objects.filter(Date_Create__month=month, Date_Create__year=year, Active=True)
        for item in bills:
            if hour_last <= 24:
                bill.append(
                    bills.filter(Date_Create__day=day, Date_Create__hour__gte=hour_first,
                                 Date_Create__hour__lt=hour_last, Active=True).count())
            hour_first += 4
            hour_last += 4

        data = {
            'labels': labels,
            'data': bill,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class MoneyDay(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        labels = ['0:00 - 4:00', '4:00 - 8:00', '8:00 - 12:00', '12:00 - 16:00', '16:00 - 20:00', '20:00 - 24:00']
        # labels = ['0:00','4:00', '8:00', '12:00', '16:00', '20:00']
        day = timezone.now().day
        hour_first = 0
        hour_last = 4
        bill = []
        bills = Bill.objects.filter(Date_Create__month=timezone.now().month, Date_Create__year=timezone.now().year,
                                    Active=True).values_list('id', flat=True)
        for item in bills:
            if hour_last <= 24:
                x = bills.filter(Date_Create__day=day, Date_Create__hour__gte=hour_first,
                                 Date_Create__hour__lt=hour_last, Active=True).values_list('Total_Money', flat=True)
                hour_first += 4
                hour_last += 4
                x = sum(x)
                bill.append(x)
        data = {
            'labels': labels,
            'data': bill,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class MoneyDayCustom(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        labels = ['0:00 - 4:00', '4:00 - 8:00', '8:00 - 12:00', '12:00 - 16:00', '16:00 - 20:00', '20:00 - 24:00']
        # labels = ['0:00','4:00', '8:00', '12:00', '16:00', '20:00']
        day = request.GET.get('day')
        month = request.GET.get('month')
        year = request.GET.get('year')
        hour_first = 0
        hour_last = 4
        bill = []
        bills = Bill.objects.filter(Date_Create__month=month, Date_Create__year=year, Active=True).values_list('id',
                                                                                                               flat=True)
        for item in bills:
            if hour_last <= 24:
                x = bills.filter(Date_Create__day=day, Date_Create__hour__gte=hour_first,
                                 Date_Create__hour__lt=hour_last, Active=True).values_list('Total_Money', flat=True)
                hour_first += 4
                hour_last += 4
                x = sum(x)
                bill.append(x)
        data = {
            'labels': labels,
            'data': bill,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class ProductDay(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        quality = []
        day = timezone.now().day
        product_list = Bill_Product.objects.filter(Bill__Date_Create__month=timezone.now().month,
                                                   Bill__Date_Create__year=timezone.now().year,
                                                   Bill__Active=True).values_list(
            'Product__title',
            flat=True).distinct()
        product_list = list(product_list)
        for x in product_list:
            item = Bill_Product.objects.filter(Bill__Date_Create__day=day, Product__title=x,
                                               Bill__Active=True).values_list('Quality',
                                                                              flat=True)
            item = sum(item)
            quality.append(item)
        data = {
            'labels': product_list,
            'data': quality,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class ProductDayCustom(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        quality = []
        day = request.GET.get('day')
        month = request.GET.get('month')
        year = request.GET.get('year')
        product_list = Bill_Product.objects.filter(Bill__Date_Create__day=day, Bill__Date_Create__month=month,
                                                   Bill__Date_Create__year=year, Bill__Active=True).values_list(
            'Product__title',
            flat=True).distinct()
        product_list = list(product_list)
        for x in product_list:
            item = Bill_Product.objects.filter(Product__title=x, Bill__Date_Create__day=day,
                                               Bill__Date_Create__month=month,
                                               Bill__Date_Create__year=year, Bill__Active=True).values_list('Quality',
                                                                                                            flat=True)
            item = sum(item)
            quality.append(item)
        data = {
            'labels': product_list,
            'data': quality,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class ServiceDay(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        quality = []
        day = timezone.now().day
        service_list = Bill_Service.objects.filter(Bill__Date_Create__month=timezone.now().month,
                                                   Bill__Date_Create__year=timezone.now().year,
                                                   Bill__Active=True).values_list(
            'Service__title',
            flat=True).distinct()
        service_list = list(service_list)
        for x in service_list:
            item = Bill_Service.objects.filter(Bill__Date_Create__day=day, Service__title=x,
                                               Bill__Active=True).values_list('Quality',
                                                                              flat=True)
            item = sum(item)
            quality.append(item)
        data = {
            'labels': service_list,
            'data': quality,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class ServiceDayCustom(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        quality = []
        day = request.GET.get('day')
        month = request.GET.get('month')
        year = request.GET.get('year')
        service_list = Bill_Service.objects.filter(Bill__Date_Create__day=day, Bill__Date_Create__month=month,
                                                   Bill__Date_Create__year=year, Bill__Active=True).values_list(
            'Service__title',
            flat=True).distinct()
        service_list = list(service_list)
        for x in service_list:
            item = Bill_Service.objects.filter(Service__title=x, Bill__Date_Create__day=day,
                                               Bill__Date_Create__month=month,
                                               Bill__Date_Create__year=year, Bill__Active=True).values_list('Quality',
                                                                                                            flat=True)
            item = sum(item)
            quality.append(item)
        data = {
            'labels': service_list,
            'data': quality,
            'status': True,
            'time': 'today'
        }
        return Response(data)


# //week
class BillWeek(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        labels = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật']
        week = datetime.date(timezone.now().year, timezone.now().month, timezone.now().day).strftime('%V')
        bill = []
        bills = Bill.objects.filter(Date_Create__week=week, Active=True)
        weekday = 2
        for item in bills:
            if weekday < 8:
                bill.append(bills.filter(Date_Create__week_day=weekday, Active=True).count())
                weekday += 1
        bill.append(bills.filter(Date_Create__week_day=1, Active=True).count())
        data = {
            'labels': labels,
            'data': bill,
            'status': True,
        }
        return Response(data)


class ProductWeek(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        quality = []
        week = datetime.date(timezone.now().year, timezone.now().month, timezone.now().day).strftime('%V')
        product_list = Bill_Product.objects.filter(Bill__Date_Create__week=week, Bill__Active=True).values_list(
            'Product__title',
            flat=True).distinct()
        for x in product_list:
            item = Bill_Product.objects.filter(Product__title=x, Bill__Date_Create__week=week,
                                               Bill__Active=True).values_list('Quality',
                                                                              flat=True)
            item = sum(item)
            quality.append(item)
        data = {
            'labels': product_list,
            'data': quality,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class ServiceWeek(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        quality = []
        week = datetime.date(timezone.now().year, timezone.now().month, timezone.now().day).strftime('%V')
        service_list = Bill_Service.objects.filter(Bill__Date_Create__week=week, Bill__Active=True).values_list(
            'Service__title',
            flat=True).distinct()
        for x in service_list:
            item = Bill_Service.objects.filter(Service__title=x, Bill__Date_Create__week=week,
                                               Bill__Active=True).values_list('Quality',
                                                                              flat=True)
            item = sum(item)
            quality.append(item)
        data = {
            'labels': service_list,
            'data': quality,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class MoneyWeek(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        labels = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật']
        week = datetime.date(timezone.now().year, timezone.now().month, timezone.now().day).strftime('%V')
        total = []
        total_list = Bill.objects.filter(Date_Create__week=week, Active=True)
        weekday = 2
        for item in total_list:
            if weekday < 8:
                price = total_list.filter(Date_Create__week_day=weekday, Active=True).values_list('Total_Money',
                                                                                                  flat=True)
                price = sum(price)
                total.append(price)
                weekday += 1
        total.append(sum(total_list.filter(Date_Create__week_day=1, Active=True).values_list('Total_Money', flat=True)))
        data = {
            'labels': labels,
            'data': total,
            'status': True,
            'time': 'today'
        }
        return Response(data)


# month
class BillMonth(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        month_input = request.GET.get('month')
        year_input = request.GET.get('year')
        day_in_month = 0
        labels = []
        bill = []
        if month_input and year_input:
            day_in_month = monthrange(int(year_input), int(month_input))[1]
            for x in range(day_in_month):
                labels.append(x + 1)
                bill.append(Bill.objects.filter(Date_Create__day=x + 1, Date_Create__month=int(month_input),
                                                Date_Create__year=int(year_input), Active=True).count())
        else:
            day_in_month = monthrange(timezone.now().year, timezone.now().month)[1]
            for x in range(day_in_month):
                labels.append(x + 1)
                bill.append(Bill.objects.filter(Date_Create__day=x + 1, Date_Create__month=timezone.now().month,
                                                Date_Create__year=timezone.now().year, Active=True).count())
        data = {
            'labels': labels,
            'data': bill,
            'status': True,
        }
        return Response(data)


class ProductMonth(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        quality = []
        month_input = request.GET.get('month')
        year_input = request.GET.get('year')
        if month_input and year_input:
            product_list = Bill_Product.objects.filter(Bill__Date_Create__month=int(month_input),
                                                       Bill__Date_Create__year=int(year_input),
                                                       Bill__Active=True).values_list(
                'Product__title',
                flat=True).distinct()
            print(product_list)
            for x in product_list:
                item = Bill_Product.objects.filter(Product__title=x, Bill__Date_Create__month=int(month_input),
                                                   Bill__Date_Create__year=int(year_input),
                                                   Bill__Active=True).values_list('Quality',
                                                                                  flat=True)
                item = sum(item)
                quality.append(item)
        else:
            product_list = Bill_Product.objects.filter(Bill__Date_Create__month=timezone.now().month,
                                                       Bill__Date_Create__year=timezone.now().year,
                                                       Bill__Active=True).values_list(
                'Product__title',
                flat=True).distinct()
            for x in product_list:
                item = Bill_Product.objects.filter(Product__title=x, Bill__Date_Create__month=timezone.now().month,
                                                   Bill__Date_Create__year=timezone.now().year,
                                                   Bill__Active=True).values_list('Quality',
                                                                                  flat=True)
                item = sum(item)
                quality.append(item)
        data = {
            'labels': product_list,
            'data': quality,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class ServiceMonth(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        quality = []
        month_input = request.GET.get('month')
        year_input = request.GET.get('year')
        if month_input and year_input:
            service_list = Bill_Service.objects.filter(Bill__Date_Create__month=int(month_input),
                                                       Bill__Date_Create__year=int(year_input),
                                                       Bill__Active=True).values_list(
                'Service__title',
                flat=True).distinct()
            for x in service_list:
                item = Bill_Service.objects.filter(Service__title=x, Bill__Date_Create__month=int(month_input),
                                                   Bill__Date_Create__year=int(year_input),
                                                   Bill__Active=True).values_list(
                    'Quality',
                    flat=True)
                item = sum(item)
                quality.append(item)
        else:
            service_list = Bill_Service.objects.filter(Bill__Date_Create__month=timezone.now().month,
                                                       Bill__Date_Create__year=timezone.now().year,
                                                       Bill__Active=True).values_list(
                'Service__title',
                flat=True).distinct()
            for x in service_list:
                item = Bill_Service.objects.filter(Service__title=x, Bill__Date_Create__month=timezone.now().month,
                                                   Bill__Date_Create__year=timezone.now().year,
                                                   Bill__Active=True).values_list('Quality',
                                                                                  flat=True)
                item = sum(item)
                quality.append(item)
        data = {
            'labels': service_list,
            'data': quality,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class MoneyMonth(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        month_input = request.GET.get('month')
        year_input = request.GET.get('year')
        day_in_month = 0
        labels = []
        total = []
        if month_input and year_input:
            day_in_month = monthrange(int(year_input), int(month_input))[1]
            for x in range(day_in_month):
                labels.append(x + 1)
                total.append(sum(Bill.objects.filter(Date_Create__day=x + 1, Date_Create__month=int(month_input),
                                                     Date_Create__year=int(year_input), Active=True).values_list(
                    'Total_Money',
                    flat=True)))
        else:
            day_in_month = monthrange(timezone.now().year, timezone.now().month)[1]
            for x in range(day_in_month):
                labels.append(x + 1)
                total.append(sum(Bill.objects.filter(Date_Create__day=x + 1, Date_Create__month=timezone.now().month,
                                                     Date_Create__year=timezone.now().year, Active=True).values_list(
                    'Total_Money',
                    flat=True)))
        data = {
            'labels': labels,
            'data': total,
            'status': True,
            'time': 'today'
        }
        return Response(data)


# year
class BillYear(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        labels = ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6', 'Tháng 7', 'Tháng 8', 'Tháng 9',
                  'Tháng 10', 'Tháng 11', 'Tháng 12']
        bill = []
        for x in range(1, 13):
            bill.append(
                Bill.objects.filter(Date_Create__month=x, Date_Create__year=timezone.now().year, Active=True).count())
        data = {
            'labels': labels,
            'data': bill,
            'status': True,
        }
        return Response(data)


class ProductYear(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        quality = []
        product_list = Bill_Product.objects.filter(Bill__Date_Create__year=timezone.now().year,
                                                   Bill__Active=True).values_list(
            'Product__title',
            flat=True).distinct()
        for x in product_list:
            item = Bill_Product.objects.filter(Product__title=x,
                                               Bill__Date_Create__year=timezone.now().year,
                                               Bill__Active=True).values_list(
                'Quality',
                flat=True)
            item = sum(item)
            quality.append(item)
        data = {
            'labels': product_list,
            'data': quality,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class ServiceYear(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        quality = []
        service_list = Bill_Service.objects.filter(Bill__Date_Create__year=timezone.now().year,
                                                   Bill__Active=True).values_list(
            'Service__title',
            flat=True).distinct()
        for x in service_list:
            item = Bill_Service.objects.filter(Service__title=x,
                                               Bill__Date_Create__year=timezone.now().year,
                                               Bill__Active=True).values_list(
                'Quality',
                flat=True)
            item = sum(item)
            quality.append(item)
        data = {
            'labels': service_list,
            'data': quality,
            'status': True,
            'time': 'today'
        }
        return Response(data)


class MoneyYear(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        labels = ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6', 'Tháng 7', 'Tháng 8', 'Tháng 9',
                  'Tháng 10', 'Tháng 11', 'Tháng 12']
        total = []
        for x in range(1, 13):
            total.append(sum(
                Bill.objects.filter(Date_Create__month=x, Date_Create__year=timezone.now().year,
                                    Active=True).values_list(
                    'Total_Money', flat=True)))
        data = {
            'labels': labels,
            'data': total,
            'status': True,
            'time': 'today'
        }
        return Response(data)
