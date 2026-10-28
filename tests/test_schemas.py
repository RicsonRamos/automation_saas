import pytest
from datetime import date
from pydantic import ValidationError
from core.schemas import ClienteSchema, PropostaSchema

def test_cliente_schema_valido():
    cliente = ClienteSchema(
        nome="Empresa Teste",
        tipo="PJ",
        cpf_cnpj="00.000.000/0001-00",
        email="contato@empresa.com",
        telefone="(11) 99999-9999"
    )
    assert cliente.nome == "Empresa Teste"
    assert cliente.tipo == "PJ"

def test_cliente_schema_tipo_invalido():
    with pytest.raises(ValidationError):
        ClienteSchema(nome="Nome Teste", tipo="OUTRO")

def test_proposta_schema_valida():
    proposta = PropostaSchema(
        cliente_id=1,
        servico="Desenvolvimento de Software",
        descricao="Sistema de automação analítica",
        valor=1500.00,
        prazo="30 dias",
        data_vencimento="2026-12-31"
    )
    assert proposta.valor == 1500.00
    assert proposta.data_vencimento == date(2026, 12, 31)

def test_proposta_schema_valor_negativo():
    with pytest.raises(ValidationError):
        PropostaSchema(
            cliente_id=1,
            servico="Consultoria",
            descricao="Descricao",
            valor=-100.0,
            prazo="15 dias",
            data_vencimento=date(2026, 12, 31)
        )
