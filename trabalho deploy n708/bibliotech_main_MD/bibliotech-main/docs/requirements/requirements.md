# Documento de Requisitos — BiblioTech

> docs/requirements/requirements.md  
> Projeto Aplicado Multiplataforma — Etapa 1 (N705)

---

## 1. Perfis de Usuários

### 1.1 Administrador
Responsável pela gestão completa do sistema. Gerencia o acervo, membros, eventos e visualiza relatórios. Geralmente é o bibliotecário ou coordenador da biblioteca comunitária.

### 1.2 Membro
Usuário cadastrado na biblioteca. Pode consultar o catálogo, visualizar seu histórico de empréstimos e se inscrever em eventos. Acessa o sistema via web ou aplicativo mobile.

### 1.3 Visitante (não autenticado)
Usuário sem cadastro que pode apenas consultar o catálogo público e a agenda de eventos, sem realizar empréstimos.

---

## 2. Requisitos Funcionais (RF)

### Módulo de Autenticação

| Código | Descrição | Prioridade |
|---|---|---|
| RF01 | O sistema deve permitir o cadastro de novos membros com nome, e-mail, CPF, telefone e endereço. | Alta |
| RF02 | O sistema deve permitir login com e-mail e senha. | Alta |
| RF03 | O sistema deve suportar dois perfis de acesso: Administrador e Membro. | Alta |
| RF04 | O sistema deve permitir a recuperação de senha via e-mail. | Média |
| RF05 | O sistema deve permitir que o Administrador ative ou desative contas de membros. | Média |

### Módulo de Catálogo

| Código | Descrição | Prioridade |
|---|---|---|
| RF06 | O sistema deve permitir ao Administrador cadastrar livros com título, autor, ISBN, editora, ano, gênero e número de exemplares. | Alta |
| RF07 | O sistema deve permitir ao Administrador editar e excluir registros de livros. | Alta |
| RF08 | O sistema deve exibir a disponibilidade de cada livro em tempo real (disponível, emprestado). | Alta |
| RF09 | O sistema deve permitir a busca de livros por título, autor, ISBN ou gênero. | Alta |
| RF10 | O sistema deve exibir a ficha completa do livro ao selecionar um resultado de busca. | Média |

### Módulo de Empréstimos e Devoluções

| Código | Descrição | Prioridade |
|---|---|---|
| RF11 | O sistema deve permitir ao Administrador registrar um empréstimo associando um livro a um membro. | Alta |
| RF12 | O sistema deve definir automaticamente a data de devolução com prazo de 15 dias. | Alta |
| RF13 | O sistema deve permitir ao Administrador registrar a devolução de um livro. | Alta |
| RF14 | O sistema deve enviar notificação (e-mail) ao membro 2 dias antes do prazo de devolução. | Média |
| RF15 | O sistema deve registrar e exibir o histórico completo de empréstimos de cada membro. | Média |
| RF16 | O sistema deve bloquear novos empréstimos para membros com livros em atraso. | Alta |
| RF17 | O sistema deve permitir a renovação do empréstimo uma vez, desde que não haja outros interessados no título. | Baixa |

### Módulo de Eventos Culturais

| Código | Descrição | Prioridade |
|---|---|---|
| RF18 | O sistema deve permitir ao Administrador cadastrar eventos com título, descrição, data, horário, local e vagas. | Alta |
| RF19 | O sistema deve permitir que membros se inscrevam em eventos com vagas disponíveis. | Média |
| RF20 | O sistema deve exibir uma agenda pública de eventos, acessível sem login. | Média |
| RF21 | O sistema deve notificar membros inscritos por e-mail sobre eventos próximos. | Baixa |

### Módulo de Relatórios

| Código | Descrição | Prioridade |
|---|---|---|
| RF22 | O sistema deve gerar relatório dos livros mais emprestados no período. | Média |
| RF23 | O sistema deve gerar relatório de empréstimos em aberto e em atraso. | Alta |
| RF24 | O sistema deve exibir o total de membros ativos cadastrados. | Média |

