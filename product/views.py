from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from product.models import Product, Service


@login_required
def product(request):
    product_list = Product.objects.all()
    context = {
        'product': product_list
    }
    return render(request, 'product.html', context)


@login_required
def service(request):
    service_list = Service.objects.all()
    context = {
        'service': service_list
    }
    return render(request, 'service.html', context)
