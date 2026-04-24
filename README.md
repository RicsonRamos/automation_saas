# 🚀 AutoProposta SaaS: De Kaos a Contrato em Segundos

> **A jornada do freelancer e da pequena agência, da proposta perdida ao faturamento inteligente.**

---

## 📖 O Problema: O Ciclo Infinito do "Copia e Cola"

Imagine um cenário comum: você acaba de fechar uma reunião excelente com um cliente em potencial. Ele está animado e pede uma proposta "para ontem". 

Você abre o Word, procura a última proposta enviada para *outro* cliente, começa a apagar nomes, trocar valores, ajustar descrições... e então acontece o erro fatal. Você envia a proposta com o nome do cliente anterior no meio do texto, ou esquece de atualizar o valor total. Além disso, depois de enviada, a proposta some em uma pasta qualquer. Você não sabe quanto tem a receber no mês, quais contratos estão ativos e se a Nota Fiscal já foi emitida.

**O resultado?** Perda de tempo, falta de profissionalismo e um financeiro que é uma caixa preta.

---

## ✨ A Solução: Automação e Gestão Local

O **AutoProposta SaaS** nasceu para ser o "cérebro" comercial do seu negócio. Ele não é apenas um gerador de documentos; é um ecossistema local que transforma conversas em contratos e contratos em receita.

Com uma interface intuitiva, ele centraliza seus clientes, automatiza a criação de documentos profissionais e oferece um painel de controle (Dashboard) que mostra exatamente onde seu dinheiro está e para onde ele vai. Tudo isso rodando localmente, garantindo 100% de privacidade para seus dados.

---

## 🚀 Funcionalidades Principais

### 📊 Dashboard de Performance
Visualize sua saúde financeira instantaneamente. Saiba quanto você já faturou (**Receita Gerada**) e quanto ainda tem por vir (**Receita Esperada**), além de monitorar o volume de vendas mensal.

### 👥 Gestão de Clientes (CRM Light)
Um cadastro centralizado para PF e PJ, mantendo histórico de contatos e documentos sempre à mão.

### 📑 Ciclo de Vida de Documentos
- **Geração Automática:** Crie arquivos `.docx` profissionais a partir de templates, sem erros de digitação.
- **Transição de Status:** Transforme orçamentos em contratos ativos com um clique.
- **Gestão de Prazos:** Nunca mais perca um vencimento de entrega ou de pagamento.

### 💰 Financeiro & Notas Fiscais
Acompanhe o status de cada pagamento e marque a emissão de Notas Fiscais, garantindo que nada escape do seu radar contábil.

---

## 🛠️ Implementação Técnica

O projeto foi construído com foco em **velocidade, robustez e extensibilidade**:

*   **Interface:** [Streamlit](https://streamlit.io/) - Uma interface moderna e responsiva voltada para dados.
*   **Motor de Documentos:** [docxtpl](https://docxtpl.readthedocs.io/) - Utiliza o poder do Jinja2 para injetar dados em arquivos Word mantendo toda a formatação original.
*   **Banco de Dados:** SQLite - Leve, rápido e não requer configuração de servidor.
*   **Arquitetura:** 
    *   `core/db.py`: Gestão de persistência e migrações automáticas.
    *   `core/proposal_generator.py`: Motor de renderização de documentos.
    *   `app.py`: Orquestração da experiência do usuário e lógica de negócio.

---

## 🚦 Como Começar

### 1. Requisitos
- Python 3.9+
- Pip (gerenciador de pacotes)

### 2. Instalação
```bash
# Clone o repositório
git clone https://github.com/RicsonRamos/automation_saas.git

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configuração do Template
Coloque seu arquivo `.docx` na pasta `templates/` e utilize as tags `{{ CLIENTE }}`, `{{ SERVICO }}`, `{{ VALOR }}`, etc.

### 4. Execução
```bash
streamlit run app.py
```

---

## 📈 Próximos Passos (Roadmap)
- [ ] Integração com IA (OpenAI/Gemini) para escrita de escopos.
- [ ] Exportação direta para PDF.
- [ ] Multi-templates (Design, Dev, Consultoria).

---
*Desenvolvido com foco em produtividade por [Ricson Ramos](https://github.com/RicsonRamos).*
