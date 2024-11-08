from datetime import datetime
import pyodbc
import os
from dotenv import load_dotenv
from replies import *

# Carregar variáveis do .env
load_dotenv()

# Função para consultar dados do banco de dados
def consulta_dados(cgcclient):
    # Usar variáveis de ambiente para conectar ao banco de dados
    conexao = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')}\\SQLEXPRESS;"
        f"DATABASE={os.getenv('DB_DATABASE')};"
        f"UID={os.getenv('DB_USERNAME')};"
        f"PWD={os.getenv('DB_PASSWORD')}"
    )

    newcgcclient = cgcclient[:8]
    cursor = conexao.cursor()
    cursor.execute(f"SELECT E1_VENCREA, E1_VALOR, E1_NOMCLI, E1_NUM, E1_PARCELA FROM SE1990 WHERE E1_CLIENTE = {newcgcclient}")
    dados = cursor.fetchall()

    qtdtit = len(dados) # Quantidade de titulos em aberto deste cliente
    nomclifull = dados[0][2]
    nomcli = nomclifull.rstrip()

    response = (f"Olá, {nomcli} \n" +
                f"No total você tem {qtdtit} títulos em aberto:\n \n" +
                "\n".join([f"Título: {linha[3].rstrip()} (Parcela {linha[4]})"
                           f"\nVencimento: {datetime.strptime(linha[0], '%Y%m%d').strftime('%d/%m/%Y')}\n"
                           f"Valor: R${linha[1]:.2f}\n "
                for index, linha in enumerate(dados)]))

    if len(response) >= 1600:
        return Replies.ERROR_LENGTH
    else:
        return response