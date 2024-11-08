from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dbselect import consulta_dados
from replies import *

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return "API do bot está funcionando!"

user_status = {}

@app.route('/bot', methods=['POST'])
def bot():

    resp = MessagingResponse()
    msg = resp.message()

    user_number = request.values.get('From', '')
    original_msg = request.values.get('Body', '') # Mensagem do cliente

    if user_number not in user_status:
        # Primeira interação: pedir o CNPJ
        user_status[user_number] = 'awaiting_response'
        msg.body(Replies.DEFAULT)

    elif user_status[user_number] == 'awaiting_response':
        # Resposta com o CNPJ fornecido pelo usuário
        if len(original_msg) < 8 :
            msg.body(Replies.ERROR_RESPONSE)

        else :
            user_status[user_number] = 'cnpj_received'
            msg.body(consulta_dados(original_msg))
            del user_status[user_number]

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)



