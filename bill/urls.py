from django.urls import path

from bill import views

urlpatterns = [
    path('', views.bill, name='bill'),
    path('details-bill/<id>/', views.details_bill, name='detail-ajax'),
    path('details/<id>/', views.load_details, name='detail-load'),
    path('add-bill/', views.add_bill, name='add-bill'),
    path('update-bill/<id>/', views.update_bill, name='update-bill'),
    # api
    path('api-bill-day/', views.BillDay.as_view(), name='bill-day'),
    path('api-bill-day-custom/', views.BillDayCustom.as_view(), name='bill-day-custom'),
    path('api-bill-week/', views.BillWeek.as_view(), name='bill-week'),
    path('api-bill-month/', views.BillMonth.as_view(), name='bill-month'),
    path('api-bill-year/', views.BillYear.as_view(), name='bill-year'),

    path('api-product-day/', views.ProductDay.as_view(), name='product-day'),
    path('api-product-day-custom/', views.ProductDayCustom.as_view(), name='product-day-custom'),
    path('api-product-week/', views.ProductWeek.as_view(), name='product-week'),
    path('api-product-month/', views.ProductMonth.as_view(), name='product-month'),
    path('api-product-year/', views.ProductYear.as_view(), name='product-year'),

    path('api-service-day/', views.ServiceDay.as_view(), name='service-day'),
    path('api-service-day-custom/', views.ServiceDayCustom.as_view(), name='service-day-custom'),
    path('api-service-week/', views.ServiceWeek.as_view(), name='service-week'),
    path('api-service-month/', views.ServiceMonth.as_view(), name='service-month'),
    path('api-service-year/', views.ServiceYear.as_view(), name='service-year'),

    path('api-money-day/', views.MoneyDay.as_view(), name='money-day'),
    path('api-money-day-custom/', views.MoneyDayCustom.as_view(), name='money-day-custom'),
    path('api-money-week/', views.MoneyWeek.as_view(), name='money-week'),
    path('api-money-month/', views.MoneyMonth.as_view(), name='money-month'),
    path('api-money-year/', views.MoneyYear.as_view(), name='money-year'),
]
