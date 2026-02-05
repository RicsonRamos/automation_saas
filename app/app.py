from core.proposal_generator import generate_proposal

data = {
    "cliente_nome": "Cliente Exemplo",
    "cliente_tipo": "PJ",
    "servico": "Análise Exploratória de Dados",
    "descricao": "Análise inicial dos dados para identificação de padrões.",
    "prazo": "15 dias",
    "valor": "3.500,00"
}

path = generate_proposal(data)
print(f"Proposta gerada em: {path}")
