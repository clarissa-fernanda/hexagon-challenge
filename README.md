
# AdventureWorks Dashboard

Este projeto configura um dashboard interativo com Streamlit para visualizar dados de vendas do banco de dados AdventureWorks, utilizando um ambiente Docker com SQL Server e Python.

## Requisitos

- Docker
- Docker Compose

## Configuração

1. Clone este repositório:

```bash
git clone https://github.com/clarissa-fernanda/hexagon-challenge
cd hexagon-challenge
```

2. Configure o ambiente Docker executando o comando:

```bash
docker compose up -d --build --wait
```

Isso fará o download da imagem do SQL Server e configurará o banco de dados AdventureWorks, além de iniciar o servidor Streamlit.

## Estrutura do Projeto

- `docker-compose.yml`: Define os serviços do Docker (banco de dados SQL Server e aplicação Streamlit).
- `restore-db.sh`: Script para baixar e restaurar o banco de dados AdventureWorks 2019.
- `requirements.txt`: Dependências de Python necessárias para o funcionamento do dashboard.
- `main.py`: Script principal que conecta ao banco de dados SQL Server, executa consultas e exibe os resultados em um dashboard interativo usando Streamlit.
- `Dockerfile`: Configura o ambiente Python e as dependências de sistema para conectar ao SQL Server.

## Como Usar

1. Acesse o dashboard no navegador, disponível em:

```
http://localhost:8501
```

2. Utilize os filtros interativos na barra lateral para selecionar períodos de data, produtos e regiões para análise das vendas.

## Funcionalidades do Dashboard

- **Vendas por Região**: Exibe o total de vendas por código de região.
- **Vendas por Produto**: Exibe o total de vendas por produto.
- **Vendas por Ano e Mês**: Exibe o total de vendas por ano e mês.
- **Gráficos**: Gráficos de barras e de linhas que mostram as vendas totais por produto e ao longo do tempo.

## Tecnologias Utilizadas

- **Python 3.12**
- **Streamlit** para criação do dashboard interativo.
- **Matplotlib** para visualização de dados.
- **Pandas** para manipulação de dados.
- **PyODBC** para conexão ao banco de dados SQL Server.
- **SQL Server** para o armazenamento de dados.
- **Docker** para gerenciar containers dos serviços de banco de dados e da aplicação.

## Banco de Dados

O banco de dados utilizado é o [AdventureWorks2019](https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorks2019.bak), um banco de dados de amostra para demonstração de funcionalidades.
