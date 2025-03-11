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

def casteljau_recursive(points, t):
    """Algoritmo de De Casteljau de forma recursiva para calcular um ponto na curva de Bézier."""
    if len(points) == 1:
        return np.array(points[0])
    new_points = [np.array((1 - t) * np.array(points[i]) + t * np.array(points[i + 1])) for i in range(len(points) - 1)]
    return casteljau_recursive(new_points, t)

def bezier_curve_casteljau(control_points, num_points=100):
    """Gera os pontos da curva de Bézier usando o algoritmo de Casteljau."""
    t_values = np.linspace(0, 1, num_points)
    return [casteljau_recursive(control_points, t) for t in t_values]

def subdivide_casteljau(P):
    """Realiza a subdivisão da curva de Bézier usando o algoritmo de De Casteljau."""
    M01 = (P[0] + P[1]) / 2
    M12 = (P[1] + P[2]) / 2
    M23 = (P[2] + P[3]) / 2

    M012 = (M01 + M12) / 2
    M123 = (M12 + M23) / 2

    M0123 = (M012 + M123) / 2

    left_curve = [P[0], M01, M012, M0123]
    right_curve = [M0123, M123, M23, P[3]]

    return left_curve, right_curve, M0123

def draw_curve(screen, curve_points, progress):
    """Desenha a curva de Bézier na tela com animação suave."""
    num_points = int(len(curve_points) * progress)
    for i in range(num_points - 1):
        pygame.draw.line(screen, CURVE_COLOR, curve_points[i], curve_points[i + 1], 2)

def draw_control_polygon(screen, control_points):
    """Desenha os pontos de controle e suas conexões."""
    for i in range(len(control_points) - 1):
        pygame.draw.line(screen, LINE_COLOR, control_points[i], control_points[i + 1], 1)
    for point in control_points:
        pygame.draw.circle(screen, CONTROL_COLOR, (int(point[0]), int(point[1])), 5)

def draw_subdivision(screen, P):
    """Desenha as subdivisões da curva Bézier."""
    left, right, midpoint = subdivide_casteljau(P)

    pygame.draw.circle(screen, MIDPOINT_COLOR, (int(midpoint[0]), int(midpoint[1])), 5)
    pygame.draw.lines(screen, CURVE_COLOR, False, left, 2)
    pygame.draw.lines(screen, CURVE_COLOR, False, right, 2)

    return left, right

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
