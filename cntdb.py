from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import pyodbc

# # Função para consultar dados do banco de dados
def consulta_dados(cgcclient):
    conexao = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=RECN100100309\\SQLEXPRESS;DATABASE=protheus1212210;UID=sa;PWD=250900'
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

    return response


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "API do bot está funcionando!"

@app.route('/bot', methods=['POST'])
def bot():
    resp = MessagingResponse()
    msg = resp.message()
    # msg.body("Digite o seu CNPJ ou CPF (Sem . / -)")

    original_msg = request.values.get('Body', '') # Mensagem do cliente
    msg.body(consulta_dados(original_msg)) # Retorno ao cliente

    consulta_dados(original_msg)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)



