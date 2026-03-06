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
    # Estabelece conexão com o banco de dados na nuvem
    # A tabela sera criada automaticamente se não existir
    conexao = conectar_banco()
    
    # O cursor é a função que executa os comandos SQL dentro do banco
    cursor = conexao.cursor()

    # Criamos a tabela 'movimentacoes'
    # Usei 'IF NOT EXISTS' para o codigo não dar erro se você rodar mais de uma vez
    # No Postgres, usamos SERIAL para o autoincremento e TIMESTAMP para data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id SERIAL PRIMARY KEY,
            whatsapp_id TEXT NOT NULL,
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL)
    ''')
    
    '''
    -- ID único gerado automaticamente
    -- Guarda o número de quem enviou
    -- Data e hora automática do gasto
    -- O que você comprou
    -- Quanto custou
    -- Categoria
    '''

    # 'commit' salva as alterações de forma permanente no servidor
    conexao.commit()

    # Sempre fechamos o cursor e a conexao para não travar o sistema
    cursor.close()
    conexao.close()

    print('--- Porquinho System (Cloud) ---')
    print('Status: Banco de dados configurado e pronto para uso!')

# --- 2. OPERAÇÕES DE DADOS (CRUD) ---

def adicionar_gasto(whatsapp_id, descricao, valor, categoria):
    # Abre a conexão novamente para inserir na nuvem
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # O comando SQL INSERT INTO
    # No PostgreSQL usamos o '%s' como espaço reservado por segurança
    comando = '''
        INSERT INTO movimentacoes (whatsapp_id, descricao, valor, categoria)
        VALUES (%s, %s, %s, %s)
    '''
    
    # Executa passandoos dados reais
    cursor.execute(comando, (whatsapp_id, descricao, valor, categoria))
    
    # Salva e fecha
    conexao.commit()
    cursor.close()
    conexao.close()
    print(f"Gasto de '{descricao}' registrado com sucesso no Neon!")

def listar_gastos(whatsapp_id):
    # Conecta ao banco no Neon
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Selecionamos tudo da tabela onde o ID seja igual ao de quem pediu
    cursor.execute("SELECT data_registro, descricao, valor, categoria FROM movimentacoes WHERE whatsapp_id = %s", (whatsapp_id,))
    
    gastos = cursor.fetchall()
    cursor.close()
    conexao.close()
    
    return gastos

def deletar_gasto(id_registro):
    # Função para remover gastos duplicados ou errados
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM movimentacoes WHERE id = %s", (id_registro,))
    conexao.commit()
    cursor.close()
    conexao.close()
    print(f"Registro {id_registro} removido com sucesso!")

# --- 3. RELATÓRIOS ---

def resumo_por_categoria(whatsapp_id):
    # O comando SUM soma os valores e o GROUP BY agrupa por categoria
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    query = """
        SELECT categoria, SUM(valor) 
        FROM movimentacoes 
        WHERE whatsapp_id = %s 
        GROUP BY categoria
    """
    
    cursor.execute(query, (whatsapp_id,))
    resumo = cursor.fetchall()
    cursor.close()
    conexao.close()
    
    return resumo

# --- 4. EXECUÇÃO DO CÓDIGO ---

if __name__ == "__main__":
    # Garante que o banco está pronto na nuvem
    inicializar_banco()