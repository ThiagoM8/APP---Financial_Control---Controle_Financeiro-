import os
import json
from datetime import datetime
import pytz
from dotenv import load_dotenv
from google import genai
# Importa as funções que você criou no database.py
from database import adicionar_gasto, inicializar_banco, listar_gastos

# 1. Lê o arquivo .env e manda a key para o os.
load_dotenv()

# 2. Configura o cliente do Gemini e busca a key no os.
client = genai.Client(api_key = os.getenv("GEMINI_API_KEY")) #os.getenv indica para pegar a key no .env

# 3. Configura o fuso horário (Essencial para o PixControl não errar o dia!)
timezone = pytz.timezone('America/Sao_Paulo')

def processar_e_salvar(whatsapp_id, texto_usuario): #Criei dois parametros, o número do usuario e a entrada do usuario.
    """
    Usa a IA para entender se o usuário quer SALVAR um gasto
    ou VER um resumo (calendário inteligente).
    """
    
    # Obtém a data e hora exata do momento da mensagem
    agora = datetime.now(timezone)
    data_formatada = agora.strftime('%Y-%m-%d %H:%M:%S')
    dia_semana = agora.strftime('%A') # Para ele saber se é 'segunda', 'terça', etc.

    # O Prompt agora inclui o CALENDÁRIO para o Gemini
    prompt = f"""
    Você é o assistente financeiro PixControl. 
    HOJE É: {dia_semana}, {data_formatada}.
    
    Sua tarefa é identificar a intenção do usuário:
    1. Se for um NOVO GASTO: Extraia valor, descrição e categoria.
    2. Se for um PEDIDO DE RESUMO/LISTAGEM: Identifique o mês e o ano solicitados. 
       (Se ele disser 'este mês', use o mês {agora.month}. Se disser 'fevereiro', use mês 2).

    Categorias aceitas: Alimentação, Transporte, Lazer, Saúde, Education, Moradia, Outros.
    
    Mensagem do usuário: "{texto_usuario}"
    
    Responda APENAS um JSON puro.
    Exemplos:
    Para gasto: {{"tipo": "registro", "valor": 25.50, "descricao": "Lanche", "categoria": "Alimentação"}}
    Para resumo: {{"tipo": "resumo", "mes": 2, "ano": 2026}}
    """
    
    try: #Usei o Try/ Except para o código não quebrar com algum erro inesperado
        # Usando o 2.5 Flash
        response = client.models.generate_content(
            model = "gemini-2.5-flash", 
            contents = prompt,
            config = {"response_mime_type": "application/json"} #Obriga a IA a responder em formato JSON
        )
        
        dados = json.loads(response.text) #Pega a frase que vem em texto e transforma em dicionario para o python conseguir ler
        
        # LÓGICA DE DECISÃO DO PIXCONTROL
        if dados.get('tipo') == 'registro': #A função get está buscando o tipo da entrada
            adicionar_gasto( #Caso for um registro, vai chamar a função e inserir o que a IA extraiu
                whatsapp_id, 
                dados['descricao'], 
                dados['valor'], 
                dados['categoria']
            )
            return f"✅ PixControl: {dados['descricao']} (R$ {dados['valor']}) salvo em {dados['categoria']}."

        elif dados.get('tipo') == 'resumo': #Verificar se é resumo, se for ele vai retornar com o resumo
            return f"📊 Entendido! Vou buscar seus gastos de {dados['mes']}/{dados['ano']}."
    
    except Exception as e: #Exception é um objeto já criado pelo python para indicar um erro
        print(f"Erro no processamento: {e}")
        return "❌ Ops! O PixControl se confundiu. Tente: 'Gastei 10 reais em café' ou 'Resumo de Fevereiro'."

# --- EXECUÇÃO DE TESTE ---
if __name__ == "__main__":
    inicializar_banco()
    print("--- PixControl: Sistema de Calendário Ativado ---")
    
    # Teste 1: Registro Normal
    print(processar_e_salvar('551198711822', '16 reais em doces'))
    
    # Teste 2: Pedido de Resumo (O Gemini agora sabe que hoje é Março!)
    print(processar_e_salvar('551198711822', 'Quanto eu gastei em fevereiro?'))