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

def divide_pontos_curva(pontos, profundidade_atual):
    """Realiza a subdivisão recursiva da curva de Bézier baseado na profundidade limitada entre 0 e 1."""
    if profundidade_atual <= 0:
        return pontos
    
    m01 = ponto_medio(pontos[0], pontos[1])
    m12 = ponto_medio(pontos[1], pontos[2])
    m23 = ponto_medio(pontos[2], pontos[3])

    m012 = ponto_medio(m01, m12)
    m123 = ponto_medio(m12, m23)
    ponto_medio_curva = ponto_medio(m012, m123)

    pontos_curva1 = [pontos[0], m01, m012, ponto_medio_curva]
    pontos_curva2 = [ponto_medio_curva, m123, m23, pontos[3]]

    pontos_curva1 = divide_pontos_curva(pontos_curva1, profundidade_atual - 0.1)
    pontos_curva2 = divide_pontos_curva(pontos_curva2, profundidade_atual - 0.1)

    return pontos_curva1 + pontos_curva2

def draw_curve_by_depth(screen, pontos_controle, profundidade, progress):
    """Desenha a curva de Bézier com animação baseada na profundidade."""
    profundidade = max(0, min(profundidade, 1))  # Limita profundidade entre 0 e 1
    if len(pontos_controle) == 4:
        pontos_curva = divide_pontos_curva(pontos_controle, profundidade)
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
    profundidade = 0.0  # Profundidade da subdivisão limitada entre 0 e 1
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
                    profundidade += 0.1  # Aumenta a profundidade da subdivisão (de 0 a 1)
                    profundidade = min(profundidade, 1)  # Garante que a profundidade não passe de 1
                    drawing = True
                    progress = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(control_points) == 4:
                    profundidade = 0  # Reseta a profundidade
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
