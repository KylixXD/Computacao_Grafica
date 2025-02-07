import pygame
import sys
import math

# Inicialização do Pygame
pygame.init()

# Configurações da janela
largura, altura = 800, 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Rasterização de Circunferências")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Tamanho do grid 
tamanho_celula = 20
linhas = altura // tamanho_celula
colunas = largura // tamanho_celula

def rasterizar_circulo_parametrico(xc, yc, r):
    pontos = []
    for angulo in range(0, 360):
        rad = math.radians(angulo)
        x = round(xc + r * math.cos(rad))
        y = round(yc + r * math.sin(rad))
        pontos.append((x, y))
    return pontos

def rasterizar_circulo_incremental(xc, yc, r):
    pontos = []

    x = r
    y = 0
    theta = 1 / r  # Incremento angular
    C = math.cos(theta)
    S = math.sin(theta)

    while y < x:
        # Adiciona os 8 pontos simétricos
        pontos.extend([
            (round(xc + x), round(yc + y)), (round(xc - x), round(yc + y)),
            (round(xc + x), round(yc - y)), (round(xc - x), round(yc - y)),
            (round(xc + y), round(yc + x)), (round(xc - y), round(yc + x)),
            (round(xc + y), round(yc - x)), (round(xc - y), round(yc - x))
        ])

        # Atualiza os valores de x e y usando a fórmula incremental
        xt = x 
        x = x * C - y * S
        y = y * C + xt * S

    return pontos


def rasterizar_circulo_bresenham(xc, yc, r):
    pontos = []
    x = 0
    y = r
    d = 3 - 2 * r
    while x <= y:
        pontos.extend([  # Adiciona os 8 simétricos
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ])
        if d < 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1
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

# Coordenadas do centro e raio da circunferência
xc, yc = 20, 20  # Centro da circunferência no grid
# r = 6 # Raio da circunferência no grid 6

r = 18

# Rasterizar com o método desejado 
# pontos = rasterizar_circulo_parametrico(xc, yc, r)
pontos = rasterizar_circulo_incremental(xc, yc, r)
# pontos = rasterizar_circulo_bresenham(xc, yc, r)

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
