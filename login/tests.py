from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User

from .models import PasswordResetToken


class RecuperacionClaveTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            email='residente@correo.com',
            password='ClaveAnterior123',
            status='active',
        )
        self.url_solicitud = reverse('recuperar_clave')
        self.url_restablecer = reverse('restablecer_clave')

    def _crear_token(self, minutos_extra=30, usado=False):
        token = PasswordResetToken.objects.create(
            user=self.usuario,
            token='a' * 64,
            expires_at=timezone.now() + timedelta(minutes=minutos_extra),
            used_at=timezone.now() if usado else None,
        )
        return token

    @patch('login.views.enviar_correo_recuperacion')
    def test_solicitud_con_correo_existente_crea_token_y_envia_email(self, mock_correo):
        respuesta = self.client.post(self.url_solicitud, {'email': self.usuario.email})

        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'login/recuperar_clave.html')
        self.assertTrue(respuesta.context['enviado'])
        self.assertEqual(PasswordResetToken.objects.filter(user=self.usuario).count(), 1)
        mock_correo.assert_called_once()

    @patch('login.views.enviar_correo_recuperacion')
    def test_solicitud_con_correo_inexistente_es_generica(self, mock_correo):
        respuesta = self.client.post(self.url_solicitud, {'email': 'noexiste@correo.com'})

        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(respuesta.context['enviado'])
        self.assertEqual(PasswordResetToken.objects.count(), 0)
        mock_correo.assert_not_called()

    @patch('login.views.enviar_correo_recuperacion')
    def test_solicitud_invalida_tokens_anteriores(self, mock_correo):
        self._crear_token()
        self.client.post(self.url_solicitud, {'email': self.usuario.email})

        self.assertEqual(
            PasswordResetToken.objects.filter(user=self.usuario, used_at__isnull=True).count(),
            1,
        )

    def test_restablecer_con_token_valido_cambia_la_clave(self):
        token = self._crear_token()

        respuesta = self.client.post(self.url_restablecer, {
            'token': token.token,
            'password': 'NuevaClave123',
            'password_confirmacion': 'NuevaClave123',
        })

        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(respuesta.context['exitoso'])
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password('NuevaClave123'))
        self.assertIsNotNone(PasswordResetToken.objects.get(pk=token.pk).used_at)

        self.assertTrue(self.client.login(
            username=self.usuario.email, password='NuevaClave123'
        ))

    def test_restablecer_con_token_usado_es_rechazado(self):
        token = self._crear_token(usado=True)

        respuesta = self.client.post(self.url_restablecer, {
            'token': token.token,
            'password': 'NuevaClave123',
            'password_confirmacion': 'NuevaClave123',
        })

        self.assertFalse(respuesta.context['exitoso'])
        self.assertFalse(respuesta.context['valido'])
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password('ClaveAnterior123'))

    def test_restablecer_con_token_expirado_es_rechazado(self):
        token = self._crear_token(minutos_extra=-1)

        respuesta = self.client.post(self.url_restablecer, {
            'token': token.token,
            'password': 'NuevaClave123',
            'password_confirmacion': 'NuevaClave123',
        })

        self.assertFalse(respuesta.context['exitoso'])
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password('ClaveAnterior123'))

    def test_restablecer_sin_token_es_rechazado(self):
        respuesta = self.client.post(self.url_restablecer, {
            'token': '',
            'password': 'NuevaClave123',
            'password_confirmacion': 'NuevaClave123',
        })

        self.assertFalse(respuesta.context['exitoso'])

    def test_restablecer_con_claves_que_no_coinciden(self):
        token = self._crear_token()

        respuesta = self.client.post(self.url_restablecer, {
            'token': token.token,
            'password': 'NuevaClave123',
            'password_confirmacion': 'OtraClave123',
        })

        self.assertFalse(respuesta.context['exitoso'])
        self.assertIsNotNone(respuesta.context['error'])
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password('ClaveAnterior123'))
