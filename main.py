import pyodbc
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.ticker import FuncFormatter
from PIL import Image

# --- 1. Conexão ao Banco de Dados SQL Server (AdventureWorks) ---

# Configurar a conexão ao SQL Server no container
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
uid = os.getenv('DB_UID')
pwd = os.getenv('DB_PWD')

# Criar a string de conexão
connection_string = f'DRIVER={{FreeTDS}};SERVER={server};DATABASE={database};UID={uid};PWD={pwd}'

# Estabelecer a conexão
connection = pyodbc.connect(connection_string)

# Definir a consulta SQL
query = """
SELECT
    soh.OrderDate,
    soh.TotalDue,
    sp.CountryRegionCode,
    prod.Name AS ProductName
FROM Sales.SalesOrderHeader soh
LEFT JOIN Sales.SalesOrderDetail sod ON sod.SalesOrderID = soh.SalesOrderID
LEFT JOIN Person.Address addr ON addr.AddressID = soh.ShipToAddressID
LEFT JOIN Person.StateProvince sp ON sp.StateProvinceID = addr.StateProvinceID
LEFT JOIN Production.Product prod ON prod.ProductID = sod.ProductID
LEFT JOIN Production.ProductSubcategory dps ON dps.ProductSubcategoryID = prod.ProductSubcategoryID
LEFT JOIN Production.ProductCategory dpc ON dpc.ProductCategoryID = dps.ProductCategoryID
"""

# Executar a consulta e carregar os dados em um DataFrame
df = pd.read_sql(query, connection)

# --- 2. Manipulação e Análise de Dados com Python ---

# Filtros interativos no Streamlit
st.title("Dashboard de Vendas - AdventureWorks")

col1, col2 = st.columns(2)

with col1:
    vendas_totais_por_regiao = df.groupby('CountryRegionCode')['TotalDue'].sum().reset_index()
    vendas_totais_por_regiao.rename(columns={'CountryRegionCode': 'Região', 'TotalDue': 'Vendas Totais ($)'}, inplace=True)
    st.subheader("Vendas Totais por Região")
    st.write(vendas_totais_por_regiao)

with col2:
    vendas_totais_por_produto = df.groupby('ProductName')['TotalDue'].sum().reset_index()
    vendas_totais_por_produto.rename(columns={'ProductName': 'Produto', 'TotalDue': 'Vendas Totais ($)'}, inplace=True)
    st.subheader("Vendas Totais por Produto")
    st.write(vendas_totais_por_produto)

col1, col2 = st.columns(2)

with col1:
    vendas_totais_por_ano = df.groupby(df['OrderDate'].dt.to_period('Y'))['TotalDue'].sum().reset_index()
    vendas_totais_por_ano.rename(columns={'OrderDate': 'Ano', 'TotalDue': 'Vendas Totais ($)'}, inplace=True)
    st.subheader("Vendas Totais por Ano")
    st.write(vendas_totais_por_ano)

with col2:
    vendas_totais_por_mes = df.groupby(df['OrderDate'].dt.to_period('M'))['TotalDue'].sum().reset_index()
    vendas_totais_por_mes.rename(columns={'OrderDate': 'Mês', 'TotalDue': 'Vendas Totais ($)'}, inplace=True)
    st.subheader("Vendas Totais por Mês")
    st.write(vendas_totais_por_mes)

# Processar dados
df['OrderDate'] = pd.to_datetime(df['OrderDate'])

# Filtros no Streamlit
st.sidebar.image(Image.open("logo.jpg"), use_column_width=True)
st.sidebar.header("Filtros")
data_inicio = st.sidebar.date_input('Data de início', df['OrderDate'].min())
data_fim = st.sidebar.date_input('Data de fim', df['OrderDate'].max())
produtos = st.sidebar.multiselect('Produto', df['ProductName'].unique())
if not produtos:
    st.sidebar.error("Por favor, selecione pelo menos um produto.")
    st.stop()
regioes = st.sidebar.multiselect('Região', df['CountryRegionCode'].unique())

df_filtrado = df.copy()
if data_inicio:
    df_filtrado = df_filtrado[df_filtrado['OrderDate'] >= pd.to_datetime(data_inicio)]
if data_fim:
    df_filtrado = df_filtrado[df_filtrado['OrderDate'] <= pd.to_datetime(data_fim)]
if regioes:
    df_filtrado = df_filtrado[df_filtrado['CountryRegionCode'].isin(regioes)]
if produtos:
    df_filtrado = df_filtrado[df_filtrado['ProductName'].isin(produtos)]

# --- 3. Criação de Visualizações com Matplotlib ---

# Gráfico de barras - Vendas por produto
fig1, ax1 = plt.subplots()
if not df_filtrado.empty:
    df_filtrado.groupby('ProductName')['TotalDue'].sum().plot(kind='bar', ax=ax1)
ax1.set_ylabel("Valor (R$)")
ax1.set_xlabel("Produto")
ax1.grid(alpha=0.2)
ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'R${x:,.0f}'))

# Gráfico de linhas - Vendas ao longo do tempo
fig2, ax2 = plt.subplots()
if not df_filtrado.empty:
    df_filtrado.groupby(df_filtrado['OrderDate'].dt.to_period('M'))['TotalDue'].sum().plot(kind='line', ax=ax2)
ax2.set_ylabel("Valor (R$)")
ax2.set_xlabel("Data")
ax2.grid(alpha=0.2)
ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'R${x:,.0f}'))

# --- 4. Construção do Dashboard com Streamlit ---

st.subheader("Vendas por Produto")
st.pyplot(fig1)

st.subheader("Vendas ao Longo do Tempo")
st.pyplot(fig2)

# KPI - Total de Vendas no Período Filtrado
st.metric("Total de Vendas", f"R$ {df_filtrado['TotalDue'].sum():,.2f}")
st.metric("Quantidade de Vendas", f"{df_filtrado['ProductName'].count()}")
