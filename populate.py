import sqlite3
from datetime import datetime

DB_PATH = "data/app/db.sqlite"

def populate_db():
    """Popular as tabelas clientes e propostas com dados de exemplo"""
    # Conectar ao banco de dados
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Inserir alguns clientes fictícios
    clientes = [
        ("João Silva", "PF", "123.456.789-10", "joao@exemplo.com", "(11) 99999-8888"),
        ("Maria Oliveira", "PF", "234.567.890-11", "maria@exemplo.com", "(21) 98888-7777"),
        ("Empresa XYZ", "PJ", "12.345.678/0001-99", "contato@empresa.com", "(31) 97777-6666")
    ]
    cursor.executemany("""
        INSERT INTO clientes (nome, tipo, cpf_cnpj, email, telefone)
        VALUES (?, ?, ?, ?, ?)
    """, clientes)

    # Inserir algumas propostas fictícias
    propostas = [
        (1, "Serviço de Consultoria", "Consultoria em TI", "30 dias", 1500.00, "2023-02-01", 1, "proposta_1.docx"),
        (2, "Desenvolvimento de Sistema", "Criação de aplicativo web", "60 dias", 5000.00, "2023-02-05", 1, "proposta_2.docx"),
        (3, "Treinamento Corporativo", "Treinamento para equipe de vendas", "15 dias", 3000.00, "2023-02-10", 2, "proposta_3.docx")
    ]
    cursor.executemany("""
        INSERT INTO propostas (cliente_id, servico, descricao, prazo, valor, date_created, version, file_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, propostas)

    # Commit e fechar a conexão
    conn.commit()
    conn.close()

    print("Dados de exemplo inseridos com sucesso!")

__main__ = populate_db()