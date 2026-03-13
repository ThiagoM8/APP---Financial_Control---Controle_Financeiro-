import psycopg2 # Driver profissional para PostgreSQL
import os
from dotenv import load_dotenv

# Carrega as configurações de ambiente (DATABASE_URL do Neon)
load_dotenv()

# --- 1. CONFIGURAÇÃO E CRIAÇÃO ---

def conectar_banco():
    """ Estabelece a conexão com o banco de dados na nuvem (Neon) """
    url = os.getenv('DATABASE_URL')
    return psycopg2.connect(url)

def inicializar_banco():
    """ Cria a tabela no Postgres se ela não existir """
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Criamos a tabela 'movimentacoes'
    # SERIAL: ID autoincremento | TIMESTAMP: Data automática
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS public.movimentacoes (
            id SERIAL PRIMARY KEY,
            whatsapp_id TEXT NOT NULL,
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            descricao TEXT NOT NULL,
            valor NUMERIC(10,2) NOT NULL,
            categoria TEXT NOT NULL)
    ''')
    
    conexao.commit()
    cursor.close()
    conexao.close()

    print('--- PixControl System (Cloud) ---')
    print('Status: Banco de dados configurado e pronto para uso!')

# --- 2. OPERAÇÕES DE DADOS (CRUD) ---

def adicionar_gasto(whatsapp_id, descricao, valor, categoria):
    """ Insere um novo gasto no banco Neon """
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    comando = '''
        INSERT INTO public.movimentacoes (whatsapp_id, descricao, valor, categoria)
        VALUES (%s, %s, %s, %s)
    '''
    
    cursor.execute(comando, (whatsapp_id, descricao, valor, categoria))
    
    conexao.commit()
    cursor.close()
    conexao.close()
    print(f"Gasto de '{descricao}' registrado com sucesso no Neon!")

def listar_gastos(whatsapp_id, mes=None, ano=None):
    """ 
    Lista os gastos de um usuário. 
    Agora aceita filtro de Mês e Ano para resumos inteligentes! 
    """
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Base da query
    query = """
        SELECT id, data_registro, descricao, valor, categoria 
        FROM public.movimentacoes 
        WHERE whatsapp_id = %s
    """
    params = [whatsapp_id]

    # Se o Gemini mandar mês e ano, filtramos no SQL
    if mes and ano:
        query += " AND EXTRACT(MONTH FROM data_registro) = %s AND EXTRACT(YEAR FROM data_registro) = %s"
        params.extend([mes, ano])
    
    query += " ORDER BY data_registro DESC"

    # Executa passando o ID como uma tupla
    cursor.execute(query, tuple(params))
    
    gastos = cursor.fetchall()
    cursor.close()
    conexao.close()
    
    return gastos

def deletar_gasto(id_registro):
    # Função para remover gastos duplicados ou errados
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM public.movimentacoes WHERE id = %s", (id_registro,))
    conexao.commit()
    cursor.close()
    conexao.close()
    print(f"Registro {id_registro} removido com sucesso!")

# --- 3. RELATÓRIOS ---

def resumo_por_categoria(whatsapp_id, mes=None, ano=None):
    # O comando SUM soma os valores e o GROUP BY agrupa por categoria
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    query = """
        SELECT categoria, SUM(valor) 
        FROM public.movimentacoes 
        WHERE whatsapp_id = %s 
    """
    params = [whatsapp_id]

    if mes and ano:
        query += " AND EXTRACT(MONTH FROM data_registro) = %s AND EXTRACT(YEAR FROM data_registro) = %s"
        params.extend([mes, ano])
    else:
        # Se não informar, pega o mês atual
        query += " AND DATE_TRUNC('month', data_registro) = DATE_TRUNC('month', CURRENT_DATE)"

    query += " GROUP BY categoria"
    
    cursor.execute(query, tuple(params))
    resumo = cursor.fetchall()
    cursor.close()
    conexao.close()
    
    return resumo

def total_gasto_mes(whatsapp_id, mes=None, ano=None):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    query = "SELECT SUM(valor) FROM public.movimentacoes WHERE whatsapp_id = %s"
    params = [whatsapp_id]

    if mes and ano:
        query += " AND EXTRACT(MONTH FROM data_registro) = %s AND EXTRACT(YEAR FROM data_registro) = %s"
        params.extend([mes, ano])
    else:
        query += " AND DATE_TRUNC('month', data_registro) = DATE_TRUNC('month', CURRENT_DATE)"

    cursor.execute(query, tuple(params))
    resultado = cursor.fetchone()
    total = resultado[0] if resultado and resultado[0] else 0

    cursor.close()
    conexao.close()

    return total or 0

# --- 4. EXECUÇÃO DO CÓDIGO ---

if __name__ == "__main__":
    # Garante que o banco está pronto na nuvem
    inicializar_banco()