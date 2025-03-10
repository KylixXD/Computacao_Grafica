import pygame
from pygame.locals import *

# Algoritmo de Recorte de Polígonos de Sutherland-Hodgman
def sutherland_hodgman_clip(polygon, clip_rect):
    def inside(p, edge):
        x, y = p
        x_min, y_min, x_max, y_max = clip_rect
        if edge == 'left':
            return x >= x_min
        elif edge == 'right':
            return x <= x_max
        elif edge == 'bottom':
            return y >= y_min
        elif edge == 'top':
            return y <= y_max

    def compute_intersection(p1, p2, edge):
        x1, y1 = p1
        x2, y2 = p2
        x_min, y_min, x_max, y_max = clip_rect
        
        if edge == 'left':
            x = x_min
            y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
        elif edge == 'right':
            x = x_max
            y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
        elif edge == 'bottom':
            y = y_min
            x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
        elif edge == 'top':
            y = y_max
            x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
        
        return (round(x), round(y))
    
    edges = ['left', 'right', 'bottom', 'top']
    clipped_polygon = polygon[:]
    
    for edge in edges:
        new_polygon = []
        prev_point = clipped_polygon[-1]  # Começamos com o último vértice
        
        for point in clipped_polygon:
            if inside(point, edge):  # Se o ponto atual está dentro
                if not inside(prev_point, edge): # Mas o anterior estava fora
                    new_polygon.append(compute_intersection(prev_point, point, edge))
                new_polygon.append(point) # Mantemos o ponto
            elif inside(prev_point, edge): # Se o ponto anterior estava dentro, mas este não
                new_polygon.append(compute_intersection(prev_point, point, edge))
            
            prev_point = point # Atualiza o ponto anterior para o próximo laço
        
        clipped_polygon = new_polygon
    
    return clipped_polygon

# Configuração do pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recorte de Polígono - Sutherland Hodgman")
clock = pygame.time.Clock()

# Polígonos ajustados conforme os exemplos das imagens
triangulo = [(310, 102), (314, 270), (577, 265)]
hexagono = [(232, 105), (366, 185), (310, 306), (139, 297), (111, 159)]
cruz = [(310, 320), (420, 320), (420, 360), (460, 360), (460, 440), (420, 440), (420, 480),
        (310, 480), (310, 440), (270, 440), (270, 360), (310, 360)]
u_bugado = [(250, 100), (250, 210), (290, 210), (290, 140), (370, 140), (370, 200), (410, 200), (410, 100)]

# Escolha do polígono descomentando um deles
# polygon = triangulo
# polygon = hexagono
# polygon = cruz
polygon = u_bugado

# Retângulo de recorte (x_min, y_min, x_max, y_max)
clip_rect = (200, 150, 500, 400)

clipped_once = False
running = True
while running:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    clipped_polygon = sutherland_hodgman_clip(polygon, clip_rect)
    
    # Printar as coordenadas do polígono após o recorte apenas uma vez, sem casas decimais
    if not clipped_once:
        print("Coordenadas após o recorte:", [(round(x), round(y)) for x, y in clipped_polygon])
        clipped_once = True
    
    # Desenhar o polígono original
    pygame.draw.polygon(screen, (0, 255, 0), polygon, 1)
    
    # Desenhar o retângulo de recorte
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(clip_rect[0], clip_rect[1], 
                                                      clip_rect[2] - clip_rect[0], clip_rect[3] - clip_rect[1]), 1)
    
    # Desenhar o polígono recortado
    if len(clipped_polygon) > 2:
        pygame.draw.polygon(screen, (0, 0, 255), clipped_polygon, 0)
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()