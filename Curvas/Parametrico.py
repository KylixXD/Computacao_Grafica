import numpy as np
import pygame

# Configuração do pygame
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
CURVE_COLOR = (255, 0, 0)
CONTROL_COLOR = (0, 0, 255)
LINE_COLOR = (100, 100, 100)
FPS = 60
pygame.display.set_caption("Bezier Parametrico")

def bernstein_poly(i, n, t):
    """Calcula o polinômio de Bernstein para a curva de Bézier"""
    from scipy.special import comb
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

def bezier_generalized(t, control_points):
    """Calcula um ponto na curva de Bézier para um valor de t."""
    n = len(control_points) - 1
    point = np.zeros(2)
    for i in range(n + 1):
        point += bernstein_poly(i, n, t) * control_points[i]
    return point

def bezier_curve_parametric(control_points, num_points=100):
    """Gera os pontos da curva de Bézier usando a equação paramétrica."""
    t_values = np.linspace(0, 1, num_points)
    return [bezier_generalized(t, control_points) for t in t_values]

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    control_points = []
    curve = []
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
                elif event.button == 3 and len(control_points) > 1:  # Botão direito do mouse
                    drawing = True  # Inicia a animação da curva
                    progress = 0
        
        if drawing and len(control_points) > 1:
            progress += 0.01
            if progress > 1:
                progress = 1
            curve = bezier_curve_parametric(control_points, 100)
        
        if len(control_points) > 1:
            draw_control_polygon(screen, control_points)
        if drawing:
            draw_curve(screen, curve, progress)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
