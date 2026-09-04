from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Tarefa


class TarefaAPITestCase(APITestCase):
    list_create_url = reverse('List-Create')

    def criar_tarefa(self, titulo='Estudar', tarefa_status='P'):
        return Tarefa.objects.create(titulo=titulo, status=tarefa_status)

    def test_lista_tarefas_vazia(self):
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_lista_tarefas_retorna_tarefas(self):
        tarefa = self.criar_tarefa()

        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], tarefa.id)
        self.assertEqual(response.data[0]['titulo'], tarefa.titulo)
        self.assertEqual(response.data[0]['status'], tarefa.status)

    def test_cria_tarefa_com_dados_validos(self):
        response = self.client.post(
            self.list_create_url,
            {'titulo': '  Estudar Django  ', 'status': 'P'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'mensagem': 'Tarefa criada com sucesso!'})
        tarefa = Tarefa.objects.get()
        self.assertEqual(tarefa.titulo, 'Estudar Django')
        self.assertEqual(tarefa.status, 'P')

    def test_nao_cria_tarefa_com_titulo_ausente(self):
        response = self.client.post(
            self.list_create_url, {'status': 'P'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Tarefa.objects.count(), 0)

    def test_nao_cria_tarefa_com_titulo_invalido(self):
        for titulo in ('  ', 'ab', 'a' * 201):
            with self.subTest(titulo=titulo):
                response = self.client.post(
                    self.list_create_url,
                    {'titulo': titulo, 'status': 'P'},
                    format='json',
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Tarefa.objects.count(), 0)

    def test_nao_cria_tarefa_com_status_diferente_de_pendente(self):
        response = self.client.post(
            self.list_create_url,
            {'titulo': 'Estudar', 'status': 'A'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Tarefa.objects.count(), 0)

    def test_atualiza_tarefa_com_put(self):
        tarefa = self.criar_tarefa()
        url = reverse('Update-Delete', kwargs={'id': tarefa.id})

        response = self.client.put(
            url, {'titulo': 'Praticar APIs', 'status': 'A'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'mensagem': 'Tarefa editada com sucesso!'})
        tarefa.refresh_from_db()
        self.assertEqual(tarefa.titulo, 'Praticar APIs')
        self.assertEqual(tarefa.status, 'A')

    def test_atualiza_parcialmente_tarefa_com_patch(self):
        tarefa = self.criar_tarefa()
        url = reverse('Update-Delete', kwargs={'id': tarefa.id})

        response = self.client.patch(url, {'status': 'F'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tarefa.refresh_from_db()
        self.assertEqual(tarefa.titulo, 'Estudar')
        self.assertEqual(tarefa.status, 'F')

    def test_nao_atualiza_com_put_incompleto(self):
        tarefa = self.criar_tarefa()
        url = reverse('Update-Delete', kwargs={'id': tarefa.id})

        response = self.client.put(url, {'status': 'A'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        tarefa.refresh_from_db()
        self.assertEqual(tarefa.status, 'P')

    def test_rejeita_metodo_nao_permitido_no_detalhe(self):
        tarefa = self.criar_tarefa()
        url = reverse('Update-Delete', kwargs={'id': tarefa.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_nao_atualiza_tarefa_inexistente(self):
        url = reverse('Update-Delete', kwargs={'id': 999})

        for metodo in ('put', 'patch', 'delete'):
            with self.subTest(metodo=metodo):
                response = getattr(self.client, metodo)(
                    url,
                    {'titulo': 'Nova tarefa', 'status': 'A'}
                    if metodo != 'delete' else None,
                    format='json',
                )
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rejeita_dados_invalidos_na_atualizacao(self):
        tarefa = self.criar_tarefa()
        url = reverse('Update-Delete', kwargs={'id': tarefa.id})

        response = self.client.patch(url, {'status': 'X'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        tarefa.refresh_from_db()
        self.assertEqual(tarefa.status, 'P')

    def test_apaga_tarefa(self):
        tarefa = self.criar_tarefa()
        url = reverse('Update-Delete', kwargs={'id': tarefa.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'mensagem': 'Tarefa apagada com sucesso!'})
        self.assertFalse(Tarefa.objects.filter(id=tarefa.id).exists())

    def test_busca_tarefas_por_titulo(self):
        self.criar_tarefa('Estudar Django')
        self.criar_tarefa('Fazer exercicios')

        response = self.client.get(reverse('Retrieve', kwargs={'titulo': 'django'}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['titulo'], 'Estudar Django')

    def test_busca_titulo_sem_resultados(self):
        response = self.client.get(reverse('Retrieve', kwargs={'titulo': 'inexistente'}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])









