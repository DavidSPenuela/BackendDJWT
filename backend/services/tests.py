from unittest.mock import MagicMock, patch

from requests.exceptions import ConnectionError as RequestsConnectionError
from rest_framework.test import APITestCase
from zeep.exceptions import Error as ZeepError

from users.models import User

PASS = 'LectorSegura#2024'

FAKE_COUNTRY = {
    'sISOCode': 'MX', 'sName': 'Mexico', 'sCapitalCity': 'Mexico City', 'sPhoneCode': '52',
    'sContinentCode': 'AM', 'sCurrencyISOCode': 'MXN', 'sCountryFlag': 'http://example.com/mx.jpg',
    'Languages': {'tLanguage': [{'sISOCode': 'spa', 'sName': 'Spanish'}]},
}


class SoapEndpointTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='lector', email='lector@biblioteca.mx', password=PASS)
        resp = self.client.post('/api/v1/auth/token/', {'email': 'lector@biblioteca.mx', 'password': PASS}, format='json')
        self.token = resp.data['access']

    def auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_requiere_token(self):
        self.assertEqual(self.client.get('/api/v1/soap/country/?code=MX').status_code, 401)

    def test_codigo_invalido(self):
        self.auth()
        self.assertEqual(self.client.get('/api/v1/soap/country/?code=MEX').status_code, 400)
        self.assertEqual(self.client.get('/api/v1/soap/country/').status_code, 400)

    @patch('services.views.get_client')
    def test_respuesta_correcta(self, mock_get_client):
        client = MagicMock()
        client.service.FullCountryInfo.return_value = FAKE_COUNTRY
        mock_get_client.return_value = client
        self.auth()
        resp = self.client.get('/api/v1/soap/country/?code=mx')
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.data['name'], 'Mexico')
        self.assertEqual(resp.data['capital'], 'Mexico City')
        self.assertEqual(resp.data['languages'], ['Spanish'])
        client.service.FullCountryInfo.assert_called_once_with(sCountryISOCode='MX')

    @patch('services.views.get_client')
    def test_pais_no_encontrado(self, mock_get_client):
        client = MagicMock()
        client.service.FullCountryInfo.return_value = {'sName': 'Country not found in the database'}
        mock_get_client.return_value = client
        self.auth()
        self.assertEqual(self.client.get('/api/v1/soap/country/?code=ZZ').status_code, 404)

    @patch('services.views.get_client')
    def test_servicio_caido_devuelve_502(self, mock_get_client):
        client = MagicMock()
        client.service.FullCountryInfo.side_effect = ZeepError('boom')
        mock_get_client.return_value = client
        self.auth()
        self.assertEqual(self.client.get('/api/v1/soap/country/?code=MX').status_code, 502)
        mock_get_client.side_effect = RequestsConnectionError('sin red')
        self.assertEqual(self.client.get('/api/v1/soap/country/?code=MX').status_code, 502)
