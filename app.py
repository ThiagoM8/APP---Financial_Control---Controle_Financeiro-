import threading
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client # Importante para enviar mensagens na thread
from brain import processar_e_salvar
from database import inicializar_banco

app = Flask(__name__)

# Configuração do Cliente Twilio para envio ativo (Background)
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_client = Client(account_sid, auth_token)

# Garante que a tabela existe ao iniciar o servidor
inicializar_banco()

# Memória temporária para mapear lista exibida → ids reais
mapa_gastos = {}

# --- TEXTO DO MENU ---
MENU_TEXTO = """
👋 *Olá! Sou o seu assistente PixControl.*

Como posso ajudar? Escolha uma opção:

*1.* 📊 *Resumo por categoria*
*2.* 🧾 *Ver últimos gastos*
*3.* 🗑️ *Apagar um gasto* (ex: apagar 1)
*4.* ❓ *Ajuda*

_Ou apenas digite o gasto (ex: Almoço 30 reais)_
"""

def tarefa_pesada(whatsapp_id, mensagem_usuario, de_numero):
    """
    Esta função roda em segundo plano. Ela processa a IA e 
    envia a mensagem de volta quando estiver pronto.
    """
    mensagem = mensagem_usuario.lower().strip()
    resposta = ""

    # --- Lógica de Comandos (Movida para cá) ---
    
    # Se for uma saudação ou opção de ajuda, exibe o menu
    if mensagem in ["oi", "ola", "olá", "menu", "ajuda", "4"]:
        resposta = MENU_TEXTO

    elif mensagem == "resumo" or mensagem == "1":
        from database import resumo_por_categoria
        dados = resumo_por_categoria(whatsapp_id)
        resposta = "📊 *Resumo por categoria*\n\n"
        if not dados:
            resposta += "Nenhum gasto registrado este mês."
        for categoria, total in dados:
            resposta += f"{categoria}: R$ {round(total,2)}\n"

    elif mensagem == "gastos" or mensagem == "2":
        from database import listar_gastos
        gastos = listar_gastos(whatsapp_id)
        resposta = "🧾 *Seus últimos gastos*\n\n"
        lista_ids = []
        for i, g in enumerate(gastos[:10], start=1):
            # Mudei de {i}️⃣ para um formato mais limpo (Corrigindo o erro visual do 10)
            resposta += f"*{i}.* {g[2]} - R$ {g[3]} ({g[4]})\n"
            lista_ids.append(g[0])
        mapa_gastos[whatsapp_id] = lista_ids
        resposta += "\nDigite: *apagar número*"

    elif mensagem.startswith("apagar") or mensagem == "3":
        if mensagem == "3":
            resposta = "Para apagar, primeiro digite *2* para ver a lista e depois *apagar número*."
        else:
            from database import deletar_gasto
            try:
                partes = mensagem.split(" ")
                if len(partes) > 1:
                    numero = int(partes[1])
                    id_real = mapa_gastos[whatsapp_id][numero - 1]
                    deletar_gasto(id_real)
                    resposta = "🗑️ Gasto removido com sucesso!"
                else:
                    resposta = "❌ Informe o número. Ex: apagar 1"
            except:
                resposta = "❌ Erro ao apagar. Verifique o número na lista."

    else:
        # Aqui é onde o Gemini brilha (e demora)
        resposta = processar_e_salvar(whatsapp_id, mensagem_usuario)

    # ENVIO ATIVO: O Twilio envia a mensagem de volta para o usuário
    twilio_client.messages.create(
        from_=de_numero, # O número do seu Bot (Sandbox)
        body=resposta,
        to=whatsapp_id
    )

@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    whatsapp_id = request.values.get('From', '')
    mensagem_usuario = request.values.get('Body', '')
    meu_numero_twilio = request.values.get('To', '') # Pega o número do bot

    print(f"Mensagem recebida de {whatsapp_id}: {mensagem_usuario}")

    # DISPARA A THREAD E SEGUE A VIDA
    threading.Thread(target=tarefa_pesada, args=(whatsapp_id, mensagem_usuario, meu_numero_twilio)).start()

    # RESPONDE AO TWILIO IMEDIATAMENTE (Status 200)
    # Isso evita o erro de 15 segundos (Timeout)
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Iniciando servidor na porta {port}...")
    app.run(host='0.0.0.0', port=port)