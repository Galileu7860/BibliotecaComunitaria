# Protótipos de Interface — BiblioTech

> prototypes/README.md  
> Projeto Aplicado Multiplataforma — Etapa 1 (N705)

Os protótipos de baixa fidelidade abaixo representam os fluxos principais do sistema
nas plataformas web e mobile. As telas foram concebidas seguindo princípios de
Design Centrado no Usuário (UCD) e Mobile UX, priorizando navegação simples e
clareza visual para usuários com diferentes níveis de familiaridade digital.

---

## Tela 1 — Login (Web e Mobile)

```
╔══════════════════════════════════════╗
║           🏛️  BiblioTech             ║
║      Sistema de Biblioteca           ║
╠══════════════════════════════════════╣
║                                      ║
║   E-mail:                            ║
║   ┌────────────────────────────┐     ║
║   │ usuario@email.com          │     ║
║   └────────────────────────────┘     ║
║                                      ║
║   Senha:                             ║
║   ┌────────────────────────────┐     ║
║   │ ••••••••                   │     ║
║   └────────────────────────────┘     ║
║                                      ║
║   [ Esqueci minha senha ]            ║
║                                      ║
║   ┌────────────────────────────┐     ║
║   │         ENTRAR             │     ║
║   └────────────────────────────┘     ║
║                                      ║
║   Não tem conta? [ Cadastrar ]       ║
╚══════════════════════════════════════╝
```

---

## Tela 2 — Catálogo de Livros (Web — Membro)

```
╔══════════════════════════════════════════════════════╗
║  BiblioTech  |  Catálogo  Empréstimos  Eventos  Sair║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  🔍 [ Buscar por título, autor ou gênero...   ] [🔎]║
║                                                      ║
║  Filtros: [ Todos ▼ ]  [ Disponíveis ☑ ]            ║
║                                                      ║
║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ║
║  │ 📗           │  │ 📘           │  │ 📙           │  ║
║  │ Dom Casmurro│  │ O Cortiço   │  │ Iracema     │  ║
║  │ M. de Assis │  │ A. Azevedo  │  │ J. de Alencar│ ║
║  │ ✅ Disponível│  │ ❌ Emprestado│  │ ✅ Disponível│  ║
║  │ [Ver mais]  │  │ [Ver mais]  │  │ [Ver mais]  │  ║
║  └─────────────┘  └─────────────┘  └─────────────┘  ║
║                                                      ║
║              << 1  2  3 ... >>                       ║
╚══════════════════════════════════════════════════════╝
```

---

## Tela 3 — Detalhe do Livro (Web)

```
╔══════════════════════════════════════════════════════╗
║  ← Voltar ao catálogo                               ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  📗  Dom Casmurro                                    ║
║       Machado de Assis — Ática — 1899               ║
║       Gênero: Romance | ISBN: 978-85-359-1484-9     ║
║                                                      ║
║  ─────────────────────────────────────────────────  ║
║  Sinopse:                                            ║
║  Clássico da literatura brasileira que narra a      ║
║  história de Bentinho e Capitu...                   ║
║                                                      ║
║  ─────────────────────────────────────────────────  ║
║  Exemplares: 3 total | ✅ 2 disponíveis              ║
║                                                      ║
║  ┌─────────────────────────────────────────────┐    ║
║  │   Solicitar Empréstimo (via bibliotecário)  │    ║
║  └─────────────────────────────────────────────┘    ║
╚══════════════════════════════════════════════════════╝
```

---

## Tela 4 — Painel do Administrador (Web)

