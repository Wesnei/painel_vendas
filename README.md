
# Painel de Vendas com Python (Streamlit + pandas + Plotly)

Aplicação web de exemplo para a aula **"Desenvolvimento de uma aplicação web para análise e visualização de dados com Python"**.

Ideia central: **o dado entra, o Python processa, a interface mostra.**

## Pré-requisitos
- Python 3.9 ou superior

## Como executar
```bash
git clone [https://github.com/Wesnei/painel_vendas.git](https://github.com/Wesnei/painel_vendas.git)
cd painel_vendas
python -m venv venv          # opcional
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

```

O navegador abre em `http://localhost:8501`. Se `streamlit` não for reconhecido, use `python -m streamlit run app.py`.

## Estrutura

| Arquivo | Função |
| --- | --- |
| `app.py` | Código da aplicação (filtros, KPIs, gráficos e exportação) |
| `vendas.csv` | Fonte de dados (`pedido_id`, `data`, `regiao`, `vendedor`, `produto`, `segmento`, `quantidade`, `valor_unitario`, `valor`) |
| `requirements.txt` | Dependências do projeto |

## Fluxo dos dados

1. **Leitura:** `pd.read_csv("vendas.csv", parse_dates=["data"])` com cache (`@st.cache_data`)
2. **Processamento:** filtros reativos (região, segmento e produto), tratamento de base vazia e agregações com `groupby`
3. **Apresentação:** cartões de KPI (`st.metric`), gráficos interativos (`st.plotly_chart`) e tabela exportável (`st.dataframe` + `st.download_button`)

## Glossário rápido

* **Fonte de dados:** de onde vem a informação (CSV, banco de dados, API).
* **Back-end:** o script Python que lê, filtra e processa os dados no servidor.
* **Front-end:** a interface interativa no navegador, renderizada pelo Streamlit.
* **DataFrame:** estrutura tabular em memória do pandas.
* **Framework:** conjunto de ferramentas que acelera a criação da aplicação web (aqui, Streamlit).

## Desafio Prático (Laboratório)

1. **Filtro temporal:** Adicionar um seletor de intervalo de datas (`st.date_input`) na barra lateral para filtrar vendas por período.
2. **Destaque de desempenho:** Criar um indicador (KPI) exibindo o **vendedor líder** em faturamento para o recorte selecionado.
3. **Persistência real:** Substituir a leitura estática do `vendas.csv` por uma consulta SQL em um banco **SQLite** local.

