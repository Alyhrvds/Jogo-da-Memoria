import pygame
import random
import time
import os

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Memória")

# Paleta de cores
cor_fundo = (60, 78, 105)  # #3C4E69
cor_carta = (139, 164, 213)  # #8BA4D5
cor_texto = (255, 247, 238)  # #FFF7EE
cor_borda = (255, 154, 105)  # #FF9A69
cor_preto = (0, 0, 0)

# Configuração das cartas
linhas = 4
colunas = 4
largura_carta = 100
altura_carta = 100
espacamento = 20
offset_superior = 80  # Move as cartas para baixo

# Carregar imagens
caminho_imagens = "imagens"
imagens_disponiveis = [img for img in os.listdir(caminho_imagens) if img.endswith(".png")]
random.shuffle(imagens_disponiveis)

# Seleciona imagens para formar os pares
imagens_selecionadas = imagens_disponiveis[:(linhas * colunas) // 2] * 2
random.shuffle(imagens_selecionadas)

# Estrutura para armazenar as cartas
cartas = []
indice = 0
for linha in range(linhas):
    linha_cartas = []
    for coluna in range(colunas):
        imagem = pygame.image.load(os.path.join(caminho_imagens, imagens_selecionadas[indice]))
        imagem = pygame.transform.scale(imagem, (largura_carta, altura_carta))
        linha_cartas.append({
            "imagem": imagem, 
            "revelada": False, 
            "coordenadas": (coluna, linha),
            "id": imagens_selecionadas[indice]  # Identificador da carta
        })
        indice += 1
    cartas.append(linha_cartas)

# Controle das cartas viradas
cartas_viradas = []
bloqueio = False
vidas = 5  # Vidas iniciais
pares_encontrados = 0

# Carregar a fonte personalizada
fonte_tentativas = pygame.font.Font(None, 36)  # Tamanho de 36 para as tentativas
fonte_vitoria = pygame.font.Font(None, 48)  # Tamanho de 48 para a mensagem de vitória
fonte_derrota = pygame.font.Font(None, 48)  # Tamanho de 48 para a mensagem de derrota

# Função para desenhar o jogo
def desenhar_jogo():
    tela.fill(cor_fundo)

    # Exibir tentativas e acertos
    texto_vidas = fonte_tentativas.render(f"Vidas: {vidas}", True, cor_texto)
    texto_acertos = fonte_tentativas.render(f"Acertos: {pares_encontrados}", True, cor_texto)
    tela.blit(texto_vidas, (10, 10))
    tela.blit(texto_acertos, (largura - 200, 10))

    # Desenhar as cartas
    for linha in range(linhas):
        for coluna in range(colunas):
            carta = cartas[linha][coluna]
            x = coluna * (largura_carta + espacamento) + espacamento
            y = linha * (altura_carta + espacamento) + espacamento + offset_superior  # Move para baixo

            if carta["revelada"]:
                tela.blit(carta["imagem"], (x, y))
            else:
                pygame.draw.rect(tela, cor_carta, (x, y, largura_carta, altura_carta))
                pygame.draw.rect(tela, cor_borda, (x, y, largura_carta, altura_carta), 5)  # Borda na carta

    pygame.display.update()

# Função para mostrar a tela de vitória
def mostrar_vitoria():
    tela.fill(cor_fundo)
    mensagem_vitoria = f"Você venceu com {pares_encontrados} acertos e {5 - vidas} vidas restantes!"
    texto_vitoria_msg = fonte_vitoria.render(mensagem_vitoria, True, cor_texto)

    # Centraliza o texto na tela
    texto_rect = texto_vitoria_msg.get_rect(center=(largura // 2, altura // 2))
    tela.blit(texto_vitoria_msg, texto_rect)

    pygame.display.update()
    time.sleep(3)

# Função para mostrar a tela de derrota
def mostrar_derrota():
    tela.fill(cor_fundo)
    mensagem_derrota = f"Você perdeu! Acertos: {pares_encontrados}"
    texto_derrota_msg = fonte_derrota.render(mensagem_derrota, True, cor_texto)

    # Centraliza o texto na tela
    texto_rect = texto_derrota_msg.get_rect(center=(largura // 2, altura // 2))
    tela.blit(texto_derrota_msg, texto_rect)

    pygame.display.update()
    time.sleep(3)

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN and not bloqueio:
            x_mouse, y_mouse = pygame.mouse.get_pos()

            for linha in range(linhas):
                for coluna in range(colunas):
                    x = coluna * (largura_carta + espacamento) + espacamento
                    y = linha * (altura_carta + espacamento) + espacamento + offset_superior

                    if x <= x_mouse <= x + largura_carta and y <= y_mouse <= y + altura_carta:
                        carta = cartas[linha][coluna]

                        if not carta["revelada"] and len(cartas_viradas) < 2:
                            carta["revelada"] = True
                            cartas_viradas.append(carta)

                        # Se duas cartas foram viradas, aguarda um momento para mostrar a segunda
                        if len(cartas_viradas) == 2:
                            desenhar_jogo()  # Atualiza a tela para mostrar a segunda carta
                            pygame.time.delay(1000)  # Aguarda 1 segundo para visualizar

                            if cartas_viradas[0]["id"] != cartas_viradas[1]["id"]:
                                cartas_viradas[0]["revelada"] = False
                                cartas_viradas[1]["revelada"] = False
                                vidas -= 1  # Diminui vidas quando erro
                            else:
                                pares_encontrados += 1  # Aumenta acertos
                                vidas += 1  # Aumenta vidas quando acerto

                            cartas_viradas = []

    desenhar_jogo()

    # Verifica se o jogo acabou por vitória ou derrota
    if pares_encontrados == (linhas * colunas) // 2:
        mostrar_vitoria()
        rodando = False
    elif vidas <= 0:
        mostrar_derrota()
        rodando = False

pygame.quit()
