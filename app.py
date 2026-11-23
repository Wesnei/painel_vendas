import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Painel de Vendas", layout="wide")
st.title("Painel de Vendas | Software e Serviços de TI")

MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def brl(valor):
    """Formata em reais no padrão brasileiro: R$ 1.234.567"""
    return f"R$ {valor:,.0f}".replace(",", ".")


@st.cache_data
def carregar_dados():
    df = pd.read_csv("vendas.csv", parse_dates=["data"])
    df["mes_num"] = df["data"].dt.month                 
    df["mes"] = df["mes_num"].map(lambda m: MESES[m - 1])
    return df


df = carregar_dados()

st.sidebar.header("Filtros")
regiao = st.sidebar.selectbox("Região", ["Todas"] + sorted(df["regiao"].unique()))
segmento = st.sidebar.selectbox("Categoria / Segmento", ["Todas"] + sorted(df["segmento"].unique()))

produtos_disponiveis = df if segmento == "Todas" else df[df["segmento"] == segmento]
produto = st.sidebar.selectbox("Produto", ["Todos"] + sorted(produtos_disponiveis["produto"].unique()))

filtrado = df.copy()
if regiao != "Todas":
    filtrado = filtrado[filtrado["regiao"] == regiao]
if segmento != "Todas":
    filtrado = filtrado[filtrado["segmento"] == segmento]
if produto != "Todos":
    filtrado = filtrado[filtrado["produto"] == produto]

if filtrado.empty:
    total = 0.0
    unidades = 0
    pedidos = 0
    ticket = 0.0
    mais_vendido = "Nenhum"
else:
    total = filtrado["valor"].sum()
    unidades = int(filtrado["quantidade"].sum())
    pedidos = filtrado["pedido_id"].nunique()
    ticket = filtrado.groupby("pedido_id")["valor"].sum().mean()
    mais_vendido = filtrado.groupby("produto")["valor"].sum().idxmax()

por_mes = filtrado.groupby(["mes_num", "mes"], as_index=False)["valor"].sum()
por_produto = (
    filtrado.groupby("produto", as_index=False)["valor"]
    .sum()
    .sort_values("valor", ascending=False)
)
por_segmento = filtrado.groupby("segmento", as_index=False)["valor"].sum()

c1, c2, c3, c4, c5 = st.columns([1.3, 1, 0.8, 1.1, 1.3])
c1.metric("Faturamento total", brl(total))
c2.metric("Unidades vendidas", f"{unidades:,}".replace(",", "."))
c3.metric("Pedidos", pedidos)
c4.metric("Ticket médio", brl(ticket))
c5.metric("Maior faturamento", mais_vendido)

if filtrado.empty:
    st.warning("Nenhum registro encontrado para a combinação de filtros selecionada.")
else:
    aba_graficos, aba_dados = st.tabs(["Gráficos Interativos", "Tabela e Exportação"])

    with aba_graficos:
        col_esq, col_dir = st.columns(2)

        with col_esq:
            graf_barras = px.bar(
                por_produto,
                x="produto",
                y="valor",
                title="Faturamento por Produto",
                labels={"produto": "Produto", "valor": "Faturamento (R$)"},
            )
            st.plotly_chart(graf_barras, use_container_width=True)

        with col_dir:
            graf_rosca = px.pie(
                por_segmento,
                names="segmento",
                values="valor",
                hole=0.45,
                title="Participação por Categoria / Segmento",
                labels={"segmento": "Categoria", "valor": "Faturamento (R$)"},
            )
            st.plotly_chart(graf_rosca, use_container_width=True)

        graf_linha = px.line(
            por_mes,
            x="mes",
            y="valor",
            markers=True,
            title=f"Evolução Mensal do Faturamento ({regiao})",
            labels={"mes": "Mês", "valor": "Faturamento (R$)"},
        )
        st.plotly_chart(graf_linha, use_container_width=True)

    with aba_dados:
        colunas = [
            "pedido_id", "data", "regiao", "vendedor", "produto",
            "segmento", "quantidade", "valor_unitario", "valor",
        ]
        tabela = filtrado[colunas].style.format({
            "data": lambda d: d.strftime("%d/%m/%Y"),
            "valor_unitario": brl,
            "valor": brl,
        })
        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=True,
            column_config={
                "pedido_id": "Pedido", "data": "Data", "regiao": "Região",
                "vendedor": "Vendedor", "produto": "Produto", "segmento": "Segmento",
                "quantidade": "Qtd", "valor_unitario": "Valor unit.", "valor": "Valor",
            },
        )

        csv_filtrado = filtrado[colunas].to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="Baixar dados filtrados (CSV)",
            data=csv_filtrado,
            file_name="vendas_filtradas.csv",
            mime="text/csv",
        )