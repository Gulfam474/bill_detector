from django.urls import path
from .views import BillCompareView

urlpatterns = [
    path('upload/', BillCompareView.as_view(), name='bill-upload'),
]

