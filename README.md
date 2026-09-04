# TODO List API

API REST para gerenciamento de tarefas, construída com Django e Django REST Framework. O projeto permite criar, listar, editar, atualizar parcialmente e excluir tarefas usando uma API simples baseada em JSON.

## Tecnologias

- Python
- Django 6.0.7
- Django REST Framework
- SQLite

## Funcionalidades

- Criar tarefas
- Listar todas as tarefas
- Atualizar uma tarefa completamente com `PUT`
- Atualizar apenas alguns campos com `PATCH`
- Excluir tarefas
- Validar título e status
- Retornar `404 Not Found` quando a tarefa não existe

## Estrutura do projeto

```text
learn_api/
├── manage.py
├── db.sqlite3
├── README.md
├── TODO_LIST_API/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── tarefas/
		├── models.py
		├── serializers.py
		├── views.py
		├── urls.py
		├── admin.py
		└── migrations/
```

## Pré-requisitos

- Python 3.12 ou superior
- `pip`
- Ambiente virtual recomendado

## Instalação

No Windows PowerShell:

```powershell
git clone <url-do-repositorio>
cd learn_api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install django djangorestframework
python manage.py migrate
```

> Caso o PowerShell bloqueie a ativação do ambiente virtual, execute `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` na sessão atual e tente novamente.

## Executando a aplicação

```powershell
python manage.py runserver
```

A API ficará disponível em:

```text
http://127.0.0.1:8000/
```

O painel administrativo está em `http://127.0.0.1:8000/admin/`.

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/tarefas/` | Lista todas as tarefas |
| `POST` | `/tarefas/` | Cria uma tarefa |
| `PUT` | `/tarefas/<id>/` | Substitui os dados editáveis da tarefa |
| `PATCH` | `/tarefas/<id>/` | Atualiza parcialmente uma tarefa |
| `DELETE` | `/tarefas/<id>/` | Exclui uma tarefa |

Todos os endpoints recebem e retornam JSON quando aplicável.

## Modelo de tarefa

| Campo | Tipo | Obrigatório | Observações |
|---|---|---:|---|
| `id` | inteiro | Não | Gerado automaticamente e somente leitura |
| `titulo` | string | Sim | Entre 3 e 200 caracteres, sem espaços nas extremidades |
| `status` | string | Não | `P` (pendente), `A` (andamento) ou `F` (feito) |
| `data_criacao` | data | Não | Gerada automaticamente na criação |

O status padrão de uma nova tarefa é `P`.

## Exemplos de uso

### Criar uma tarefa

```bash
curl -X POST http://127.0.0.1:8000/tarefas/ \
	-H "Content-Type: application/json" \
	-d '{"titulo":"Estudar Django","status":"P"}'
```

Resposta esperada:

```json
{
	"mensagem": "Tarefa criada com sucesso!"
}
```

### Listar tarefas

```bash
curl http://127.0.0.1:8000/tarefas/
```

### Atualização completa com `PUT`

No `PUT`, envie os campos obrigatórios do serializer de atualização:

```bash
curl -X PUT http://127.0.0.1:8000/tarefas/1/ \
	-H "Content-Type: application/json" \
	-d '{"titulo":"Estudar Django REST Framework","status":"A"}'
```

### Atualização parcial com `PATCH`

Use `PATCH` quando quiser alterar somente um campo. O `partial=True` é aplicado na view:

```bash
curl -X PATCH http://127.0.0.1:8000/tarefas/1/ \
	-H "Content-Type: application/json" \
	-d '{"status":"F"}'
```

Nesse caso, `titulo` não precisa ser enviado.

### Excluir uma tarefa

```bash
curl -X DELETE http://127.0.0.1:8000/tarefas/1/
```

## Validações

### Título

- É removido o espaço em branco no início e no fim.
- Não pode ficar vazio.
- Deve ter pelo menos 3 caracteres.
- Deve ter no máximo 200 caracteres.

### Status

O valor deve ser um dos seguintes:

- `P`: pendente
- `A`: andamento
- `F`: feito

## Respostas de erro

- `400 Bad Request`: dados inválidos no corpo da requisição.
- `404 Not Found`: tarefa não encontrada para o identificador informado.

## Testes

Os testes podem ser executados com:

```powershell
python manage.py test
```

Atualmente, a estrutura de testes existe, mas ainda não contém casos automatizados para os endpoints.

## Configuração para produção

O projeto está configurado para desenvolvimento. Antes de publicar a aplicação, revise pelo menos:

- `DEBUG = False`
- `SECRET_KEY` em variável de ambiente
- `ALLOWED_HOSTS` com os domínios permitidos
- banco de dados apropriado para produção
- autenticação e permissões da API
- HTTPS e configurações de segurança do Django

## Observações atuais

- O banco padrão é o SQLite, armazenado em `db.sqlite3`.
- Os endpoints usam `AllowAny`; não há autenticação implementada.
- O projeto não possui ainda documentação OpenAPI/Swagger.