---

## 3. Requisitos Não Funcionais (RNF)

### 3.1 Desempenho

| Código | Descrição |
|---|---|
| RNF01 | O sistema deve responder a requisições de busca no catálogo em até 2 segundos. |
| RNF02 | O sistema deve suportar pelo menos 100 usuários simultâneos sem degradação perceptível. |

### 3.2 Disponibilidade

| Código | Descrição |
|---|---|
| RNF03 | O sistema deve estar disponível pelo menos 99% do tempo em horário comercial (segunda a sexta, 7h–22h). |
| RNF04 | Manutenções programadas devem ser realizadas fora do horário comercial e comunicadas com antecedência. |

### 3.3 Segurança

| Código | Descrição |
|---|---|
| RNF05 | As senhas dos usuários devem ser armazenadas com hash BCrypt. |
| RNF06 | A comunicação entre cliente e servidor deve ser realizada via HTTPS. |
| RNF07 | O sistema deve utilizar autenticação baseada em JWT com expiração de 8 horas. |
| RNF08 | O sistema deve estar em conformidade com a LGPD (Lei Geral de Proteção de Dados). |

### 3.4 Usabilidade

| Código | Descrição |
|---|---|
| RNF09 | A interface deve ser responsiva, adaptando-se a telas de desktop, tablet e smartphone. |
| RNF10 | O sistema deve ser operável por usuários com baixo letramento digital, com navegação intuitiva. |
| RNF11 | As principais ações devem ser executadas em no máximo 3 cliques/toques a partir da tela inicial. |

### 3.5 Compatibilidade

| Código | Descrição |
|---|---|
| RNF12 | O frontend web deve ser compatível com os navegadores Chrome, Firefox e Edge (versões dos últimos 2 anos). |
| RNF13 | O aplicativo mobile deve funcionar em Android 10+ e iOS 14+. |

### 3.6 Confiabilidade

| Código | Descrição |
|---|---|
| RNF14 | O sistema deve realizar backup automático do banco de dados diariamente. |
| RNF15 | Em caso de falha, o sistema deve garantir rollback de transações incompletas. |

---

## 4. Regras de Negócio (RN)

| Código | Descrição |
|---|---|
| RN01 | Um membro só pode ter até 3 livros emprestados simultaneamente. |
| RN02 | O prazo padrão de empréstimo é de 15 dias corridos. |
| RN03 | Membros com empréstimo em atraso não podem realizar novos empréstimos. |
| RN04 | A renovação de empréstimo só é permitida uma vez por exemplar por usuário. |
| RN05 | O cadastro de livros exige que ao menos título, autor e número de exemplares sejam informados. |
| RN06 | Um evento não pode ter mais inscrições do que o número de vagas definido. |
| RN07 | Somente o Administrador pode registrar empréstimos, devoluções e gerenciar o acervo. |

---

## 5. Histórias de Usuário

### Como Membro:
- **HU01:** Como membro, quero buscar livros pelo título ou autor para encontrar rapidamente o que desejo ler.
- **HU02:** Como membro, quero visualizar meu histórico de empréstimos para saber quais livros já li.
- **HU03:** Como membro, quero receber um aviso antes do prazo de devolução para não atrasar a entrega.
- **HU04:** Como membro, quero me inscrever em eventos culturais para participar das atividades da biblioteca.
- **HU05:** Como membro, quero ver a agenda de eventos para planejar minha participação.

### Como Administrador:
- **HU06:** Como administrador, quero cadastrar novos livros para manter o acervo atualizado.
- **HU07:** Como administrador, quero registrar empréstimos e devoluções para controlar a movimentação do acervo.
- **HU08:** Como administrador, quero visualizar relatórios de empréstimos em atraso para contatar os membros.
- **HU09:** Como administrador, quero cadastrar eventos para divulgar as atividades da biblioteca.
- **HU10:** Como administrador, quero bloquear membros com atraso para incentivar a devolução dos livros.
