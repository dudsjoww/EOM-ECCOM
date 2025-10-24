-- ===========================================
-- BANCO DE DADOS: SISTEMA DE TATUAGEM (FINAL)
-- ===========================================

-- ===========================================
-- USUÁRIOS (clientes, tatuadores e admin)
-- ===========================================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    telefone VARCHAR(20),
    ativo BOOLEAN DEFAULT true,
    criado_em TIMESTAMP DEFAULT NOW()
);

-- ===========================================
-- TATUADORES
-- ===========================================
CREATE TABLE tatuadores (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    especialidade VARCHAR(255),
    ativo BOOLEAN DEFAULT true
);
-- ===========================================
-- HORÁRIOS DE TRABALHO
-- ===========================================
CREATE TABLE horarios_de_trabalho (
    id SERIAL PRIMARY KEY,
    dia_semana VARCHAR(15) CHECK (dia_semana IN ('SEG','TER','QUA','QUI','SEX','SAB','DOM'))
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    observacao TEXT
);

CREATE TABLE todos_os_horarios (
    id SERIAL PRIMARY KEY,
    tatuador_id INT REFERENCES tatuadores(id),
    horario_id INT REFERENCES horarios_de_trabalho(id)
);


-- ===========================================
-- ESTOQUE
-- ===========================================
CREATE TABLE estoque(
    id SERIAL PRIMARY KEY,
    nome_item VARCHAR(255) NOT NULL,
    quantidade INT NOT NULL DEFAULT 0,
    custo_unitario NUMERIC(10,2) NOT NULL,
    preco_venda NUMERIC(10,2) DEFAULT NULL,
    marca VARCHAR(50) NOT NULL,
    unidade_medida VARCHAR(20) NOT NULL,
    descricao TEXT,
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW(),
    passivo BOOLEAN DEFAULT false
    ativo BOOLEAN DEFAULT true,
);
-- ===========================================
-- CONSUMÍVEIS (referência ao estoque)
-- ===========================================
CREATE TABLE venda_consumivel(
    id SERIAL PRIMARY KEY,
    item_id INT NOT NULL REFERENCES estoque(id),
    pedido_id INT NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    quantidade INT NOT NULL,
    preco_final NUMERIC(10,2) NOT NULL,
    ativo BOOLEAN DEFAULT true
);

-- ===========================================
-- ORÇAMENTOS
-- ===========================================
CREATE TABLE orcamentos (
    id SERIAL PRIMARY KEY,
    valor_sessao NUMERIC(10,2) NOT NULL, -- valor base da sessão
    duracao_horas NUMERIC(5,2) DEFAULT 1,
    qtd_sessoes INT DEFAULT 1,
    enviado_em TIMESTAMP DEFAULT NOW(),
    confirmado_cliente BOOLEAN DEFAULT false
);

-- ===========================================
-- AGENDAMENTOS
-- ===========================================
CREATE TABLE agendamentos (
    id SERIAL PRIMARY KEY,
    data_agendada DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    confirmado_cliente BOOLEAN DEFAULT false,
    criado_em TIMESTAMP DEFAULT NOW()
);
-- ===========================================
-- PEDIDOS DE VENDA
-- ===========================================
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    tatuador_id INT REFERENCES tatuadores(id) ON DELETE SET NULL,
    area_corpo VARCHAR(50) DEFAULT 'Não escolhido',
    tamanho VARCHAR(50) DEFAULT 'Não escolhido',
    imagem_png TEXT,
    coordenadas JSONB DEFAULT NULL,
    status VARCHAR(50) DEFAULT 'solicitado' CHECK (status IN (
        'solicitado', 'em_orcamento', 'resposta_cliente', 'separado',
        'agendado', 'concluido', 'cancelado'
    )),
    agendamento_id INT REFERENCES agendamentos(id) ON DELETE SET NULL,
    venda_consumivel_id INT REFERENCES venda_consumivel(id) ON DELETE SET NULL,
    sessao_id INT REFERENCES sessao(id) ON DELETE SET NULL,
    observacao TEXT,
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW()
);

CREATE TABLE sessao(
    id SERIAL PRIMARY KEY,
    orcamento_id INT NOT NULL REFERENCES orcamentos(id) ON DELETE CASCADE,
    data_sessao DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    observacao TEXT
);

-- ===========================================
-- PAGAMENTOS
-- ===========================================
CREATE TABLE pagamentos (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    valor_total NUMERIC(10,2) NOT NULL,
    metodo_pagamento VARCHAR(50) DEFAULT 'presencial',
    feedback_cliente TEXT,
    nota_cliente INT CHECK (nota_cliente BETWEEN 1 AND 5),
    origem_cliente VARCHAR(100),
    confirmado BOOLEAN DEFAULT false,
    data_pagamento TIMESTAMP
);