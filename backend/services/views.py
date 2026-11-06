"""Consumo de un Web Service SOAP público con zeep.

Servicio usado: CountryInfoService (oorsprong.org). La operación FullCountryInfo recibe
un código ISO de país (MX, US, ES...) y regresa nombre, capital, moneda, idiomas, etc.
"""
import re
from functools import lru_cache

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from requests.exceptions import RequestException
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from zeep import Client
from zeep.exceptions import Error as ZeepError
from zeep.helpers import serialize_object
from zeep.transports import Transport


@lru_cache(maxsize=1)
def get_client():
    """Crea (una sola vez) el cliente SOAP; descargar el WSDL en cada petición sería lento."""
    transport = Transport(timeout=10, operation_timeout=15)
    return Client(settings.SOAP_COUNTRY_WSDL, transport=transport)


def _languages(data):
    langs = data.get('Languages') or {}
    items = langs.get('tLanguage') if isinstance(langs, dict) else langs
    if isinstance(items, dict):
        items = [items]
    return [i.get('sName') for i in (items or []) if isinstance(i, dict) and i.get('sName')]


class CountryInfoSoapView(APIView):
    """Consulta información de un país a través de un servicio SOAP (protegido con JWT)."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Consume el servicio SOAP CountryInfoService (zeep) y devuelve el resultado como JSON.',
        manual_parameters=[openapi.Parameter(
            'code', openapi.IN_QUERY, description='Código ISO de 2 letras (ej. MX, US, ES)',
            type=openapi.TYPE_STRING, required=True)],
    )
    def get(self, request):
        code = request.query_params.get('code', '').strip().upper()
        if not re.fullmatch(r'[A-Z]{2}', code):
            return Response({'detail': 'El parámetro "code" debe ser un código ISO de 2 letras (ej. MX).'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            result = get_client().service.FullCountryInfo(sCountryISOCode=code)
        except (ZeepError, RequestException) as exc:
            return Response({'detail': f'El servicio SOAP no está disponible: {exc}'},
                            status=status.HTTP_502_BAD_GATEWAY)

        data = serialize_object(result)
        if not data or str(data.get('sName', '')).startswith('Country not found'):
            return Response({'detail': f'No se encontró el país con código {code}.'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({
            'source': 'SOAP - CountryInfoService (zeep)',
            'code': data.get('sISOCode'),
            'name': data.get('sName'),
            'capital': data.get('sCapitalCity'),
            'phone_code': data.get('sPhoneCode'),
            'continent_code': data.get('sContinentCode'),
            'currency': data.get('sCurrencyISOCode'),
            'flag': data.get('sCountryFlag'),
            'languages': _languages(data),
        })
