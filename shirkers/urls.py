from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<vat_id>\d{8})/', views.CompanyView.as_view(),
        name='company_view'),
    url(r'^', views.Home.as_view(), name='home'),
]
