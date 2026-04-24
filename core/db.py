import sqlite3
from pathlib import Path

DB_PATH = Path("data/app/db.sqlite")  # inclua a extensão .sqlite

def get_connection():
    """Estabelece e retorna uma conexão com o banco de dados SQLite."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # Garante que o diretório exista
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_db():
    """Inicializa o banco de dados com as tabelas necessárias e realiza migrações simples."""
    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # Tabela de clientes
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            tipo TEXT,
            cpf_cnpj TEXT,
            email TEXT,
            telefone TEXT
        );
    """)

    # -------------------------
    # Tabela de propostas / projetos
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS propostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            servico TEXT,
            descricao TEXT,
            prazo TEXT,
            valor REAL,
            file_path TEXT,
            version INTEGER
        );
    """)

    # Migração simples: Adiciona colunas se não existirem
    columns_to_add = [
        ("status", "TEXT DEFAULT 'Orçamento'"),
        ("data_vencimento", "DATE"),
        ("nf_emitida", "BOOLEAN DEFAULT 0")
    ]
    
    cursor.execute("PRAGMA table_info(propostas)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    for col_name, col_type in columns_to_add:
        if col_name not in existing_columns:
            cursor.execute(f"ALTER TABLE propostas ADD COLUMN {col_name} {col_type}")

    # -------------------------
    # Tabela de financeiro (Pagamentos)
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financeiro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposta_id INTEGER UNIQUE, -- Garante pagamento único por proposta
            valor REAL,
            data_vencimento DATE,
            data_pagamento DATE,
            status TEXT DEFAULT 'Pendente',
            FOREIGN KEY (proposta_id) REFERENCES propostas(id)
        );
    """)

    # -------------------------
    # Tabela de Histórico de Status
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposta_id INTEGER,
            status_anterior TEXT,
            status_novo TEXT,
            data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (proposta_id) REFERENCES propostas(id)
        );
    """)

    conn.commit()
    conn.close()
