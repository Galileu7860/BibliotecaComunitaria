# Modelo de Dados — BiblioTech

> docs/database/database_model.md  
> Projeto Aplicado Multiplataforma — Etapa 1 (N705)

---

## 1. Diagrama Entidade-Relacionamento (ER)

```
┌─────────────────┐       ┌──────────────────────┐       ┌──────────────────┐
│    USUARIOS     │       │     EMPRESTIMOS       │       │     LIVROS       │
├─────────────────┤       ├──────────────────────┤       ├──────────────────┤
│ PK id           │       │ PK id                 │       │ PK id            │
│    nome         │1     N│ FK id_usuario          │N     1│    titulo        │
│    email        ├───────┤ FK id_exemplar         ├───────┤    autor         │
│    senha_hash   │       │    data_emprestimo    │       │    isbn          │
│    cpf          │       │    data_prevista_dev  │       │    editora       │
│    telefone     │       │    data_devolucao     │       │    ano_publicacao│
│    endereco     │       │    status             │       │    genero        │
│    perfil       │       │    renovado           │       │    descricao     │
│    ativo        │       └──────────────────────┘       └────────┬─────────┘
│    created_at   │                                               │
└────────┬────────┘                                             1 │
         │                                                         │
         │ 1                                               ┌───────▼──────────┐
         │                                                 │    EXEMPLARES    │
         │ N                                               ├──────────────────┤
┌────────▼────────────────┐                               │ PK id            │
│  INSCRICOES_EVENTOS     │                               │ FK id_livro      │
├─────────────────────────┤                               │    codigo_barras │
│ PK id                   │                               │    estado        │
│ FK id_usuario           │                               │    disponivel    │
│ FK id_evento            │                               └──────────────────┘
│    data_inscricao       │
└─────────────────────────┘
         │ N
         │
         │ 1
┌────────▼─────────┐
│     EVENTOS      │
├──────────────────┤
│ PK id            │
│    titulo        │
│    descricao     │
│    data_evento   │
│    horario       │
│    local         │
│    vagas_total   │
│    vagas_disp    │
│    ativo         │
└──────────────────┘
```

---

## 2. Descrição das Entidades e Relacionamentos

### 2.1 USUARIOS
Armazena todos os usuários do sistema, tanto Administradores quanto Membros.

**Relacionamentos:**
- Um usuário pode ter **muitos** empréstimos (1:N com EMPRESTIMOS)
- Um usuário pode se inscrever em **muitos** eventos (1:N com INSCRICOES_EVENTOS)

### 2.2 LIVROS
Representa as obras do acervo bibliográfico. Um livro pode ter múltiplos exemplares físicos.

**Relacionamentos:**
- Um livro possui **um ou mais** exemplares (1:N com EXEMPLARES)

### 2.3 EXEMPLARES
Representa as cópias físicas de um livro. Cada exemplar é o objeto real que é emprestado.

**Relacionamentos:**
- Um exemplar pertence a **um** livro (N:1 com LIVROS)
- Um exemplar pode estar em **muitos** empréstimos ao longo do tempo, mas em apenas **um** empréstimo ativo por vez (1:N com EMPRESTIMOS)

### 2.4 EMPRESTIMOS
Registra cada operação de empréstimo, associando um membro a um exemplar específico.

**Relacionamentos:**
- Um empréstimo pertence a **um** usuário (N:1 com USUARIOS)
- Um empréstimo refere-se a **um** exemplar (N:1 com EXEMPLARES)

### 2.5 EVENTOS
Armazena os eventos culturais organizados pela biblioteca.

**Relacionamentos:**
- Um evento pode ter **muitas** inscrições de usuários (1:N com INSCRICOES_EVENTOS)

### 2.6 INSCRICOES_EVENTOS
Tabela de junção que registra quais membros estão inscritos em quais eventos.

**Relacionamentos:**
- Cada inscrição pertence a **um** usuário e a **um** evento (N:N resolvido)

---

## 3. Dicionário de Dados

### Tabela: `usuarios`

| Coluna | Tipo | Restrição | Descrição |
|---|---|---|---|
| id | BIGINT | PK, AUTO_INCREMENT | Identificador único |
| nome | VARCHAR(150) | NOT NULL | Nome completo do usuário |
| email | VARCHAR(150) | NOT NULL, UNIQUE | E-mail (usado no login) |
| senha_hash | VARCHAR(255) | NOT NULL | Senha criptografada com BCrypt |
| cpf | CHAR(11) | NOT NULL, UNIQUE | CPF sem formatação |
| telefone | VARCHAR(20) | NULL | Telefone de contato |
| endereco | VARCHAR(255) | NULL | Endereço completo |
| perfil | ENUM('ADMIN','MEMBRO') | NOT NULL, DEFAULT 'MEMBRO' | Perfil de acesso |
| ativo | BOOLEAN | NOT NULL, DEFAULT TRUE | Indica se a conta está ativa |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Data de cadastro |

### Tabela: `livros`

| Coluna | Tipo | Restrição | Descrição |
|---|---|---|---|
| id | BIGINT | PK, AUTO_INCREMENT | Identificador único |
| titulo | VARCHAR(255) | NOT NULL | Título da obra |
| autor | VARCHAR(150) | NOT NULL | Nome do autor |
| isbn | VARCHAR(20) | NULL, UNIQUE | ISBN da obra |
| editora | VARCHAR(100) | NULL | Nome da editora |
| ano_publicacao | YEAR | NULL | Ano de publicação |
| genero | VARCHAR(80) | NULL | Gênero literário |
| descricao | TEXT | NULL | Sinopse ou descrição |

