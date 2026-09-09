# TODO List API

API REST para gerenciamento de tarefas e cadastro de usuários, construída com Django, Django REST Framework e SimpleJWT. O projeto permite criar, listar, editar, atualizar parcialmente e excluir tarefas, além de registrar usuários usando uma API baseada em JSON.

## Tecnologias

- Python
- Django 6.0.7
- Django REST Framework
- djangorestframework-simplejwt
- SQLite

## Funcionalidades

- Criar tarefas
- Listar todas as tarefas
- Buscar tarefas por trecho do título
- Atualizar uma tarefa completamente com `PUT`
- Atualizar apenas alguns campos com `PATCH`
- Excluir tarefas
- Validar título e status
- Retornar `404 Not Found` quando a tarefa não existe
- Registrar usuários com username, email e senha
- Validar confirmação e força da senha
- Usar um modelo de usuário customizado
- Configurar autenticação JWT e permissões autenticadas por padrão

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
├── tarefas/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
└── usuarios/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── tests.py
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
pip install django djangorestframework djangorestframework-simplejwt
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
| `GET` | `/tarefas/<titulo>/` | Busca tarefas cujo título contém o texto informado |
| `PUT` | `/tarefas/<id>/` | Substitui os dados editáveis da tarefa |
| `PATCH` | `/tarefas/<id>/` | Atualiza parcialmente uma tarefa |
| `DELETE` | `/tarefas/<id>/` | Exclui uma tarefa |
| `POST` | `/autenticacao/registro/` | Registra um novo usuário |

Todos os endpoints recebem e retornam JSON quando aplicável.

O cadastro de usuário não exige autenticação. Os endpoints de tarefas também
definem `AllowAny` explicitamente; os demais endpoints usam a permissão global
`IsAuthenticated` configurada no projeto.

## Cadastro de usuário

Envie `username`, `email`, `password` e `confirm_password` para registrar um
usuário. O email deve ser único, o username deve ter pelo menos três caracteres
e a senha precisa passar pelos validadores de senha do Django.

```bash
curl -X POST http://127.0.0.1:8000/autenticacao/registro/ \
	-H "Content-Type: application/json" \
	-d '{"username":"usuario_teste","email":"usuario@example.com","password":"SenhaForte123!","confirm_password":"SenhaForte123!"}'
```

O campo `password` nunca é retornado na resposta. A senha é armazenada usando
o hashing padrão do Django.

O projeto usa `usuarios.CustomUser` como modelo de usuário e configura
`JWTAuthentication` como autenticação padrão do Django REST Framework. Os
tokens JWT ainda não possuem endpoints próprios neste projeto.

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

### Buscar tarefas por título

A busca não diferencia letras maiúsculas de minúsculas e retorna todas as tarefas cujo título contém o trecho informado:

```bash
curl http://127.0.0.1:8000/tarefas/django/
```

O resultado é uma lista de tarefas com `id`, `titulo`, `status` e `data_criacao`. Para títulos com espaços ou caracteres especiais, codifique o valor na URL.

### Atualização completa com `PUT`

No `PUT`, envie os campos obrigatórios do serializer de atualização:

O campo `data_criacao` também faz parte da representação de atualização, mas é somente leitura e não deve ser enviado para alteração.

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

### Usuário

- `username` é removido dos espaços no início e no fim.
- Deve ter pelo menos 3 caracteres.
- `email` é obrigatório, válido e único.
- `password` e `confirm_password` devem ser iguais.
- A senha deve atender aos validadores configurados no Django.

## Respostas de erro

- `400 Bad Request`: dados inválidos no corpo da requisição.
- `404 Not Found`: tarefa não encontrada para o identificador informado.
- `405 Method Not Allowed`: método HTTP não disponível para o endpoint.
- `401 Unauthorized`: autenticação ausente ou token JWT inválido em endpoints protegidos.

## Testes

Os testes podem ser executados com:

```powershell
python manage.py test
```

A suíte usa `APITestCase` e cobre os endpoints de tarefas e o cadastro de
usuários, incluindo:

- Listagem com e sem tarefas.
- Criação com dados válidos, título ausente ou inválido e status não permitido na criação.
- Atualização completa com `PUT` e atualização parcial com `PATCH`.
- Rejeição de `PUT` incompleto e de dados inválidos na atualização.
- Busca por trecho do título e busca sem resultados.
- Exclusão de tarefas.
- Acesso a tarefa inexistente e uso de método HTTP não permitido.
- Registro de usuário com dados válidos e verificação do hashing da senha.
- Remoção de espaços do username e rejeição de username curto.
- Rejeição de senhas diferentes ou fracas.
- Rejeição de email duplicado ou inválido.

O comando deve terminar com todos os testes aprovados e sem problemas na checagem do Django:

```powershell
python manage.py check
```

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
- Os endpoints de tarefas e o cadastro usam `AllowAny` explicitamente.
- A autenticação JWT está configurada, mas os endpoints de emissão e renovação de tokens ainda não foram adicionados.
- O projeto não possui ainda documentação OpenAPI/Swagger.