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
-- HORÁRIOS DE TRABALHO
-- ===========================================
CREATE TABLE horarios_de_trabalho (
    id SERIAL PRIMARY KEY,
    dia_semana VARCHAR(15) CHECK (STATUS IN (
        'SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM'
    )) -- 'segunda', 'terça', ...
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
-- TATUADORES
-- ===========================================
CREATE TABLE tatuadores (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    horario_id INT REFERENCES todos_os_horarios(id), -- referência ao horário
    especialidade VARCHAR(255),
    ativo BOOLEAN DEFAULT true
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
    ativo BOOLEAN DEFAULT true,
    marca VARCHAR(100),
    descricao TEXT,
    unidade_medida VARCHAR(50),
    data_registro TIMESTAMP DEFAULT NOW(),
    passive BOOLEAN DEFAULT false
);
============================================
-- Trigger para definir preco_venda = custo_unitario * 1.2 se não informado
-- CREATE OR REPLACE FUNCTION set_preco_venda_default()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     IF NEW.preco_venda IS NULL THEN
--         NEW.preco_venda := NEW.custo_unitario * 1.2;
--     END IF;
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;
===========================================


CREATE TRIGGER trg_set_preco_venda
BEFORE INSERT OR UPDATE ON estoque
FOR EACH ROW
EXECUTE FUNCTION set_preco_venda_default();

-- ===========================================
-- CONSUMÍVEIS (referência ao estoque)
-- ===========================================
CREATE TABLE consumiveis (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco NUMERIC(10,2) NOT NULL,
    estoque_id INT NOT NULL REFERENCES estoque(id),
    ativo BOOLEAN DEFAULT true
);

-- ===========================================
-- PEDIDOS DE TATUAGEM
-- ===========================================
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    tatuador_id INT REFERENCES tatuadores(id) ON DELETE SET NULL,
    area_corpo VARCHAR(50) NOT NULL,
    tamanho VARCHAR(50),
    imagem_png TEXT,
    coordenadas JSONB,
    status VARCHAR(50) DEFAULT 'solicitado' CHECK (status IN (
        'solicitado',
        'em_orcamento',
        'aguardando_cliente',
        'agendado',
        'concluido',
        'cancelado'
    )),
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW()
);

-- ===========================================
-- ORÇAMENTOS
-- ===========================================
CREATE TABLE orcamentos (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    tatuador_id INT NOT NULL REFERENCES tatuadores(id) ON DELETE CASCADE,
    valor_sessao NUMERIC(10,2) NOT NULL, -- valor base da sessão
    duracao_horas NUMERIC(5,2) DEFAULT 1,
    qtd_sessoes INT DEFAULT 1,
    observacao TEXT,
    enviado_em TIMESTAMP DEFAULT NOW(),
    confirmado_cliente BOOLEAN DEFAULT false
);

-- ===========================================
-- ITENS USADOS NO ORÇAMENTO (Consumíveis)
-- ===========================================
CREATE TABLE orcamento_consumiveis (
    id SERIAL PRIMARY KEY,
    orcamento_id INT NOT NULL REFERENCES orcamentos(id) ON DELETE CASCADE,
    estoque_id INT NOT NULL REFERENCES estoque(id) ON DELETE CASCADE,
    quantidade NUMERIC(10,2) NOT NULL
);

-- ===========================================
-- AGENDAMENTOS
-- ===========================================
CREATE TABLE agendamentos (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    tatuador_id INT NOT NULL REFERENCES tatuadores(id) ON DELETE CASCADE,
    cliente_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    data_agendada DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    confirmado_cliente BOOLEAN DEFAULT false,
    compareceu BOOLEAN DEFAULT false,
    concluido BOOLEAN DEFAULT false,
    cancelado BOOLEAN DEFAULT false,
    criado_em TIMESTAMP DEFAULT NOW()
);

-- ===========================================
-- CONSUMO DE ITENS (referencia custo de compra)
-- ===========================================
CREATE TABLE consumo_itens (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    consumivel_id INT NOT NULL REFERENCES consumiveis(id) ON DELETE CASCADE,
    quantidade INT NOT NULL,
    preco_unitario NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(10,2) GENERATED ALWAYS AS (quantidade * preco_unitario) STORED
);

-- ===========================================
-- VENDA DE CONSUMÍVEIS (referencia preco_venda)
-- ===========================================
CREATE TABLE venda_consumiveis (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    consumivel_id INT NOT NULL REFERENCES consumiveis(id) ON DELETE CASCADE,
    quantidade INT NOT NULL,
    preco_unitario NUMERIC(10,2) NOT NULL DEFAULT 0,
    subtotal NUMERIC(10,2) GENERATED ALWAYS AS (quantidade * preco_unitario) STORED
);

-- ===========================================
-- PAGAMENTOS
-- ===========================================
CREATE TABLE pagamentos (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    valor_total NUMERIC(10,2) NOT NULL,
    metodo_pagamento VARCHAR(50) DEFAULT 'presencial',
    confirmado BOOLEAN DEFAULT false,
    data_pagamento TIMESTAMP
);

-- ===========================================
-- TRIGGER PARA ATUALIZAR DATA DE MODIFICAÇÃO EM PEDIDOS
-- ===========================================
CREATE OR REPLACE FUNCTION atualizar_data_pedido()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_pedido_update
BEFORE UPDATE ON pedidos
FOR EACH ROW
EXECUTE FUNCTION atualizar_data_pedido();
