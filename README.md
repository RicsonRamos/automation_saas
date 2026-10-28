# Enterprise Contract Automation and Commercial Governance Platform

Local-First commercial management and contract generation system built with Python, Pydantic, docxtpl, and SQLite, designed to automate document lifecycle and track receivable pipelines with strict schema validation.

---

## 1. Problema de Negócio e Contexto

No gerenciamento comercial de prestadores de serviços e pequenas empresas técnicas, o processo manual de emissão de propostas e contratos impõe sérios riscos jurídicos e operacionais:

1. **Risco de Conformidade e Falhas Humanas:** O método tradicional de "copiar e colar" em editores de texto frequentemente gera incidentes graves, como a manutenção indevida do nome ou dados confidenciais de outros clientes, valores incorretos de parcelas e divergência de cláusulas contratuais.
2. **Invisibilidade Financeira e Descontrole de Caixa:** Após o envio de propostas, a falta de um repositório centralizado impede a gestão do funil comercial, dificultando prever a receita futura (*expected revenue*) e auditar quais notas fiscais e recebimentos foram liquidados.

Esta plataforma foi desenvolvida para substituir processos manuais por um fluxo automatizado e auditável que:
- Valida rigorosamente todos os dados cadastrais e financeiros antes da emissão documental.
- Renderiza contratos em formato `.docx` preservando integralmente o layout corporativo e jurídico original.
- Controla o ciclo de vida da proposta (Em Aberto, Contrato Ativo, Finalizado).
- Monitora os indicadores financeiros de caixa e recebíveis em tempo real.

---

## 2. Processo e Racional das Escolhas Técnicas

### 2.1. Validação Estrita de Schemas com Pydantic
- **Prevenção de Inconsistências:** A manipulação de valores financeiros e registros de clientes (PF/PJ) utiliza schemas Pydantic (`ClienteSchema`, `PropostaSchema`). Erros de tipo, campos obrigatórios ausentes ou valores negativos são interceptados na camada de entrada antes de qualquer inserção no banco de dados.

### 2.2. Motor de Documentos com docxtpl e Jinja2
- **docxtpl vs. Geração em PDF Puro (ReportLab/Weasyprint):** A geração direta em PDF restringe a capacidade do cliente ou departamento jurídico de revisar ou aditivar termos antes da assinatura final. O `docxtpl` permite usar arquivos `.docx` existentes como matrizes de estilo, combinando a flexibilidade do Jinja2 para interpolação de variáveis dinâmicas (`{{ CLIENTE }}`, `{{ VALOR }}`) com a fidelidade tipográfica de documentos legais.

### 2.3. Persistência Relacional Local-First (SQLite)
- **Privacidade Absoluta e Zero Sobrecarga de Infraestrutura:** Dados comerciais de clientes e valores faturados são mantidos em banco relacional local SQLite (`data/app.db`). Essa escolha garante total confidencialidade das propostas comerciais sem custos com instâncias gerenciadas em nuvem.
- **Camada de Acesso a Dados Modular (`core/db.py`):** Inicialização idempotente de tabelas e isolamento de conexões via context managers, facilitando a migração futura para PostgreSQL corporativo se houver expansão multi-usuário.

---

## 3. Resultados Atingidos e Métricas de Validação

### 3.1. Eficiência do Processo Documental
- **Tempo de Emissão:** Redução do ciclo de montagem de propostas de 20 a 30 minutos manuais para emissão determinística em menos de 5 segundos.
- **Eliminação de Erros de Transcrição:** Zero divergência de valores e nomes entre o registro comercial cadastrado e a minuta contratual gerada.

### 3.2. Visibilidade Financeira (Dashboard de Governança)
- **Monitoramento em Tempo Real:** Segregação analítica instantânea entre Receita Realizada (pagamentos liquidados) e Receita Esperada (contratos ativos em fase de execução).
- **Controle Fiscal:** Sinalização visual de status de emissão de Nota Fiscal vinculada a cada contrato.

---

## 4. Arquitetura da Solução e Estrutura

```text
automation_saas/
├── app.py                      # Orquestrador da interface Streamlit e regras de navegação
├── config.yaml                 # Parametrização global de diretórios e padrões
├── populate.py                 # Script de carga inicial para homologação e testes
├── requirements.txt            # Dependências com versões especificadas
├── core/
│   ├── config_loader.py        # Validação de diretórios e carregamento de configurações
│   ├── db.py                   # Criação de schema, conexões SQLite e queries estruturadas
│   ├── proposal_generator.py   # Motor de interpolação Jinja2 sobre modelos docx
│   └── schemas.py              # Modelos Pydantic para validação estrita de dados
├── templates/                  # Modelos de propostas e contratos (.docx)
├── data/                       # Armazenamento do banco SQLite local (app.db)
└── output/                     # Contratos e propostas finais gerados
```

---

## 5. Como Executar

### 5.1. Pré-requisitos
- Python 3.9 ou superior
- Git

### 5.2. Instalação e Execução

1. Clone o repositório:
```bash
git clone https://github.com/RicsonRamos/automation_saas.git
cd automation_saas
```

2. Crie e ative um ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. (Opcional) Popule o banco com registros fictícios de homologação:
```bash
python populate.py
```

5. Inicie a aplicação:
```bash
streamlit run app.py
```
Acesse a aplicação no navegador em `http://localhost:8501`.
