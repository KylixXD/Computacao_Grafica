import pygame
import sys
import math
from collections import deque

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Algoritmos de Preenchimento")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (150, 150, 150)
VERMELHO = (255, 0, 0)

# Configurações do grid
tamanho_celula = 10
linhas, colunas = altura // tamanho_celula, largura // tamanho_celula

# Estruturas de dados
modo = "poligono"
algoritmo_preenchimento = "flood_fill"  # Alterne entre "flood_fill" e "scanline"
pontos_poligono = []
pontos_borda = []
centro_circulo = None
raio_circulo = None
grid = [[BRANCO for _ in range(colunas)] for _ in range(linhas)]

# 📌 **Funções de Rasterização e Preenchimento**
def rasterizar_linha_bresenham(x0, y0, x1, y1):
    """Algoritmo de Bresenham para rasterização de linhas."""
    pontos = []
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx - dy
    while True:
        pontos.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return pontos

def rasterizar_circulo_bresenham(xc, yc, r):
    """Algoritmo de Bresenham para rasterização de circunferências."""
    pontos = []
    x, y = 0, r
    d = 3 - 2 * r
    while x <= y:
        pontos.extend([
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ])
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
    return pontos

def flood_fill(grid, x, y, target_color, new_color):
    """Preenchimento Flood Fill usando BFS."""
    if x < 0 or x >= colunas or y < 0 or y >= linhas or grid[y][x] != target_color or target_color == new_color:
        return
    queue = deque([(x, y)])
    while queue:
        cx, cy = queue.popleft()
        if 0 <= cx < colunas and 0 <= cy < linhas and grid[cy][cx] == target_color:
            grid[cy][cx] = new_color
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                queue.append((nx, ny))

def scanline_fill(grid, pontos_poligono):
    """Preenchimento por varredura (Scanline)."""
    min_y, max_y = min(p[1] for p in pontos_poligono), max(p[1] for p in pontos_poligono)
    for y in range(min_y, max_y + 1):
        intersecoes = []
        for i in range(len(pontos_poligono)):
            x0, y0 = pontos_poligono[i]
            x1, y1 = pontos_poligono[(i + 1) % len(pontos_poligono)]
            if y0 == y1:
                continue
            if (y0 <= y < y1) or (y1 <= y < y0):
                x_intersecao = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                intersecoes.append(int(round(x_intersecao)))
        intersecoes.sort()
        for i in range(0, len(intersecoes), 2):
            if i + 1 < len(intersecoes):
                for x in range(intersecoes[i], intersecoes[i + 1] + 1):
                    if 0 <= x < colunas and 0 <= y < linhas and grid[y][x] != PRETO:
                        grid[y][x] = VERMELHO

def desenhar_grid():
    """Desenha o grid."""
    for x in range(0, largura, tamanho_celula):
        pygame.draw.line(tela, CINZA, (x, 0), (x, altura))
    for y in range(0, altura, tamanho_celula):
        pygame.draw.line(tela, CINZA, (0, y), (largura, y))

def desenhar_pontos():
    """Desenha os pontos do grid."""
    for y in range(linhas):
        for x in range(colunas):
            if grid[y][x] != BRANCO:
                pygame.draw.rect(tela, grid[y][x], (x * tamanho_celula, y * tamanho_celula, tamanho_celula, tamanho_celula))


# 📌 **Escolha da Forma**
forma_selecionada = "forma_c"  # Altere para "retangulo", "triangulo", "hexagono", "circunferencia", "forma_a", "forma_c"

formas = {
    "zero": [(0,0)],
    "retangulo": [(-15, -10), (15, -10), (15, 10), (-15, 10)],
    "triangulo": [(0, -20), (20, 20), (-20, 20)],
    "hexagono": [(0, -20), (17, -10), (17, 10), (0, 20), (-17, 10), (-17, -10)],
    "forma_a": [(-20, -15), (5, -25), (30, -5), (26, 5), (-10, 10), (-5, -2)],
    "forma_c": [(-15, -15), (0, -15), (8, -8), (15, -15), (30, -15), (30, 0), (8, 13), (-15, 0)]
}


if forma_selecionada == "circunferencia":
    centro_circulo = (colunas // 2, linhas // 2)
    raio_circulo = 30
    pontos_borda = rasterizar_circulo_bresenham(*centro_circulo, raio_circulo)
else:
    pontos_poligono = [(x + colunas // 2, y + linhas // 2) for x, y in formas[forma_selecionada]]
    for i in range(len(pontos_poligono) - 1):
        pontos_borda += rasterizar_linha_bresenham(*pontos_poligono[i], *pontos_poligono[i + 1])
    pontos_borda += rasterizar_linha_bresenham(*pontos_poligono[-1], *pontos_poligono[0])

# Desenha bordas no grid
for x, y in pontos_borda:
    if 0 <= x < colunas and 0 <= y < linhas:
        grid[y][x] = PRETO

# 📌 **Preenchimento**
if forma_selecionada == "circunferencia":
    # Ponto de início para o Flood Fill dentro do círculo
    flood_fill(grid, centro_circulo[0], centro_circulo[1], BRANCO, VERMELHO)
elif forma_selecionada != "circunferencia":
    if algoritmo_preenchimento == "flood_fill":
        flood_fill(grid, colunas // 2, linhas // 2, BRANCO, VERMELHO)
    elif algoritmo_preenchimento == "scanline":
        scanline_fill(grid, pontos_poligono)


# 📌 **Loop principal**
rodando = True
while rodando:
    tela.fill(BRANCO)
    desenhar_grid()
    desenhar_pontos()
    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

pygame.quit()
sys.exit()
