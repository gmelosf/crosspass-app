# CrossPass — Modelo de Negócio Interativo

App Streamlit com modelo financeiro completo, análise de mercado e pitch para o CrossPass, marketplace de CrossFit no Brasil.

## Como rodar localmente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/crosspass-app.git
cd crosspass-app

# Instale as dependências
pip install -r requirements.txt

# Rode o app
streamlit run app.py
```

## Deploy no Streamlit Cloud

1. Faça fork ou push deste repositório para o seu GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório
4. Defina `app.py` como arquivo principal
5. Clique em Deploy

## Estrutura do app

| Página | Conteúdo |
|---|---|
| Visão Geral | KPIs principais, gráficos de EBITDA e caixa |
| Mercado | TAM/SAM/SOM, distribuição de boxes, benchmarks |
| Modelo Financeiro | DRE, Fluxo de Caixa, Balanço resumido |
| Valuation & DCF | FCFF, NPV, TIR, tabela de sensibilidade |
| Unit Economics | LTV/CAC, payback, cohort, retenção |
| Cenários | Bear / Base / Bull comparativo |
| Business Canvas | Canvas completo interativo |
| Pitch | Texto de 2 minutos + análise + exportar CSV |

## Premissas editáveis na sidebar

Todas as premissas são editáveis em tempo real via sliders:

- Número de boxes e alunos por box
- Mensalidade, take rate, adoção máx. Ano 5
- Preço SaaS, CAC, churn mensal, salário do time
- WACC, crescimento na perpetuidade
- Valores de captação (Seed e Série A)

Qualquer alteração recalcula o modelo inteiro instantaneamente.

## Fontes dos dados de mercado

- **Boxes ativos**: crossfit.com/gyms/brazil (mar/2026)
- **Mensalidade média**: Tecnofit, Ativo.com (2024)
- **Ocupação de academia**: ClassPass Industry Report (mar/2026)
- **Crescimento global CrossFit**: Tecnofit Blog (set/2025)
- **ClassPass receita/crescimento**: Reuters / Athletech News (ago/2024)
- **Participantes Open 2024**: Hora do Burpee (mar/2024)

## Aviso

As projeções financeiras são estimativas baseadas em premissas públicas e benchmarks de mercado. Não constituem garantia de resultado.
