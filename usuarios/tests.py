from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrarUsuarioTests(APITestCase):
	url = '/autenticacao/registro/'

	def dados_usuario(self, **alteracoes):
		dados = {
			'username': 'usuario_teste',
			'email': 'usuario@example.com',
			'password': 'SenhaForte123!',
			'confirm_password': 'SenhaForte123!',
		}
		dados.update(alteracoes)
		return dados

	def test_registra_usuario_com_dados_validos(self):
		response = self.client.post(self.url, self.dados_usuario(), format='json')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		usuario = get_user_model().objects.get(username='usuario_teste')
		self.assertEqual(usuario.email, 'usuario@example.com')
		self.assertTrue(usuario.check_password('SenhaForte123!'))
		self.assertNotIn('password', response.data)
		self.assertNotIn('confirm_password', response.data)

	def test_rejeita_username_com_menos_de_tres_caracteres(self):
		response = self.client.post(
			self.url,
			self.dados_usuario(username='ab'),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('username', response.data)

	def test_remove_espacos_do_username(self):
		response = self.client.post(
			self.url,
			self.dados_usuario(username='  usuario_teste  '),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(
			get_user_model().objects.filter(username='usuario_teste').exists()
		)

	def test_rejeita_senhas_diferentes(self):
		response = self.client.post(
			self.url,
			self.dados_usuario(confirm_password='SenhaDiferente123!'),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('non_field_errors', response.data)

	def test_rejeita_senha_fraca(self):
		response = self.client.post(
			self.url,
			self.dados_usuario(password='123', confirm_password='123'),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('non_field_errors', response.data)

	def test_rejeita_email_duplicado(self):
		get_user_model().objects.create_user(
			username='outro_usuario',
			email='usuario@example.com',
			password='SenhaForte123!',
		)

		response = self.client.post(self.url, self.dados_usuario(), format='json')

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('email', response.data)

	def test_rejeita_email_invalido(self):
		response = self.client.post(
			self.url,
			self.dados_usuario(email='email-invalido'),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('email', response.data)