### Tabela: `exemplares`

| Coluna | Tipo | Restrição | Descrição |
|---|---|---|---|
| id | BIGINT | PK, AUTO_INCREMENT | Identificador único |
| id_livro | BIGINT | FK → livros.id, NOT NULL | Livro ao qual pertence |
| codigo_barras | VARCHAR(50) | NULL, UNIQUE | Código de barras do exemplar |
| estado | ENUM('OTIMO','BOM','RUIM','DANIFICADO') | NOT NULL, DEFAULT 'BOM' | Estado físico do exemplar |
| disponivel | BOOLEAN | NOT NULL, DEFAULT TRUE | Indica se está disponível para empréstimo |

### Tabela: `emprestimos`

| Coluna | Tipo | Restrição | Descrição |
|---|---|---|---|
| id | BIGINT | PK, AUTO_INCREMENT | Identificador único |
| id_usuario | BIGINT | FK → usuarios.id, NOT NULL | Membro que realizou o empréstimo |
| id_exemplar | BIGINT | FK → exemplares.id, NOT NULL | Exemplar emprestado |
| data_emprestimo | DATE | NOT NULL | Data do empréstimo |
| data_prevista_dev | DATE | NOT NULL | Data prevista para devolução |
| data_devolucao | DATE | NULL | Data efetiva de devolução (null = em aberto) |
| status | ENUM('ATIVO','DEVOLVIDO','ATRASADO') | NOT NULL, DEFAULT 'ATIVO' | Status do empréstimo |
| renovado | BOOLEAN | NOT NULL, DEFAULT FALSE | Indica se houve renovação |

### Tabela: `eventos`

| Coluna | Tipo | Restrição | Descrição |
|---|---|---|---|
| id | BIGINT | PK, AUTO_INCREMENT | Identificador único |
| titulo | VARCHAR(200) | NOT NULL | Título do evento |
| descricao | TEXT | NULL | Descrição detalhada |
| data_evento | DATE | NOT NULL | Data de realização |
| horario | TIME | NOT NULL | Horário de início |
| local | VARCHAR(200) | NOT NULL | Local de realização |
| vagas_total | INT | NOT NULL | Número total de vagas |
| vagas_disponiveis | INT | NOT NULL | Vagas ainda disponíveis |
| ativo | BOOLEAN | NOT NULL, DEFAULT TRUE | Indica se o evento está ativo |

### Tabela: `inscricoes_eventos`

| Coluna | Tipo | Restrição | Descrição |
|---|---|---|---|
| id | BIGINT | PK, AUTO_INCREMENT | Identificador único |
| id_usuario | BIGINT | FK → usuarios.id, NOT NULL | Membro inscrito |
| id_evento | BIGINT | FK → eventos.id, NOT NULL | Evento da inscrição |
| data_inscricao | DATETIME | NOT NULL, DEFAULT NOW() | Data e hora da inscrição |

---

## 4. Script DDL (MySQL)

```sql
CREATE DATABASE IF NOT EXISTS bibliotech CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bibliotech;

CREATE TABLE usuarios (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome         VARCHAR(150) NOT NULL,
    email        VARCHAR(150) NOT NULL UNIQUE,
    senha_hash   VARCHAR(255) NOT NULL,
    cpf          CHAR(11)     NOT NULL UNIQUE,
    telefone     VARCHAR(20),
    endereco     VARCHAR(255),
    perfil       ENUM('ADMIN','MEMBRO') NOT NULL DEFAULT 'MEMBRO',
    ativo        BOOLEAN NOT NULL DEFAULT TRUE,
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE livros (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    titulo          VARCHAR(255) NOT NULL,
    autor           VARCHAR(150) NOT NULL,
    isbn            VARCHAR(20) UNIQUE,
    editora         VARCHAR(100),
    ano_publicacao  YEAR,
    genero          VARCHAR(80),
    descricao       TEXT
);

CREATE TABLE exemplares (
    id            BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_livro      BIGINT NOT NULL,
    codigo_barras VARCHAR(50) UNIQUE,
    estado        ENUM('OTIMO','BOM','RUIM','DANIFICADO') NOT NULL DEFAULT 'BOM',
    disponivel    BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (id_livro) REFERENCES livros(id)
);

CREATE TABLE emprestimos (
    id                 BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_usuario         BIGINT NOT NULL,
    id_exemplar        BIGINT NOT NULL,
    data_emprestimo    DATE NOT NULL,
    data_prevista_dev  DATE NOT NULL,
    data_devolucao     DATE,
    status             ENUM('ATIVO','DEVOLVIDO','ATRASADO') NOT NULL DEFAULT 'ATIVO',
    renovado           BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_exemplar) REFERENCES exemplares(id)
);

CREATE TABLE eventos (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
    titulo              VARCHAR(200) NOT NULL,
    descricao           TEXT,
    data_evento         DATE NOT NULL,
    horario             TIME NOT NULL,
    local               VARCHAR(200) NOT NULL,
    vagas_total         INT NOT NULL,
    vagas_disponiveis   INT NOT NULL,
    ativo               BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE inscricoes_eventos (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_usuario      BIGINT NOT NULL,
    id_evento       BIGINT NOT NULL,
    data_inscricao  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_evento) REFERENCES eventos(id),
    UNIQUE KEY uq_usuario_evento (id_usuario, id_evento)
);
```
