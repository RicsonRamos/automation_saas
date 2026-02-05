import sqlite3
from pathlib import Path

DB_PATH = Path("data/app/db.sqlite")  # inclua a extensão .sqlite

def get_connection():
    """Estabelece e retorna uma conexão com o banco de dados SQLite."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # Garante que o diretório exista
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_db():
    """Inicializa o banco de dados com as tabelas necessárias."""
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
    # Tabela de propostas
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
            version INTEGER,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );
    """)

    conn.commit()
    conn.close()