```
╔══════════════════════════════════════════════════════╗
║  BiblioTech ADMIN   |  Acervo  Empréstimos  Membros  ║
║                         Eventos  Relatórios   Sair   ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  📊 Resumo do Dia                                   ║
║                                                      ║
║  ┌──────────┐  ┌──────────┐  ┌──────────┐            ║
║  │  📚 142  │  │  🔄 23   │  │  ⚠️  5   │          ║
║  │  Livros  │  │ Emprest. │  │  Atrasos │            ║
║  │  no acervo│  │  ativos  │  │          │           ║
║  └──────────┘  └──────────┘  └──────────┘            ║
║                                                      ║
║  📋 Empréstimos em Atraso                           ║
║  ──────────────────────────────────────────────────  ║
║  João Silva  |  Dom Casmurro  |  Venceu: 20/03/2026  ║
║  [Contatar]  [Registrar Devolução]                   ║
║  ──────────────────────────────────────────────────  ║
║  Ana Costa   |  O Cortiço    |  Venceu: 22/03/2026   ║
║  [Contatar]  [Registrar Devolução]                   ║
╚══════════════════════════════════════════════════════╝
```

---

## Tela 5 — Registro de Empréstimo (Web — Admin)

```
╔══════════════════════════════════════════════════════╗
║  ← Voltar                  Novo Empréstimo           ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  Membro:                                             ║
║  ┌──────────────────────────────────────────┐        ║
║  │ 🔍 Buscar por nome ou CPF...             │        ║
║  └──────────────────────────────────────────┘        ║
║  ✅ Ana Costa — CPF: 123.456.789-00 — Ativo          ║
║     Empréstimos ativos: 1/3                          ║
║                                                      ║
║  Exemplar:                                           ║
║  ┌──────────────────────────────────────────┐        ║
║  │ 🔍 Buscar por título ou código de barras │        ║
║  └──────────────────────────────────────────┘        ║
║  ✅ Dom Casmurro — Exemplar BC001 — Disponível       ║
║                                                      ║
║  Data de devolução prevista: 11/04/2026 (15 dias)    ║
║                                                      ║
║  ┌─────────────────────────────────────────┐         ║
║  │           CONFIRMAR EMPRÉSTIMO          │         ║
║  └─────────────────────────────────────────┘         ║
╚══════════════════════════════════════════════════════╝
```

---

## Tela 6 — Home Mobile (React Native)

```
╔════════════════════════╗
║  🏛️ BiblioTech          ║
║  Olá, João! 👋          ║
╠════════════════════════╣
║                        ║
║  📚 Meus Empréstimos   ║
║  ┌──────────────────┐  ║
║  │ Dom Casmurro     │  ║
║  │ Devolver até:    │  ║
║  │ 11/04/2026 ✅    │  ║
║  └──────────────────┘  ║
║                        ║
║  🔍 Buscar no Acervo   ║
║  ┌──────────────────┐  ║
║  │ 🔍 Buscar livro  │  ║
║  └──────────────────┘  ║
║                        ║
║  📅 Próximos Eventos   ║
║  ┌──────────────────┐  ║
║  │ Clube do Livro   │  ║
║  │ 15/04 às 18h30   │  ║
║  │ [Inscrever-se]   │  ║
║  └──────────────────┘  ║
╠════════════════════════╣
║  🏠 Início  📚 Acervo  ║
║  📅 Eventos  👤 Perfil ║
╚════════════════════════╝
```

---

## Tela 7 — Eventos (Mobile)

```
╔════════════════════════╗
║  ← Eventos Culturais   ║
╠════════════════════════╣
║                        ║
║  ┌──────────────────┐  ║
║  │ 📖 Clube do Livro│  ║
║  │ 15/04 | 18h30    │  ║
║  │ Sala de Leitura  │  ║
║  │ Vagas: 8/20      │  ║
║  │ [✅ Inscrever-se]│  ║
║  └──────────────────┘  ║
║                        ║
║  ┌──────────────────┐  ║
║  │ 🎨 Oficina Arte  │  ║
║  │ 22/04 | 14h00    │  ║
║  │ Auditório        │  ║
║  │ Vagas: 0/15      │  ║
║  │ [❌ Esgotado]    │  ║
║  └──────────────────┘  ║
╠════════════════════════╣
║  🏠 Início  📚 Acervo  ║
║  📅 Eventos  👤 Perfil ║
╚════════════════════════╝
```
