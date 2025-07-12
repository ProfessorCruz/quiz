""" Este arquivo gerencia o banco de dados SQLite para o projeto do quiz.
Inclui funções para conectar, criar tabelas, adicionar dados e buscar perguntas. """
import sqlite3  # Importa a biblioteca sqlite3 para manipulação de bancos de dados.
from random import randint  # Importa a função randint para gerar números aleatórios.

db_name = 'quiz.sqlite'  # Define o nome do arquivo do banco de dados como 'quiz.sqlite'.
conn = None  # Inicializa a variável de conexão como None (será usada globalmente).
cursor = None  # Inicializa o cursor como None (usado para executar comandos SQL).

def open():  # Define a função open para abrir a conexão com o banco de dados.
    """ Abre a conexão com o banco de dados e configura o cursor. """
    global conn, cursor  # Declara conn e cursor como variáveis globais.
    conn = sqlite3.connect(db_name)  # Estabelece a conexão com o banco 'quiz.sqlite'.
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL.

def close():  # Define a função close para fechar a conexão com o banco de dados.
    """ Fecha o cursor e a conexão com o banco de dados. """
    cursor.close()  # Fecha o cursor.
    conn.close()  # Fecha a conexão com o banco de dados.

def do(query):  # Define a função do para executar consultas SQL e confirmar mudanças.
    """ Executa uma consulta SQL e confirma as alterações no banco. """
    cursor.execute(query)  # Executa a consulta SQL passada como argumento.
    conn.commit()  # Confirma as alterações no banco de dados.

def clear_db():  # Define a função clear_db para deletar todas as tabelas existentes.
    """ Deleta todas as tabelas do banco de dados. """
    open()  # Abre a conexão com o banco de dados.
    query = '''DROP TABLE IF EXISTS quiz_content'''  # Define a consulta para deletar a tabela quiz_content, se existir.
    do(query)  # Executa a consulta.
    query = '''DROP TABLE IF EXISTS question'''  # Define a consulta para deletar a tabela question, se existir.
    do(query)  # Executa a consulta.
    query = '''DROP TABLE IF EXISTS quiz'''  # Define a consulta para deletar a tabela quiz, se existir.
    do(query)  # Executa a consulta.
    close()  # Fecha a conexão com o banco de dados.

def create():  # Define a função create para criar as tabelas do banco de dados.
    """ Cria as tabelas quiz, question e quiz_content no banco de dados. """
    open()  # Abre a conexão com o banco de dados.
    cursor.execute('''PRAGMA foreign_keys=on''')  # Ativa suporte a chaves estrangeiras.
    
    do('''CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY, 
            name VARCHAR)'''  # Cria a tabela quiz com id como chave primária e name como campo de texto.
    )
    do('''CREATE TABLE IF NOT EXISTS question (
                id INTEGER PRIMARY KEY, 
                question VARCHAR, 
                answer VARCHAR, 
                wrong1 VARCHAR, 
                wrong2 VARCHAR, 
                wrong3 VARCHAR)'''  # Cria a tabela question com id, pergunta, resposta correta e três opções erradas.
    )
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
                id INTEGER PRIMARY KEY,
                quiz_id INTEGER,
                question_id INTEGER,
                FOREIGN KEY (quiz_id) REFERENCES quiz (id),
                FOREIGN KEY (question_id) REFERENCES question (id) )'''  # Cria a tabela quiz_content com links entre quizzes e perguntas.
    )
    close()  # Fecha a conexão com o banco de dados.

def show(table):  # Define a função show para exibir os dados de uma tabela específica.
    """ Exibe todos os dados de uma tabela especificada. """
    query = 'SELECT * FROM ' + table  # Cria a consulta SQL para selecionar todos os dados da tabela passada.
    open()  # Abre a conexão com o banco de dados.
    cursor.execute(query)  # Executa a consulta SQL.
    print(cursor.fetchall())  # Imprime todas as linhas retornadas pela consulta.
    close()  # Fecha a conexão com o banco de dados.

def show_tables():  # Define a função show_tables para exibir o conteúdo de todas as tabelas.
    """ Exibe o conteúdo das tabelas question, quiz e quiz_content. """
    show('question')  # Chama a função show para exibir os dados da tabela question.
    show('quiz')  # Chama a função show para exibir os dados da tabela quiz.
    show('quiz_content')  # Chama a função show para exibir os dados da tabela quiz_content.

def add_questions():  # Define a função add_questions para adicionar perguntas ao banco.
    """ Adiciona uma lista de perguntas ao banco de dados na tabela question. """
    questions = [
        ('Quantos meses em um ano têm 28 dias?', 'Todos', 'Um', 'Nenhum', 'Dois'),
        ('Como ficará o penhasco verde se cair no Mar Vermelho?', 'Molhado', 'Vermelho', 'Não mudará', 'Roxo'),
        ('Se um avião cair na fronteira entre Brasil e Argentina, onde enterram os sobreviventes?', 'Em lugar nenhum', 'Brasil', 'Argentina', 'Na fronteira'),
        ('O que pesa mais: 1 kg de algodão ou 1 kg de ferro?', 'Pesam o mesmo', 'Ferro', 'Algodão', 'Depende do volume'),
        ('Um trem elétrico está indo para o norte. Para onde vai a fumaça?', 'Não tem fumaça', 'Para o sul', 'Para o norte', 'Para cima'),
        ('Se você jogar uma pedra azul no mar vermelho, o que acontece?', 'Ela afunda', 'Ela boia', 'Ela muda de cor', 'Ela dissolve'),
        ('O pai da Maria tem 4 filhas: Nana, Nene, Nini, Nono. Qual o nome da quinta?', 'Maria', 'Nunu', 'Nana', 'Nene'),
        ('O que acontece se você ficar olhando muito tempo para o sol?', 'Você fica cego', 'Você brilha', 'Ele some', 'Você enxerga melhor'),
        ('Qual é o animal que anda com os pés na cabeça?', 'Piolho', 'Macaco', 'Cobra', 'Pinguim'),
        ('O que não tem comprimento, profundidade, largura ou altura, mas pode ser medido?', 'Tempo', 'Estupidez', 'Mar', 'Ar'),
        ('Quando é possível tirar água com uma rede?', 'Quando a água está congelada', 'Quando não há peixes', 'Quando os peixes dourados nadam para longe', 'Quando a rede quebra'),
        ('O que é maior que um elefante e não pesa nada?', 'Sombra de um elefante', 'Um balão', 'Um paraquedas', 'Uma nuvem'),
        ('O que está no meu bolso?', 'Anel', 'Punho', 'Buraco', 'Pão')
    ]
    open()  # Abre a conexão com o banco de dados.
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''', questions)  # Insere várias perguntas de uma vez.
    conn.commit()  # Confirma as inserções.
    close()  # Fecha a conexão com o banco de dados.

