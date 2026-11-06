from django.urls import path

from services import views

urlpatterns = [
    path('soap/country/', views.CountryInfoSoapView.as_view(), name='soap_country'),
]
