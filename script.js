let tentativas = []; // Array para armazenar as tentativas do jogador

function enviarPalavra() {
    var palavra = document.getElementById('palavra').value;

    fetch('/verificar_palavra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'palavra=' + encodeURIComponent(palavra)
    })
    .then(response => response.json())
    .then(data => {
        // Salva a tentativas
        tentativas.push(palavra);
        document.getElementById('mensagem').textContent = data.mensagem;

        // Atualiza a lista de tentativas
        document.getElementById('tentativas').innerHTML = tentativas.map(tentativa => `<li>${tentativa}</li>`).join('');

        // Mostra tentativas restantes
        document.getElementById('tentativas-restantes').textContent = `Tentativas restantes: ${data.tentativas_restantes}`;

        // Verifica se o jogo acabou
        if (data.fim) {
            document.getElementById('palavra').disabled = true;
        } else {
            // Limpa o campo
            document.getElementById('palavra').value = '';
            document.getElementById('letras-erradas').textContent = `Você errou a palavra: '${palavra}'. Letras erradas: ${data.letras_erradas.join(', ')}. Letras corretas: ${data.letras_certas.join(', ')}`;
        }
    });
}

// Função para permitir o envio ao pressionar Enter
document.getElementById('palavra').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        enviarPalavra();
    }
});
