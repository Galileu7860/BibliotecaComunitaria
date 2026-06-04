# Especificação de API — BiblioTech

> docs/api/api_specification.md  
> Projeto Aplicado Multiplataforma — Etapa 1 (N705)

---

## 1. Visão Geral

A API do BiblioTech segue o padrão **REST (REpresentational State Transfer)**, utilizando JSON como formato de troca de dados e JWT para autenticação. Todos os endpoints, exceto os de autenticação e o catálogo público, exigem o envio do token JWT no cabeçalho da requisição.

**URL Base:** `https://api.bibliotech.com.br/v1`

**Autenticação:** `Authorization: Bearer <token_jwt>`

**Formato de resposta:** `application/json`

---

## 2. Autenticação e Autorização

### 2.1 Login

**POST** `/auth/login`

Autentica o usuário e retorna um token JWT.

**Parâmetros de Requisição (Body — JSON):**

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| email | string | Sim | E-mail do usuário |
| senha | string | Sim | Senha do usuário |

**Exemplo de Requisição:**
```json
POST /auth/login
Content-Type: application/json

{
  "email": "joao@email.com",
  "senha": "minhasenha123"
}
```

**Exemplo de Resposta (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "tipo": "Bearer",
  "expiracao": "2026-03-28T18:00:00",
  "usuario": {
    "id": 1,
    "nome": "João Silva",
    "perfil": "MEMBRO"
  }
}
```

**Respostas de erro:**

| Código | Descrição |
|---|---|
| 401 | Credenciais inválidas |
| 400 | Campos obrigatórios ausentes |

---

### 2.2 Cadastro de Usuário

**POST** `/auth/cadastro`

Registra um novo membro no sistema.

**Parâmetros de Requisição (Body — JSON):**

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| nome | string | Sim | Nome completo |
| email | string | Sim | E-mail (único) |
| senha | string | Sim | Senha (mínimo 8 caracteres) |
| cpf | string | Sim | CPF sem formatação |
| telefone | string | Não | Telefone de contato |
| endereco | string | Não | Endereço completo |

**Exemplo de Resposta (201 Created):**
```json
{
  "id": 42,
  "nome": "Maria Santos",
  "email": "maria@email.com",
  "perfil": "MEMBRO",
  "ativo": true,
  "created_at": "2026-03-27T10:30:00"
}
```

---

## 3. Módulo de Acervo (Livros)

### 3.1 Listar Livros

**GET** `/livros`

Retorna a lista paginada de livros do acervo. Acessível sem autenticação.

**Parâmetros de Query (opcionais):**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| titulo | string | Filtra por título (busca parcial) |
| autor | string | Filtra por autor (busca parcial) |
| genero | string | Filtra por gênero |
| disponivel | boolean | Filtra apenas livros disponíveis |
| page | int | Número da página (padrão: 0) |
| size | int | Itens por página (padrão: 20) |

**Exemplo de Requisição:**
```
GET /livros?titulo=dom&disponivel=true&page=0&size=10
```

**Exemplo de Resposta (200 OK):**
```json
{
  "content": [
    {
      "id": 5,
      "titulo": "Dom Casmurro",
      "autor": "Machado de Assis",
      "isbn": "9788535914849",
      "genero": "Romance",
      "exemplares_disponiveis": 2,
      "exemplares_total": 3
    }
  ],
  "totalElements": 1,
  "totalPages": 1,
  "page": 0,
  "size": 10
}
```

---

### 3.2 Buscar Livro por ID

**GET** `/livros/{id}`

Retorna os dados completos de um livro.

**Exemplo de Resposta (200 OK):**
```json
{
  "id": 5,
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "isbn": "9788535914849",
  "editora": "Ática",
  "ano_publicacao": 1899,
  "genero": "Romance",
  "descricao": "Clássico da literatura brasileira...",
  "exemplares": [
    { "id": 10, "codigo_barras": "BC001", "estado": "BOM", "disponivel": true },
    { "id": 11, "codigo_barras": "BC002", "estado": "OTIMO", "disponivel": false }
  ]
}
```

---

### 3.3 Cadastrar Livro

**POST** `/livros`  
**Requer:** perfil ADMIN

**Parâmetros de Requisição (Body — JSON):**

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| titulo | string | Sim | Título da obra |
| autor | string | Sim | Nome do autor |
| isbn | string | Não | ISBN da obra |
| editora | string | Não | Nome da editora |
| ano_publicacao | int | Não | Ano de publicação |
| genero | string | Não | Gênero literário |
| descricao | string | Não | Sinopse |
| quantidade_exemplares | int | Sim | Número de cópias a cadastrar |

**Exemplo de Resposta (201 Created):**
```json
{
  "id": 20,
  "titulo": "O Cortiço",
  "autor": "Aluísio Azevedo",
  "exemplares_criados": 2
}
```

---

### 3.4 Atualizar Livro

**PUT** `/livros/{id}`  
**Requer:** perfil ADMIN

Atualiza os dados de um livro existente. Aceita os mesmos campos do cadastro.

**Resposta (200 OK):** Objeto do livro atualizado.

---

### 3.5 Excluir Livro

**DELETE** `/livros/{id}`  
**Requer:** perfil ADMIN

Remove um livro do acervo. Só é permitido se não houver exemplares com empréstimos ativos.

**Resposta (204 No Content)**

| Código | Descrição |
|---|---|
| 409 Conflict | Livro possui empréstimos ativos |

---

## 4. Módulo de Empréstimos

### 4.1 Registrar Empréstimo

**POST** `/emprestimos`  
**Requer:** perfil ADMIN

**Parâmetros de Requisição (Body — JSON):**

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| id_usuario | long | Sim | ID do membro |
| id_exemplar | long | Sim | ID do exemplar |

**Exemplo de Resposta (201 Created):**
```json
{
  "id": 88,
  "usuario": { "id": 3, "nome": "Ana Souza" },
  "exemplar": { "id": 10, "titulo": "Dom Casmurro" },
  "data_emprestimo": "2026-03-27",
  "data_prevista_devolucao": "2026-04-11",
  "status": "ATIVO"
}
```

**Respostas de erro:**

| Código | Descrição |
|---|---|
| 422 | Membro com empréstimo em atraso |
| 422 | Membro atingiu limite de 3 empréstimos simultâneos |
| 409 | Exemplar não disponível |

---

### 4.2 Registrar Devolução

**PATCH** `/emprestimos/{id}/devolucao`  
**Requer:** perfil ADMIN

**Exemplo de Resposta (200 OK):**
```json
{
  "id": 88,
  "status": "DEVOLVIDO",
  "data_devolucao": "2026-04-10",
  "devolvido_no_prazo": true
}
```

---

### 4.3 Listar Empréstimos do Membro

**GET** `/emprestimos/membro/{id_usuario}`  
**Requer:** autenticação (ADMIN vê qualquer membro; MEMBRO vê apenas o próprio)

**Parâmetros de Query:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| status | string | Filtra por status: ATIVO, DEVOLVIDO, ATRASADO |

---

## 5. Módulo de Eventos

### 5.1 Listar Eventos

**GET** `/eventos`

Retorna a lista de eventos ativos. Acessível sem autenticação.

**Exemplo de Resposta (200 OK):**
```json
{
  "content": [
    {
      "id": 3,
      "titulo": "Clube do Livro — Abril",
      "data_evento": "2026-04-15",
      "horario": "18:30",
      "local": "Sala de Leitura",
      "vagas_disponiveis": 8,
      "vagas_total": 20
    }
  ]
}
```

---

### 5.2 Inscrever-se em Evento

**POST** `/eventos/{id}/inscricao`  
**Requer:** autenticação (MEMBRO ou ADMIN)

**Exemplo de Resposta (201 Created):**
```json
{
  "id_inscricao": 14,
  "evento": "Clube do Livro — Abril",
  "data_inscricao": "2026-03-27T11:00:00"
}
```

**Respostas de erro:**

| Código | Descrição |
|---|---|
| 409 | Usuário já está inscrito neste evento |
| 422 | Evento sem vagas disponíveis |

---

### 5.3 Cadastrar Evento

**POST** `/eventos`  
**Requer:** perfil ADMIN

| Campo | Tipo | Obrigatório |
|---|---|---|
| titulo | string | Sim |
| descricao | string | Não |
| data_evento | date (YYYY-MM-DD) | Sim |
| horario | time (HH:mm) | Sim |
| local | string | Sim |
| vagas_total | int | Sim |

---

## 6. Códigos de Status HTTP Utilizados

| Código | Significado |
|---|---|
| 200 OK | Requisição bem-sucedida |
| 201 Created | Recurso criado com sucesso |
| 204 No Content | Operação realizada sem retorno |
| 400 Bad Request | Dados inválidos ou campos obrigatórios ausentes |
| 401 Unauthorized | Token ausente ou inválido |
| 403 Forbidden | Perfil sem permissão para o recurso |
| 404 Not Found | Recurso não encontrado |
| 409 Conflict | Conflito de estado (ex: exemplar já emprestado) |
| 422 Unprocessable Entity | Regra de negócio violada |
| 500 Internal Server Error | Erro inesperado no servidor |

---

## 7. Formato de Erro Padrão

Todos os erros retornam o seguinte formato JSON:

```json
{
  "timestamp": "2026-03-27T10:45:00",
  "status": 422,
  "erro": "Regra de negócio violada",
  "mensagem": "O membro possui empréstimo em atraso e não pode realizar novos empréstimos.",
  "path": "/emprestimos"
}
```
