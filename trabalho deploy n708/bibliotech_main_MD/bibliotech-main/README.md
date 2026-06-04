# BiblioTech — Sistema de Gestão para Bibliotecas Comunitárias

> Projeto Aplicado Multiplataforma — Etapa 1 (N705)  
> Universidade de Fortaleza (UNIFOR) — EAD

---

## Descrição do Projeto

O **BiblioTech** é uma solução de software multiplataforma voltada para a gestão completa de bibliotecas comunitárias. O sistema permite o gerenciamento de acervos, empréstimos, devoluções, cadastro de membros e divulgação de eventos culturais, promovendo o acesso democrático à cultura e ao conhecimento em comunidades periféricas e espaços públicos de Fortaleza e região.

---

## Problema Abordado e Justificativa

Bibliotecas comunitárias enfrentam desafios significativos na organização de seus acervos e no controle de empréstimos, operando frequentemente de forma manual — com fichas físicas, planilhas improvisadas ou sem qualquer registro sistemático. Essa realidade resulta em:

- Perda e extravio de livros sem rastreabilidade
- Dificuldade dos membros em consultar quais títulos estão disponíveis
- Falta de divulgação estruturada de eventos e atividades culturais
- Ausência de dados para tomada de decisão pelos gestores

O BiblioTech resolve esses problemas oferecendo uma plataforma digital acessível tanto via navegador web quanto por dispositivos móveis, sem exigir conhecimento técnico avançado por parte dos operadores.

---

## Objetivos do Sistema

- Digitalizar e centralizar o catálogo do acervo bibliográfico
- Automatizar o controle de empréstimos e devoluções com alertas de prazo
- Facilitar o cadastro e a gestão de membros da biblioteca
- Promover a divulgação de eventos e atividades culturais
- Gerar relatórios de uso para apoio à gestão

---

## Escopo do Projeto

### Dentro do Escopo (Etapa 1 — Planejamento)
- Documento de requisitos funcionais e não funcionais
- Modelagem do banco de dados (diagrama ER)
- Especificação da arquitetura do sistema
- Especificação das APIs REST
- Protótipos de interface (web e mobile)
- Cronograma de desenvolvimento para a Etapa 2

### Fora do Escopo (Etapa 1)
- Implementação de código (será realizada na Etapa 2 — N708)
- Integração com sistemas externos de pagamento
- Funcionalidade de e-book ou conteúdo digital

---

## Visão Geral da Arquitetura

O BiblioTech adota uma **arquitetura em camadas (Layered Architecture)** com separação clara entre frontend, backend e banco de dados, comunicando-se via **API REST**.

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENTES                            │
│                                                         │
│   ┌──────────────────┐    ┌──────────────────────┐      │
│   │  Web (React.js)  │    │ Mobile (React Native) │      │
│   └────────┬─────────┘    └──────────┬────────────┘      │
└────────────┼──────────────────────────┼───────────────────┘
             │         HTTPS / REST API │
┌────────────▼──────────────────────────▼───────────────────┐
│                  BACKEND (Spring Boot / Java)              │
│                                                           │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Controller │→ │   Service    │→ │   Repository     │  │
│  │  (REST)    │  │ (Regras de   │  │ (JPA/Hibernate)  │  │
│  └────────────┘  │  Negócio)    │  └────────┬─────────┘  │
│                  └──────────────┘           │            │
└─────────────────────────────────────────────┼────────────┘
                                              │
┌─────────────────────────────────────────────▼────────────┐
│                    BANCO DE DADOS                        │
│                       MySQL 8.x                          │
└──────────────────────────────────────────────────────────┘
```

---

## Tecnologias Propostas

| Camada | Tecnologia | Versão |
|---|---|---|
| Backend | Spring Boot (Java) | 3.x |
| Frontend Web | React.js | 18.x |
| Mobile | React Native | 0.73.x |
| Banco de Dados | MySQL | 8.x |
| ORM | Hibernate / JPA | — |
| Autenticação | JWT (JSON Web Token) | — |
| Documentação de API | Swagger / OpenAPI | 3.x |
| Versionamento | Git / GitHub | — |
| Build (Backend) | Maven | 3.x |

---

## Relação com o ODS 11 — Cidades e Comunidades Sustentáveis

O ODS 11 busca tornar as cidades e comunidades inclusivas, seguras, resilientes e sustentáveis. O BiblioTech contribui diretamente para essa meta ao:

- **Democratizar o acesso à cultura e ao conhecimento** em comunidades com poucos recursos
- **Fortalecer espaços culturais comunitários** por meio da digitalização de seus processos
- **Promover a inclusão digital** ao oferecer uma interface simples e acessível
- **Apoiar a tomada de decisão** de gestores de bibliotecas com dados e relatórios

A digitalização de bibliotecas comunitárias é um passo concreto para tornar comunidades mais inteligentes e sustentáveis, alinhando tecnologia ao desenvolvimento humano e social.

---

## Cronograma para a Etapa 2 (N708)

| Semana | Atividade |
|---|---|
| 1–2 | Configuração do ambiente; estrutura inicial do projeto Spring Boot e React |
| 3–4 | Implementação do módulo de autenticação (login, JWT, perfis de acesso) |
| 5–6 | Implementação do módulo de catálogo (CRUD de livros, busca e filtragem) |
| 7–8 | Implementação do módulo de membros (cadastro, perfil, histórico) |
| 9–10 | Implementação do módulo de empréstimos e devoluções (com notificações) |
| 11–12 | Implementação do módulo de eventos culturais |
| 13 | Testes unitários e de integração |
| 14 | Ajustes finais, deploy e documentação de encerramento |

---

## Integrantes da Equipe e Papéis

| Nome | Matrícula | Papel |
|---|---|---|
| João Victor da Silva Lima | 2326312 | Arquiteto de Software / Desenvolvedor Backend |
| Pedro Átila Freitas Costa | 2323832 | Desenvolvedor Frontend Web |
| José Thiago Rodrigues Tavares | 2327303 | Desenvolvedor Mobile |
| Risoleta Pereira Pinto | 2323869 | Analista de Requisitos / Documentação |

---

## Estrutura do Repositório

```
bibliotech/
├── README.md
├── docs/
│   ├── requirements/
│   │   └── requirements.md
│   ├── architecture/
│   │   └── architecture.md
│   ├── database/
│   │   └── database_model.md
│   └── api/
│       └── api_specification.md
└── prototypes/
    └── (wireframes das telas principais)
```
