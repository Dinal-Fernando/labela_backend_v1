from django.urls import re_path

from core_apps.order.views import CartView, OrderView

urlpatterns = [
    re_path(r'^cart/?(?P<product_id>[\d]+)?/$', CartView.as_view(), name='product'),
    re_path(r'^order/$', OrderView.as_view(), name='order'),
]
