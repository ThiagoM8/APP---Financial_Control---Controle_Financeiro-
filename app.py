from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from brain import processar_e_salvar
from database import inicializar_banco
import os

app = Flask(__name__)

# garante que a tabela existe ao iniciar o servidor
inicializar_banco()

# memória temporária para mapear lista exibida → ids reais
mapa_gastos = {}

@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():

    whatsapp_id = request.values.get('From', '')
    mensagem_usuario = request.values.get('Body', '')

    print(f"Mensagem recebida de {whatsapp_id}: {mensagem_usuario}")

    mensagem = mensagem_usuario.lower().strip()

    # --- COMANDO RESUMO ---
    if mensagem == "resumo":

        from database import resumo_por_categoria

        dados = resumo_por_categoria(whatsapp_id)

        resposta = "📊 *Resumo por categoria*\n\n"

        for categoria, total in dados:
            resposta += f"{categoria}: R$ {round(total,2)}\n"

    # --- COMANDO GASTOS ---
    elif mensagem == "gastos":

        from database import listar_gastos

        gastos = listar_gastos(whatsapp_id)

        resposta = "🧾 *Seus últimos gastos*\n\n"

        lista_ids = []

        for i, g in enumerate(gastos[:10], start=1):
            resposta += f"{i}️⃣ {g[2]} - R$ {g[3]} ({g[4]})\n"
            lista_ids.append(g[0])

        mapa_gastos[whatsapp_id] = lista_ids

        resposta += "\nDigite: apagar número"

    # --- COMANDO APAGAR ---
    elif mensagem.startswith("apagar"):

        from database import deletar_gasto

        try:
            numero = int(mensagem.split(" ")[1])

            id_real = mapa_gastos[whatsapp_id][numero - 1]

            deletar_gasto(id_real)

            resposta = "🗑️ Gasto removido com sucesso!"

        except:
            resposta = "❌ Use: apagar número\nExemplo: apagar 2"

    # --- MENSAGEM NORMAL (IA) ---
    else:

        resposta = processar_e_salvar(whatsapp_id, mensagem_usuario)

    # resposta para o WhatsApp
    resp = MessagingResponse()
    resp.message(resposta)

    return str(resp)


# --- INICIALIZAÇÃO DO SERVIDOR ---
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    print(f"Iniciando servidor na porta {port}...")

    app.run(host='0.0.0.0', port=port)