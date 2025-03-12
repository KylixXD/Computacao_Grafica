import numpy as np
import pygame

# Configuração do pygame
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
CURVE_COLOR = (255, 0, 0)
CONTROL_COLOR = (0, 0, 255)
MIDPOINT_COLOR = (0, 255, 0)
LINE_COLOR = (100, 100, 100)
FPS = 60
pygame.display.set_caption("Bezier Casteljau")

def ponto_medio(p1, p2):
    """Calcula o ponto médio entre dois pontos."""
    return (p1 + p2) / 2

def casteljau(P0, P1, P2, P3, t, pontos=[]):
    """Recursão do algoritmo de Casteljau baseado na subdivisão da curva."""
    M01 = ponto_medio(P0, P1)
    M12 = ponto_medio(P1, P2)
    M23 = ponto_medio(P2, P3)
    
    M012 = ponto_medio(M01, M12)
    M123 = ponto_medio(M12, M23)
    
    M0123 = ponto_medio(M012, M123)
    
    if t > 0.005:
        t /= 2
        casteljau(P0, M01, M012, M0123, t, pontos)
        pontos.append(M0123)
        casteljau(M0123, M123, M23, P3, t, pontos)
    else:
        pontos.append(P0)
        pontos.append(P3)
    
    return pontos

def draw_curve_by_depth(screen, pontos_controle, profundidade, progress):
    """Desenha a curva de Bézier com animação baseada na profundidade."""
    profundidade = max(0, min(profundidade, 1))  # Limita profundidade entre 0 e 1
    if len(pontos_controle) == 4:
        pontos_curva = casteljau(pontos_controle[0], pontos_controle[1], pontos_controle[2], pontos_controle[3], profundidade, [])
        num_points = int(len(pontos_curva) * progress)
        if num_points > 1:
            pygame.draw.lines(screen, CURVE_COLOR, False, pontos_curva[:num_points], 2)

def draw_control_polygon(screen, control_points):
    """Desenha os pontos de controle e suas conexões."""
    for i in range(len(control_points) - 1):
        pygame.draw.line(screen, LINE_COLOR, control_points[i], control_points[i + 1], 1)
    for point in control_points:
        pygame.draw.circle(screen, CONTROL_COLOR, (int(point[0]), int(point[1])), 5)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    control_points = []
    profundidade = 0.1  # Profundidade inicial
    drawing = False
    progress = 0  # Progresso da animação
    
    while running:
        screen.fill(BACKGROUND_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    control_points.append(np.array(event.pos, dtype=float))
                    drawing = False
                    progress = 0
                elif event.button == 3 and len(control_points) == 4:  # Botão direito do mouse
                    profundidade = min(profundidade + 0.1, 1)  # Aumenta a profundidade da subdivisão
                    drawing = True
                    progress = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(control_points) == 4:
                    profundidade = 0.1  # Reseta a profundidade
                    drawing = False
                    progress = 0
        
        if len(control_points) > 1:
            draw_control_polygon(screen, control_points)
        if len(control_points) == 4 and drawing:
            progress += 0.02
            if progress > 1:
                progress = 1
            draw_curve_by_depth(screen, control_points, profundidade, progress)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
