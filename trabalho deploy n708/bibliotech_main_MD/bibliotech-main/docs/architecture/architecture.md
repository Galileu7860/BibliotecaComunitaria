# Documento de Arquitetura — BiblioTech

> docs/architecture/architecture.md  
> Projeto Aplicado Multiplataforma — Etapa 1 (N705)

---

## 1. Visão Geral da Arquitetura

O BiblioTech é construído sobre uma **arquitetura em camadas (Layered Architecture)**, com separação clara de responsabilidades entre as camadas de apresentação, aplicação, domínio e persistência. O backend expõe uma **API REST** consumida tanto pelo frontend web quanto pelo aplicativo mobile, garantindo que ambos os clientes compartilhem a mesma lógica de negócio.

Esse padrão foi escolhido por ser amplamente documentado, de fácil manutenção, e por mapear diretamente para as boas práticas do ecossistema Spring Boot — tecnologia central do projeto.

---

## 2. Diagrama de Arquitetura

```
╔══════════════════════════════════════════════════════════════╗
║                      CAMADA DE APRESENTAÇÃO                  ║
║                                                              ║
║  ┌──────────────────────────┐  ┌────────────────────────┐   ║
║  │     React.js (Web)       │  │  React Native (Mobile)  │   ║
║  │  - Catálogo               │  │  - Catálogo             │   ║
║  │  - Empréstimos            │  │  - Meu histórico        │   ║
║  │  - Eventos                │  │  - Eventos              │   ║
║  │  - Painel Admin           │  │  - Notificações         │   ║
║  └────────────┬─────────────┘  └───────────┬────────────┘   ║
╚═══════════════╪════════════════════════════╪════════════════╝
                │      HTTPS + JWT           │
╔═══════════════▼════════════════════════════▼════════════════╗
║                    CAMADA DE APLICAÇÃO                       ║
║              Spring Boot 3.x (Java)                         ║
║                                                              ║
║  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  ║
║  │  Controllers │  │   Services   │  │   Repositories   │  ║
║  │  (REST API)  │→ │  (Negócio)   │→ │  (JPA/Hibernate) │  ║
║  └──────────────┘  └──────────────┘  └────────┬─────────┘  ║
║                                                │            ║
║  ┌────────────────────────────────────────┐   │            ║
║  │     Módulos: Acervo | Empréstimos      │   │            ║
║  │     Membros | Eventos | Relatórios     │   │            ║
║  └────────────────────────────────────────┘   │            ║
╚════════════════════════════════════════════════╪════════════╝
                                                 │
╔════════════════════════════════════════════════▼════════════╗
║                    CAMADA DE PERSISTÊNCIA                    ║
║                       MySQL 8.x                             ║
║                                                              ║
║   Tabelas: usuarios | livros | exemplares | emprestimos     ║
║            eventos | inscricoes_eventos | notificacoes      ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 3. Componentes do Sistema

### 3.1 Frontend Web (React.js)

Aplicação de página única (SPA — Single Page Application) responsável pela interface do usuário no navegador. Comunica-se com o backend exclusivamente via chamadas HTTP à API REST, utilizando tokens JWT para autenticação.

**Principais responsabilidades:**
- Renderização das telas de catálogo, empréstimos, membros e eventos
- Painel administrativo com acesso restrito ao perfil Administrador
- Gerenciamento de estado com React Context ou Redux

### 3.2 Aplicativo Mobile (React Native)

Aplicativo nativo para Android e iOS construído com React Native, compartilhando lógica de negócio e chamadas de API com o frontend web. Focado nas funcionalidades do Membro: consulta ao catálogo, histórico de empréstimos, agenda de eventos e notificações push.

**Principais responsabilidades:**
- Interface otimizada para telas móveis (UX Mobile-first)
- Notificações locais para alertas de prazo de devolução
- Acesso offline a informações básicas do catálogo (cache local)

### 3.3 Backend — API REST (Spring Boot / Java)

Núcleo do sistema, responsável por toda a lógica de negócio, validações, autenticação e acesso ao banco de dados. Organizado em módulos seguindo o padrão **MVC (Model-View-Controller)** com camada de serviço.

**Módulos:**
- `auth` — Autenticação, geração e validação de JWT
- `acervo` — Gestão de livros e exemplares
- `emprestimos` — Controle de empréstimos e devoluções
- `membros` — Cadastro e gestão de usuários
- `eventos` — Gestão de eventos culturais
- `relatorios` — Geração de relatórios e métricas
- `notificacoes` — Envio de e-mails e alertas

### 3.4 Banco de Dados (MySQL 8.x)

Sistema de gerenciamento de banco de dados relacional responsável pela persistência de todos os dados da aplicação. O acesso é realizado pelo backend via **Hibernate/JPA**, eliminando SQL nativo na maioria dos casos e facilitando a manutenção.

---

## 4. Padrões Arquiteturais Utilizados

| Padrão | Onde é Aplicado | Justificativa |
|---|---|---|
| Layered Architecture | Estrutura geral do sistema | Separação de responsabilidades, facilidade de manutenção |
| MVC (Model-View-Controller) | Backend Spring Boot | Padrão nativo do Spring, amplamente documentado |
| REST (REpresentational State Transfer) | Comunicação cliente-servidor | Interoperabilidade entre web e mobile; stateless |
| Repository Pattern | Camada de acesso a dados | Abstração do banco de dados via JPA/Hibernate |
| JWT (JSON Web Token) | Autenticação | Stateless, seguro, compatível com clientes múltiplos |
| DTO (Data Transfer Object) | Transferência de dados entre camadas | Evita exposição direta das entidades do banco |

---

## 5. Fluxo de Autenticação

```
Cliente                    Backend                      MySQL
  │                           │                            │
  │── POST /auth/login ───────►│                            │
  │   {email, senha}          │── SELECT usuario ─────────►│
  │                           │◄── dados do usuario ────────│
  │                           │                            │
  │                           │ [valida senha com BCrypt]  │
  │                           │                            │
  │◄── 200 OK ────────────────│                            │
  │   {token: "JWT..."}       │                            │
  │                           │                            │
  │── GET /livros ────────────►│                            │
  │   Authorization: Bearer   │                            │
  │                           │ [valida JWT]               │
  │◄── 200 OK + dados ────────│                            │
