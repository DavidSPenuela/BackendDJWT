from rest_framework.test import APITestCase

from users.models import User

ADMIN_PASS = 'AdminSegura#2024'
LECTOR_PASS = 'LectorSegura#2024'


class UserSecurityTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@biblioteca.mx', password=ADMIN_PASS)
        self.lector = User.objects.create_user(
            username='lector', email='lector@biblioteca.mx', password=LECTOR_PASS,
            matricula='A0001', first_name='Ana')

    def login(self, email, password):
        resp = self.client.post('/api/v1/auth/token/', {'email': email, 'password': password}, format='json')
        self.assertEqual(resp.status_code, 200, resp.content)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")
        return resp.data

    def test_login_devuelve_access_y_refresh(self):
        data = self.login('lector@biblioteca.mx', LECTOR_PASS)
        self.assertIn('access', data)
        self.assertIn('refresh', data)

    def test_datos_personales_sin_password_y_con_matricula(self):
        self.login('lector@biblioteca.mx', LECTOR_PASS)
        resp = self.client.get('/api/v1/auth/me/')
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('password', resp.data)
        self.assertEqual(resp.data['matricula'], 'A0001')

    def test_datos_personales_requieren_token(self):
        self.assertEqual(self.client.get('/api/v1/auth/me/').status_code, 401)

    def test_lista_y_detalle_no_exponen_password(self):
        self.login('admin@biblioteca.mx', ADMIN_PASS)
        lista = self.client.get('/api/v1/users/')
        self.assertEqual(lista.status_code, 200)
        for u in lista.data:
            self.assertNotIn('password', u)
        detalle = self.client.get(f'/api/v1/users/{self.lector.id}/')
        self.assertNotIn('password', detalle.data)

    def test_usuario_normal_no_puede_usar_el_crud(self):
        self.login('lector@biblioteca.mx', LECTOR_PASS)
        self.assertEqual(self.client.get('/api/v1/users/').status_code, 403)

    def test_crear_usuario_hashea_password_y_no_la_devuelve(self):
        self.login('admin@biblioteca.mx', ADMIN_PASS)
        resp = self.client.post('/api/v1/users/', {
            'username': 'nuevo', 'email': 'nuevo@biblioteca.mx',
            'password': 'NuevoSegura#2024', 'matricula': 'B0002',
        }, format='json')
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertNotIn('password', resp.data)
        nuevo = User.objects.get(email='nuevo@biblioteca.mx')
        self.assertTrue(nuevo.check_password('NuevoSegura#2024'))
        self.assertNotEqual(nuevo.password, 'NuevoSegura#2024')

    def test_crear_usuario_sin_password_falla(self):
        self.login('admin@biblioteca.mx', ADMIN_PASS)
        resp = self.client.post('/api/v1/users/', {
            'username': 'x', 'email': 'x@biblioteca.mx'}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_editar_sin_password_NO_cambia_la_contrasena(self):
        """Prueba central: el admin edita a otro usuario sin enviar password."""
        self.login('admin@biblioteca.mx', ADMIN_PASS)
        hash_lector = self.lector.password
        hash_admin = self.admin.password

        resp = self.client.patch(f'/api/v1/users/{self.lector.id}/',
                                 {'first_name': 'Ana María'}, format='json')
        self.assertEqual(resp.status_code, 200, resp.content)
        self.lector.refresh_from_db()
        self.admin.refresh_from_db()

        self.assertEqual(self.lector.first_name, 'Ana María')
        self.assertEqual(self.lector.password, hash_lector)      # no cambió
        self.assertTrue(self.lector.check_password(LECTOR_PASS))  # sigue siendo la suya
        self.assertEqual(self.admin.password, hash_admin)
        self.assertFalse(self.lector.check_password(ADMIN_PASS))  # no heredó la del admin

    def test_put_sin_password_tampoco_cambia_la_contrasena(self):
        self.login('admin@biblioteca.mx', ADMIN_PASS)
        hash_lector = self.lector.password
        resp = self.client.put(f'/api/v1/users/{self.lector.id}/', {
            'username': 'lector', 'email': 'lector@biblioteca.mx', 'matricula': 'A0001',
        }, format='json')
        self.assertEqual(resp.status_code, 200, resp.content)
        self.lector.refresh_from_db()
        self.assertEqual(self.lector.password, hash_lector)

    def test_editar_con_password_si_la_cambia(self):
        self.login('admin@biblioteca.mx', ADMIN_PASS)
        resp = self.client.patch(f'/api/v1/users/{self.lector.id}/',
                                 {'password': 'OtraClave#2024'}, format='json')
        self.assertEqual(resp.status_code, 200, resp.content)
        self.lector.refresh_from_db()
        self.assertTrue(self.lector.check_password('OtraClave#2024'))
        self.assertFalse(self.lector.check_password(LECTOR_PASS))
