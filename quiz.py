""" Este arquivo cria um aplicativo Flask para gerenciar um site de quizzes dinâmico usando sessões. """
import os  # Importa o módulo os para manipular o sistema de arquivos.
from flask import Flask, session, request, redirect, url_for, render_template  # Importa funções e classes do Flask.
from db_scripts import get_question_after, get_quises  # Importa funções do módulo db_scripts.

def start_quiz(quiz_id):  # Define a função start_quiz para inicializar a sessão.
    """ Cria valores desejados no dicionário de sessão. """
    session['quiz'] = quiz_id  # Armazena o ID do quiz na sessão.
    session['last_question'] = 0  # Inicializa o ID da última pergunta como 0.

def end_quiz():  # Define a função end_quiz para limpar a sessão.
    """ Limpa todos os dados da sessão. """
    session.clear()  # Limpa todos os dados da sessão.

def quiz_form():  # Define a função quiz_form para gerar o formulário de seleção de quiz.
    """ Obtém uma lista de quizzes do banco de dados e formula um formulário com uma lista suspensa. """
    q_list = get_quises()  # Busca a lista de quizzes do banco de dados.
    return render_template('first.html', q_list=q_list)  # Renderiza o template com a lista de quizzes.

def index():  # Define a função index para a página inicial.
    """ Primeira página: se vier com uma requisição GET, escolha um quiz,
    se POST, memorize o ID do quiz e envie para as perguntas. """
    if request.method == 'GET':  # Verifica se o método é GET.
        # O quiz não foi selecionado, reinicia o ID do quiz e mostra o formulário de seleção.
        start_quiz(-1)  # Inicia a sessão com ID inválido.
        return quiz_form()  # Retorna o formulário de seleção.
    else:  # Caso contrário (método POST).
        # Dados adicionais recebidos na requisição! Usa-os.
        quest_id = request.form.get('quiz')  # Obtém o ID do quiz do formulário.
        start_quiz(quest_id)  # Inicia a sessão com o ID escolhido.
        return redirect(url_for('test'))  # Redireciona para a página de teste.

def test():  # Define a função test para a página de perguntas.
    """ Retorna a página de perguntas. """
    # E se um usuário sem escolher um quiz for diretamente para o endereço '/test'?
    if not ('quiz' in session) or int(session['quiz']) < 0:  # Verifica se a sessão é inválida.
        return redirect(url_for('index'))  # Redireciona para a página inicial.
    else:  # Caso contrário.
        # Ainda existe uma versão antiga da função.
        result = get_question_after(session['last_question'], session['quiz'])  # Busca a próxima pergunta.
        if result is None or len(result) == 0:  # Verifica se não há mais perguntas.
            return redirect(url_for('result'))  # Redireciona para o resultado.
        else:  # Caso contrário.
            session['last_question'] = result[0]  # Atualiza o ID da última pergunta.
            # Se ensinarmos o banco de dados a retornar Row ou dict, não devemos escrever result[0] e sim result['id'].
            return '<h1>' + str(session['quiz']) + '<br>' + str(result) + '</h1>'  # Retorna a pergunta como HTML.

def result():  # Define a função result para a página de resultados.
    """ Finaliza o quiz e retorna uma mensagem de fim. """
    end_quiz()  # Limpa a sessão.
    return "isso é tudo pessoal!"  # Retorna uma mensagem de fim.

folder = os.getcwd()  # Armazena o diretório de trabalho atual.
# Cria o objeto do aplicativo web.
app = Flask(__name__, template_folder=folder, static_folder=folder)  # Inicializa o Flask com pastas de templates e estáticos.
                          # O parâmetro named static_folder define o nome da pasta contendo os arquivos estáticos.
                          # O parâmetro named template_folder define o nome da pasta contendo os templates.

app.add_url_rule('/', 'index', index, methods=['post', 'get'])  # Adiciona a rota '/' com métodos GET e POST.
app.add_url_rule('/test', 'test', test)  # Adiciona a rota '/test'.
app.add_url_rule('/result', 'result', result)  # Adiciona a rota '/result'.
# Configura a chave de criptografia.
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'  # Define a chave secreta.

if __name__ == "__main__":  # Verifica se o script é executado diretamente.
    # Inicia o servidor web.
    app.run()  # Executa o aplicativo.
