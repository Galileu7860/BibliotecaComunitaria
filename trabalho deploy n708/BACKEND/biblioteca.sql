-- 1. Criando a tabela de Usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telephone VARCHAR(20) NOT NULL,
    data_cadastro DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'ativo'
);

-- 2. Criando a tabela de Livros
CREATE TABLE livros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(150) NOT NULL,
    isbn VARCHAR(13) UNIQUE,
    categoria VARCHAR(50),
    qtd_total INT DEFAULT 1,
    qtd_disponivel INT DEFAULT 1
);

-- 3. Criando a tabela de Empréstimos (com os relacionamentos)
CREATE TABLE emprestimos (
    id SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_livro INT NOT NULL,
    data_emprestimo DATE DEFAULT CURRENT_DATE,
    data_devolucao_prevista DATE NOT NULL,
    data_devolucao_real DATE,
    status VARCHAR(20) DEFAULT 'pendente',

    -- Restrições de Chave Estrangeira (Garante a integridade dos dados)
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE RESTRICT,
    FOREIGN KEY (id_livro) REFERENCES livros(id) ON DELETE RESTRICT
);