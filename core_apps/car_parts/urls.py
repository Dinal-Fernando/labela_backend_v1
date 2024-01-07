from django.urls import re_path
from core_apps.car_parts.views import ProductView

urlpatterns = [
    re_path(r'^product/?(?P<product_id>[\d]+)?/$', ProductView.as_view(), name='product'),
]

