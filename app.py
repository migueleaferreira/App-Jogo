from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'segredo'  # Necessário para usar sessões

# Lista de palavras-chave
palavras_chaves = ["cachorro", "gato", "elefante", "tigre", "papagaio", "leao", "cobra", "zebra", "girafa", "urso"]
palavra_secreta = random.choice(palavras_chaves)
max_tentativas = 5  # Define o número máximo de tentativas

# Rota principal para carregar a página
@app.route('/')
def index():
    session['tentativas_restantes'] = max_tentativas  # Reinicia as tentativas a cada nova partida
    session['palavra_secreta'] = palavra_secreta  # Armazena a palavra secreta na sessão
    return render_template('index.html', num_letras=len(palavra_secreta))  # Passa a quantidade de letras para o template

# Rota para processar as tentativas do jogador
@app.route('/verificar_palavra', methods=['POST'])
def verificar_palavra():
    if 'tentativas_restantes' not in session:
        session['tentativas_restantes'] = max_tentativas  # Inicializa as tentativas se não estiverem na sessão
    
    palavra_jogador = request.form['palavra'].lower()
    session['tentativas_restantes'] -= 1  # Decrementa o número de tentativas

    proximidade = sum(1 for a, b in zip(palavra_jogador, session['palavra_secreta']) if a == b)

    # Identifica letras que estão erradas e corretas
    letras_erradas = [letra for letra in palavra_jogador if letra not in session['palavra_secreta']]
    letras_certas = [letra for letra in palavra_jogador if letra in session['palavra_secreta'] and letra not in letras_erradas]

    # Verifica se o jogador acertou ou se as tentativas acabaram
    if palavra_jogador == session['palavra_secreta']:
        return jsonify({'mensagem': 'Parabéns, você acertou!', 'fim': True, 'letras_erradas': [], 'letras_certas': letras_certas, 'tentativas_restantes': session['tentativas_restantes']})
    elif session['tentativas_restantes'] <= 0:
        return jsonify({'mensagem': f'Suas tentativas acabaram! A palavra era: {session["palavra_secreta"]}.', 'fim': True, 'letras_erradas': [], 'letras_certas': letras_certas, 'tentativas_restantes': 0})
    else:
        return jsonify({'mensagem': f'Sua palavra tem {proximidade} letras corretas.', 'fim': False, 'letras_erradas': letras_erradas, 'letras_certas': letras_certas, 'tentativas_restantes': session['tentativas_restantes']})

if __name__ == '__main__':
    app.run(debug=True)