def add_quiz():  # Define a função add_quiz para adicionar quizzes ao banco.
    """ Adiciona uma lista de quizzes ao banco de dados na tabela quiz. """
    quizes = [
        ('Quiz 1', ),
        ('Quiz 2', ),
        ('Quiz estranho', )
    ]
    open()  # Abre a conexão com o banco de dados.
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)  # Insere vários quizzes de uma vez.
    conn.commit()  # Confirma as inserções.
    close()  # Fecha a conexão com o banco de dados.

def add_links():  # Define a função add_links para conectar quizzes a perguntas.
    """ Permite adicionar manualmente links entre quizzes e perguntas na tabela quiz_content. """
    open()  # Abre a conexão com o banco de dados.
    cursor.execute('''PRAGMA foreign_keys=on''')  # Ativa suporte a chaves estrangeiras.
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"  # Define a consulta para inserir links.
    answer = input("Adicionar um link (y/n)?")  # Pede ao usuário se deseja adicionar um link.
    while answer != 'n':  # Loop enquanto o usuário não digitar 'n'.
        quiz_id = int(input("id do quiz: "))  # Pede o ID do quiz.
        question_id = int(input("id da pergunta: "))  # Pede o ID da pergunta.
        cursor.execute(query, [quiz_id, question_id])  # Executa a inserção.
        conn.commit()  # Confirma a inserção.
        answer = input("Adicionar um link (y/n)?")  # Pergunta novamente.
    close()  # Fecha a conexão com o banco de dados.

