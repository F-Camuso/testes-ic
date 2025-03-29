<h1 align="center">Testes IC</h1>

<p align="center">
    <img src = https://img.shields.io/badge/Python-Linguagem%20-brightgreen>
    <img src="https://img.shields.io/badge/MySQL-Database-blue">
    <img src="https://img.shields.io/badge/Pandas-Library-blue">
    <img src="https://img.shields.io/badge/Flask-Web%20Framework-lightblue">
</p>

---

# Descrição
  * O projeto tem como objetivo realizar extração, tratamento e análise de dados financeiros a partir de diferentes fontes, utilizando web scraping, manipulação de arquivos CSV e PDF, e consulta a bancos de dados. Além disso, possui um front-end desenvolvido em Vue.js que permite realizar a busca das despesas e das operadoras.
---
# Pré-requisitos
``` 
# Instalar dependências
pip install -r requirements.txt

# Copiar o exemplo para o .env e mudar as credenciais de acordo com o que você usa no banco
cp .env-example .env

# Configurar um banco de dados (usei o docker para isso)
docker pull mysql:latest

# Rodar a aplicação
python app.py

# Rodar o banco (eu fiz com o root, se for configurar um usuario novo, basta adicionar os parametros)
docker run --name {nome_container} -e MYSQL_ROOT_PASSWORD={senha} -p 3306:3306 -d mysql:latest

```
---
# Bibliotecas Utilizadas
 * Flask - Back-end da aplicação
 * requests - Requisições HTTP
 * BeautifulSoup - Web scraping
 * pdfplumber - Extração de textos de PDFs
 * pandas - Manipulação de dados
 * mysql-connector-python - Conexão com MySQL
 * Vue.js - Front-end dinâmico 
 * axios - Comunicação entre front-end e back-end
 * csv - Manipulação de arquivos CSV
 * zipfile - Extração de arquivos ZIP
---