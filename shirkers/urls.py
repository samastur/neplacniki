from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^embed/result/(?P<vat_id>\d{8})/', views.EmbedResult.as_view(), name='embed_result'),
    url(r'^embed/', views.Embed.as_view(), name='embed'),
    url(r'^(?P<vat_id>\d{8})/', views.CompanyView.as_view(),
        name='company_view'),
    url(r'^', views.Home.as_view(), name='home'),
]
