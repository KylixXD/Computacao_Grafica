import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da janela
largura, altura = 400, 400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Rasterização de Linhas")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Tamanho do grid (resolução reduzida)
tamanho_celula = 20
linhas = altura // tamanho_celula
colunas = largura // tamanho_celula



# Funções de rasterização
def rasterizar_linha_analitico(x0, y0, x1, y1):
    pontos = []
    dx = x1 - x0
    dy = y1 - y0
    if dx == 0:
        for y in range(min(y0, y1), max(y0, y1) + 1):
            pontos.append((x0, y))
    else:
        m = dy / dx
        b = y0 - m * x0
        for x in range(min(x0, x1), max(x0, x1) + 1):
            y = round(m * x + b)
            pontos.append((x, y))
    return pontos

def rasterizar_linha_dda(x0, y0, x1, y1):
    pontos = []
    dx = x1 - x0
    dy = y1 - y0
    passos = max(abs(dx), abs(dy))
    inc_x = dx / passos
    inc_y = dy / passos
    x, y = x0, y0
    for _ in range(passos + 1):
        pontos.append((round(x), round(y)))
        x += inc_x
        y += inc_y
    return pontos

def rasterizar_linha_bresenham(x0, y0, x1, y1):
    pontos = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    p = dx - dy
    while True:
        pontos.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * p
        if e2 > -dy:
            p -= dy
            x0 += sx
        if e2 < dx:
            p += dx
            y0 += sy
    
    return pontos



# Converte coordenadas para o grid reduzido
def para_grid(x, y):
    return x // tamanho_celula, y // tamanho_celula

# Desenha o grid na tela
def desenhar_grid():
    for x in range(0, largura, tamanho_celula):
        pygame.draw.line(tela, PRETO, (x, 0), (x, altura))
    for y in range(0, altura, tamanho_celula):
        pygame.draw.line(tela, PRETO, (0, y), (largura, y))

# Desenha os pontos no grid
def desenhar_pontos(pontos, cor):
    for x, y in pontos:
        pygame.draw.rect(tela, cor, (x * tamanho_celula, y * tamanho_celula, tamanho_celula, tamanho_celula))

# Coordenadas das linhas (descomente apenas uma coordenada)
#Linha Diagonal
# x0, y0 =  1, 1   
# x1, y1 = 15, 18  

# Linha com Inclinação de 45º
# x0, y0 = 3, 15
# x1, y1 = 15, 5

# Linha quase verticais 
x0, y0 = 10, 2
x1, y1 = 12, 18

# # Linha na Horizontal
# x0, y0 =  1, 10
# x1, y1 = 18, 10

#Linha na Vertical
# x0, y0 = 10, 2
# x1, y1 = 10, 18


# Rasterizar com o método desejado (descomente apenas uma função)
# pontos = rasterizar_linha_analitico(x0, y0, x1, y1)
# pontos = rasterizar_linha_dda(x0, y0, x1, y1)
pontos = rasterizar_linha_bresenham(x0, y0, x1, y1)

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Preenche a tela com branco
    tela.fill(BRANCO)

    # Desenha o grid
    desenhar_grid()

    # Desenha os pontos rasterizados
    desenhar_pontos(pontos, PRETO)

    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
sys.exit()