def auto_link_quizzes_questions():  # Define a função auto_link_quizzes_questions para automação de links.
    """ Esta função vincula automaticamente questões e quizzes na tabela quiz_content para fins de teste.
Ela usa os IDs existentes nas tabelas question e quiz para criar links aleatórios ou sequenciais. """
    open()  # Abre a conexão com o banco de dados.
    cursor.execute('''PRAGMA foreign_keys=on''')  # Ativa suporte a chaves estrangeiras.
    
    # Busca todos os IDs de quizzes disponíveis
    cursor.execute('SELECT id FROM quiz')  # Executa a consulta para obter os IDs de quiz.
    quiz_ids = [row[0] for row in cursor.fetchall()]  # Cria uma lista com os IDs de quiz.
    
    # Busca todos os IDs de perguntas disponíveis
    cursor.execute('SELECT id FROM question')  # Executa a consulta para obter os IDs de question.
    question_ids = [row[0] for row in cursor.fetchall()]  # Cria uma lista com os IDs de question.
    
    # Verifica se há quizzes e perguntas para vincular
    if not quiz_ids or not question_ids:  # Verifica se as listas estão vazias.
        print("Nenhum quiz ou pergunta disponível para vinculação.")  # Exibe mensagem de erro.
        close()  # Fecha a conexão com o banco de dados.
        return  # Sai da função.
    
    # Vincula cada quiz a um número aleatório de perguntas
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"  # Define a consulta para inserir links.
    for quiz_id in quiz_ids:  # Itera sobre cada ID de quiz.
        # Escolhe aleatoriamente entre 1 e o número total de perguntas para vincular
        num_links = randint(1, len(question_ids))  # Gera um número aleatório de links.
        linked_questions = set()  # Usa um conjunto para evitar duplicatas.
        while len(linked_questions) < num_links and len(linked_questions) < len(question_ids):  # Loop até atingir o número de links.
            question_id = question_ids[randint(0, len(question_ids) - 1)]  # Escolhe um ID de pergunta aleatório.
            if question_id not in linked_questions:  # Verifica se a pergunta já foi vinculada.
                linked_questions.add(question_id)  # Adiciona a pergunta ao conjunto.
                cursor.execute(query, [quiz_id, question_id])  # Executa a inserção do link.
    
    conn.commit()  # Confirma todas as inserções no banco de dados.
    close()  # Fecha a conexão com o banco de dados.
    print(f"Vinculados {len(quiz_ids)} quizzes a perguntas de forma aleatória.")  # Exibe mensagem de sucesso.

def get_question_after(last_id=0, vict_id=1):  # Define a função para buscar a próxima pergunta.
    """ Retorna a próxima pergunta após o ID fornecido, com valor padrão para a primeira pergunta. """
    open()  # Abre a conexão com o banco de dados.
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content 
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ? 
    ORDER BY quiz_content.id '''  # Consulta SQL para buscar a próxima pergunta.
    cursor.execute(query, [last_id, vict_id])  # Executa a consulta com os parâmetros.
    result = cursor.fetchone()  # Busca a primeira linha do resultado.
    close()  # Fecha a conexão com o banco de dados.
    return result  # Retorna o resultado.

def get_quises():  # Define a função para listar todos os quizzes.
    """ Retorna uma lista de quizzes (id, name) com uma opção simples por enquanto. """
    query = 'SELECT * FROM quiz ORDER BY id'  # Consulta SQL para listar quizzes.
    open()  # Abre a conexão com o banco de dados.
    cursor.execute(query)  # Executa a consulta.
    result = cursor.fetchall()  # Busca todas as linhas.
    close()  # Fecha a conexão com o banco de dados.
    return result  # Retorna a lista de quizzes.

def get_quiz_count():  # Define a função para contar o número máximo de quiz_id.
    """ Função opcional para obter o maior quiz_id. """
    query = 'SELECT MAX(quiz_id) FROM quiz_content'  # Consulta SQL para encontrar o máximo.
    open()  # Abre a conexão com o banco de dados.
    cursor.execute(query)  # Executa a consulta.
    result = cursor.fetchone()  # Busca o resultado.
    close()  # Fecha a conexão com o banco de dados.
    return result  # Retorna o resultado.

def get_random_quiz_id():  # Define a função para obter um ID de quiz aleatório.
    """ Retorna um ID de quiz aleatório baseado nos dados do quiz_content. """
    query = 'SELECT quiz_id FROM quiz_content'  # Consulta SQL para listar IDs de quizzes.
    open()  # Abre a conexão com o banco de dados.
    cursor.execute(query)  # Executa a consulta.
    ids = cursor.fetchall()  # Busca todos os IDs.
    rand_num = randint(0, len(ids) - 1)  # Gera um número aleatório dentro do intervalo.
    rand_id = ids[rand_num][0]  # Seleciona o ID aleatório.
    close()  # Fecha a conexão com o banco de dados.
    return rand_id  # Retorna o ID aleatório.

def main():  # Define a função principal para inicializar o banco de dados.
    """ Executa a sequência de inicialização do banco de dados. """
    clear_db()  # Limpa o banco de dados.
    create()  # Cria as tabelas.
    add_questions()  # Adiciona perguntas.
    add_quiz()  # Adiciona quizzes.
    show_tables()  # Mostra as tabelas.
    #add_links()  # Adiciona links entre quizzes e perguntas.
    auto_link_quizzes_questions()
    show_tables()  # Mostra as tabelas atualizadas.
    # print(get_question_after(0, 3))  # Comentário de linha desativada para teste.
    # print(get_quiz_count())  # Comentário de linha desativada para teste.
    # print(get_random_quiz_id())  # Comentário de linha desativada para teste.
    pass  # Passa sem ação (placeholder).

if __name__ == "__main__":  # Verifica se o script é executado diretamente.
    main()  # Chama a função principal.
