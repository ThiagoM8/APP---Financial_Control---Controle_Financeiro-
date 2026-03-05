import sqlite3 

def inicializar_banco():
    # Estabelece conexão com o banco de dados
    # O arquivo 'porquinho.bd' sera criado automaticamente na primeira vez
    conexao = sqlite3.connect('porquinho.db')
    # O cursor é a função que executa os comandos SQL dentro do banco
    cursor = conexao.cursor()

    #Criamos a tabela 'movimentacoes'
    # Usei 'IF NOT EXIST' para o codigo não dar erro se você rodar mais de uma vez
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    # 'commit' salva as alterações de forma permanente no arquivo
    conexao.commit()

    #Sempre fechamos a conexao para não travar o arquivo no sistema
    conexao.close()

    print('--- Porquinho System ---')
    print('Status: Banco de dados configurado e pronto para uso!')

if __name__ == "__main__":
    inicializar_banco()

def adicionar_gasto(whatsapp_id, descricao, valor, categoria):
    # Abre a conexão novamente para inserir
    conexao = sqlite3.connect('porquinho.db')
    cursor = conexao.cursor()
    
    # O comando SQL INSERT INTO
    # Usamos o '?' como um espaço reservado por segurança (evita ataques de SQL Injection)
    comando = '''
        INSERT INTO movimentacoes (whatsapp_id, descricao, valor, categoria)
        VALUES (?, ?, ?, ?)
    '''
    
    # Executa passando os dados reais
    cursor.execute(comando, (whatsapp_id, descricao, valor, categoria))
    
    # Salva e fecha
    conexao.commit()
    conexao.close()
    print(f"Gasto de '{descricao}' registrado com sucesso!")