```

---

## 6. Decisões Técnicas e Justificativas

**Por que Spring Boot (Java)?**  
Spring Boot é um dos frameworks mais maduros e amplamente utilizados para desenvolvimento de APIs REST corporativas. Oferece integração nativa com JPA/Hibernate (MySQL), suporte robusto a autenticação JWT via Spring Security, e vasta documentação — fatores essenciais para uma equipe em formação.

**Por que React.js para web e React Native para mobile?**  
O compartilhamento de paradigmas entre React.js e React Native reduz a curva de aprendizado. Ambos utilizam JavaScript/TypeScript, JSX e o mesmo modelo de componentes, permitindo que o desenvolvedor trabalhe em ambas as plataformas com conhecimento unificado.

**Por que MySQL?**  
Os dados do BiblioTech são altamente relacionais (livros → exemplares → empréstimos → membros). Bancos relacionais como MySQL são ideais para esse modelo, garantindo integridade referencial via chaves estrangeiras e suporte a transações ACID — essenciais para operações de empréstimo.

**Por que JWT para autenticação?**  
JWT é stateless, o que significa que o servidor não precisa manter sessões em memória. Isso facilita o escalonamento horizontal do backend e funciona igualmente bem para clientes web e mobile.

---

## 7. Planejamento de Testes

| Tipo de Teste | Ferramenta | Cobertura Alvo |
|---|---|---|
| Testes Unitários (backend) | JUnit 5 + Mockito | Camada de Service (regras de negócio) |
| Testes de Integração (API) | Spring Boot Test + RestAssured | Todos os endpoints REST |
| Testes de Interface (web) | Jest + React Testing Library | Componentes principais |
| Testes de Carga | JMeter | Endpoint de busca no catálogo |
| Testes Manuais (mobile) | Expo Dev Tools | Fluxo completo de empréstimo |
