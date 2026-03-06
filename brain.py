import os
import json
from dotenv import load_dotenv
from google import genai
# Importa as funções que você criou no database.py (agora com Postgres)
from database import adicionar_gasto, inicializar_banco

# 1. Carrega as configurações de ambiente (Gemini API e DATABASE_URL)
load_dotenv()

# 2. Configura o cliente do Gemini 
# No Render, garante que a chave se chama GEMINI_API_KEY
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def processar_e_salvar(whatsapp_id, texto_usuario):
    """
    Usa a IA para traduzir o texto do usuário em dados estruturados
    e salva no banco de dados Neon (PostgreSQL).
    """
    
    # O Prompt ensina a IA a ser o "Tradutor" do PiggyWise
    prompt = f"""
    Você é o assistente financeiro PiggyWise. 
    Extraia o valor (float), a descrição e a categoria da mensagem abaixo.
    
    Categorias aceitas: Alimentação, Transporte, Lazer, Saúde, Educação, Moradia, Outros.
    
    Mensagem do usuário: "{texto_usuario}"
    
    Responda APENAS um JSON puro, sem formatação markdown (sem as crases ```json).
    Exemplo de resposta: {{"valor": 25.50, "descricao": "Lanche", "categoria": "Alimentação"}}
    """
    
    try:
        # Chama o modelo 2.0 Flash para processamento ultra rápido
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        # Limpeza de possíveis formatações que a IA possa enviar por engano (Markdown)
        # Ajustado para evitar o erro de parênteses que tivemos antes!
        dados_limpos = response.text.strip().replace('```json', '').replace('```', '')
        dados = json.loads(dados_limpos)
        
        # Chama a função de banco de dados para persistir a informação no Neon
        adicionar_gasto(
            whatsapp_id, 
            dados['descricao'], 
            dados['valor'], 
            dados['categoria']
        )
        
        return f"✅ Sucesso! {dados['descricao']} (R$ {dados['valor']}) salvo em {dados['categoria']}."
    
    except Exception as e:
        # Log de erro para você acompanhar no painel do Render
        print(f"Erro no processamento: {e}")
        return "❌ Ops! Não consegui entender esse gasto. Tente algo como: 'Gastei 50 no mercado'."

# --- EXECUÇÃO DE TESTE ---
if __name__ == "__main__":
    # Garante que a tabela exista no banco de dados Neon
    inicializar_banco()
    
    print("--- PiggyWise: Iniciando Processamento na Nuvem ---")
    
    # Simulando uma mensagem vinda do WhatsApp para teste
    resultado = processar_e_salvar('5511999999999', 'Gastei 45 reais no cinema com a Gigi')
    
    print(resultado)

    # commit final