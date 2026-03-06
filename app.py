from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from brain import processar_e_salvar # Importa a lógica da IA que você já validou!
import os

app = Flask(__name__)

# --- ROTA PARA O WHATSAPP ---

@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    """
    Essa é a função principal que o Twilio chama quando 
    chega uma mensagem nova no seu número.
    """
    
    # 1. Captura o número de quem enviou e o texto da mensagem
    # O Twilio manda isso dentro do formulário da requisição
    whatsapp_id = request.values.get('From', '')
    mensagem_usuario = request.values.get('Body', '')

    print(f"Mensagem recebida de {whatsapp_id}: {mensagem_usuario}")

    # 2. Chama o 'Cérebro' do Porquinho para entender o gasto e salvar no Neon
    # O brain.py vai retornar uma frase confirmando o sucesso ou erro
    resposta_ia = processar_e_salvar(whatsapp_id, mensagem_usuario)

    # 3. Prepara a resposta para devolver ao WhatsApp via Twilio
    resp = MessagingResponse()
    resp.message(resposta_ia)

    return str(resp)

# --- INICIALIZAÇÃO DO SERVIDOR ---

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f" Iniciando servidor na porta {port}...") 
    app.run(host='0.0.0.0', port=port)

    # commit final