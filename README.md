# TODO List API

API REST para gerenciamento de tarefas e cadastro de usuários, construída com Django, Django REST Framework e SimpleJWT. O projeto oferece cadastro de usuários, autenticação JWT e operações CRUD para tarefas.

## Tecnologias

- Python
- Django 6.0.7
- Django REST Framework
- djangorestframework-simplejwt
- SQLite

## Funcionalidades

- Criar, listar e buscar tarefas do usuário autenticado
- Atualizar tarefas com `PUT` e `PATCH`
- Excluir tarefas
- Associar cada tarefa ao usuário que a criou
- Validar título e status
- Registrar usuários com `username`, `email`, `password` e `confirm_password`
- Validar força da senha e confirmação
- Usar `CustomUser` como modelo de autenticação
- Fazer login com `username` ou `email` e receber tokens JWT
- Configurar `JWTAuthentication` como autenticação padrão do DRF

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
| `GET` | `/tarefas/` | Lista as tarefas do usuário autenticado |
| `POST` | `/tarefas/` | Cria uma tarefa para o usuário autenticado |
| `GET` | `/tarefas/<titulo>/` | Busca tarefas do usuário autenticado por trecho do título |
| `PUT` | `/tarefas/<id>/` | Atualiza totalmente uma tarefa do usuário autenticado |
| `PATCH` | `/tarefas/<id>/` | Atualiza parcialmente uma tarefa do usuário autenticado |
| `DELETE` | `/tarefas/<id>/` | Exclui uma tarefa do usuário autenticado |
| `POST` | `/autenticacao/registro/` | Registra um usuário |
| `POST` | `/autenticacao/login/` | Gera tokens JWT com login via username ou email |
| `POST` | `/autenticacao/refresh/` | Gera um novo access token usando um refresh token válido |

## Autenticação e permissões

O projeto usa `JWTAuthentication` como autenticação padrão no DRF. Os endpoints de tarefas exigem um access token JWT válido.

Em outras palavras:

- `/autenticacao/registro/` é público
- `/autenticacao/login/` é público
- `/autenticacao/refresh/` é público e exige um refresh token válido
- `/tarefas/` e `/tarefas/<id>/` exigem autenticação
- uma tarefa só pode ser listada, buscada, alterada ou excluída pelo usuário ao qual pertence
- o usuário da tarefa é preenchido automaticamente a partir do token JWT e não deve ser enviado no corpo da requisição

Para acessar os endpoints de tarefas, envie o access token no cabeçalho:

```text
Authorization: Bearer <token_access>
```

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
`JWTAuthentication` como autenticação padrão do Django REST Framework. O login
é feito por `CustomTokenObtainPairView`, que aceita `username` ou `email`.

## Login com JWT

O endpoint de login aceita `username` ou `email` no campo `username` e retorna
`access` e `refresh`.

```bash
curl -X POST http://127.0.0.1:8000/autenticacao/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"usuario_teste","password":"SenhaForte123!"}'
```

ou

```bash
curl -X POST http://127.0.0.1:8000/autenticacao/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"usuario@example.com","password":"SenhaForte123!"}'
```

Resposta esperada:

```json
{
  "refresh": "<token_refresh>",
  "access": "<token_access>"
}
```

## Renovação do access token

Quando o access token expirar, envie o refresh token para obter um novo access
token:

```bash
curl -X POST http://127.0.0.1:8000/autenticacao/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<token_refresh>"}'
```

Resposta esperada:

```json
{
  "access": "<novo_token_access>"
}
```

Um refresh token inválido ou expirado é rejeitado pela API.

## Modelo de tarefa

| Campo | Tipo | Obrigatório | Observações |
|---|---|---:|---|
| `id` | inteiro | Não | Gerado automaticamente e somente leitura |
| `titulo` | string | Sim | Entre 3 e 200 caracteres, sem espaços nas extremidades |
| `status` | string | Não | `P` (pendente), `A` (andamento) ou `F` (feito) |
| `data_criacao` | data | Não | Gerada automaticamente na criação |
| `usuario` | relação com usuário | Sim | Preenchido automaticamente com o usuário autenticado |

O status padrão de uma nova tarefa é `P`.

## Exemplos de uso

### Criar uma tarefa

```bash
curl -X POST http://127.0.0.1:8000/tarefas/ \
	-H "Content-Type: application/json" \
  -H "Authorization: Bearer <token_access>" \
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
curl http://127.0.0.1:8000/tarefas/ \
  -H "Authorization: Bearer <token_access>"
```

### Buscar tarefas por título

A busca não diferencia letras maiúsculas de minúsculas e retorna todas as tarefas cujo título contém o trecho informado:

```bash
curl http://127.0.0.1:8000/tarefas/django/ \
  -H "Authorization: Bearer <token_access>"
```

O resultado é uma lista de tarefas com `id`, `titulo`, `status` e `data_criacao`. Para títulos com espaços ou caracteres especiais, codifique o valor na URL.

### Atualização completa com `PUT`

No `PUT`, envie os campos obrigatórios do serializer de atualização:

O campo `data_criacao` também faz parte da representação de atualização, mas é somente leitura e não deve ser enviado para alteração.

```bash
curl -X PUT http://127.0.0.1:8000/tarefas/1/ \
	-H "Content-Type: application/json" \
  -H "Authorization: Bearer <token_access>" \
	-d '{"titulo":"Estudar Django REST Framework","status":"A"}'
```

### Atualização parcial com `PATCH`

Use `PATCH` quando quiser alterar somente um campo. O `partial=True` é aplicado na view:

```bash
curl -X PATCH http://127.0.0.1:8000/tarefas/1/ \
	-H "Content-Type: application/json" \
  -H "Authorization: Bearer <token_access>" \
	-d '{"status":"F"}'
```

Nesse caso, `titulo` não precisa ser enviado.

### Excluir uma tarefa

```bash
curl -X DELETE http://127.0.0.1:8000/tarefas/1/ \
  -H "Authorization: Bearer <token_access>"
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

A suíte atual cobre:

- listagem de tarefas vazia e com registros
- rejeição de requisições sem autenticação
- listagem e busca limitadas às tarefas do usuário autenticado
- rejeição de alteração ou exclusão de tarefa de outro usuário
- criação com dados válidos
- criação inválida com título ausente, título curto, título longo e status inválido
- atualização completa com `PUT`
- atualização parcial com `PATCH`
- rejeição de `PUT` incompleto
- rejeição de método HTTP não permitido
- tentativa de atualizar tarefa inexistente
- busca por título com e sem resultados
- exclusão de tarefa
- registro de usuário com dados válidos
- validação de `username`, `email`, `password` e `confirm_password`
- login com `username` e com `email`
- rejeição de credenciais inválidas
- renovação de access token com refresh token válido
- rejeição de refresh token inválido

Verificação do Django:

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

- o banco padrão é SQLite em `db.sqlite3`
- o projeto usa `CustomUser` em `usuarios/models.py`
- registro, login e renovação de token são públicos; os endpoints de tarefas exigem autenticação
- cada usuário acessa somente as próprias tarefas
- os tokens JWT são emitidos via endpoint customizado de login
- ainda não há documentação OpenAPI/Swagger