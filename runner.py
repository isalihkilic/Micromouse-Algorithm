import pygame

from labyrinth import Labyrinth
from micromouse import Micromouse

maze = Labyrinth()
mouse = Micromouse()

cell_size = 15

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font('freesansbold.ttf', 12)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.floodfill_openmaze()
            mouse.floodfill_closedmaze()
            mouse.move_to_best()
            left, forward, right = maze.get_sensor_data(mouse.current_position, mouse.heading)
            done = mouse.add_observation(left, forward, right)
    screen.fill("white")
    true_maze = pygame.Surface((301, 361))
    true_maze.fill("white")
    for row, cells in enumerate(maze.cells):
        for col, cell in enumerate(cells):
            if cell & 1 > 0:
                pygame.draw.line(true_maze, pygame.Color(0, 0, 0), (col * cell_size, row * cell_size), (col * cell_size + cell_size, row * cell_size))
            if cell & 2 > 0:
                pygame.draw.line(true_maze, pygame.Color(0, 0, 0), (col * cell_size + cell_size, row * cell_size), (col * cell_size + cell_size, row * cell_size + cell_size))
            if cell & 4 > 0:
                pygame.draw.line(true_maze, pygame.Color(0, 0, 0), (col * cell_size, row * cell_size + cell_size), (col * cell_size + cell_size, row * cell_size + cell_size))
            if cell & 8 > 0:
                pygame.draw.line(true_maze, pygame.Color(0, 0, 0), (col * cell_size, row * cell_size), (col * cell_size, row * cell_size + cell_size))

    open_maze = pygame.Surface((301, 361))
    open_maze.fill("white")
    for row, cells in enumerate(mouse.cells):
        for col, cell in enumerate(cells):
            if cell & 1 > 0:
                pygame.draw.line(open_maze, pygame.Color(0, 0, 0), (col * cell_size, row * cell_size), (col * cell_size + cell_size, row * cell_size))
            if cell & 2 > 0:
                pygame.draw.line(open_maze, pygame.Color(0, 0, 0), (col * cell_size + cell_size, row * cell_size), (col * cell_size + cell_size, row * cell_size + cell_size))
            if cell & 4 > 0:
                pygame.draw.line(open_maze, pygame.Color(0, 0, 0), (col * cell_size, row * cell_size + cell_size), (col * cell_size + cell_size, row * cell_size + cell_size))
            if cell & 8 > 0:
                pygame.draw.line(open_maze, pygame.Color(0, 0, 0), (col * cell_size, row * cell_size), (col * cell_size, row * cell_size + cell_size))
    for row, cells in enumerate(mouse.floodmaze):
        for col, cell in enumerate(cells):
            text = font.render(str(cell), True, pygame.Color(0, 0, 0))
            textRect = text.get_rect()
            textRect.center = ((col + 0.5) * cell_size, (row + 0.5) * cell_size)
            open_maze.blit(text, textRect)
    closed_maze = pygame.Surface((301, 361))
    closed_maze.fill("white")
    for row, cells in enumerate(mouse.cells):
        for col, cell in enumerate(cells):
            if cell & 16 > 0:
                pygame.draw.line(closed_maze, pygame.Color(0, 0, 0), (col * cell_size, row * cell_size), (col * cell_size + cell_size, row * cell_size))
            if cell & 32 > 0:
                pygame.draw.line(closed_maze, pygame.Color(0, 0, 0), (col * cell_size + cell_size, row * cell_size), (col * cell_size + cell_size, row * cell_size + cell_size))
            if cell & 64 > 0:
                pygame.draw.line(closed_maze, pygame.Color(0, 0, 0), (col * cell_size, row * cell_size + cell_size), (col * cell_size + cell_size, row * cell_size + cell_size))
            if cell & 128 > 0:
                pygame.draw.line(closed_maze, pygame.Color(0, 0, 0), (col * cell_size, row * cell_size), (col * cell_size, row * cell_size + cell_size))
    for row, cells in enumerate(mouse.floodclosedmaze):
        for col, cell in enumerate(cells):
            text = font.render(str(cell), True, pygame.Color(0, 0, 0))
            textRect = text.get_rect()
            textRect.center = ((col + 0.5) * cell_size, (row + 0.5) * cell_size)
            closed_maze.blit(text, textRect)
    pygame.draw.circle(true_maze, pygame.Color(255, 0, 0), ((mouse.current_position[1] + 0.5) * cell_size, (mouse.current_position[0] + 0.5) * cell_size), cell_size / 2)
    pygame.draw.circle(open_maze, pygame.Color(255, 0, 0), ((mouse.current_position[1] + 0.5) * cell_size, (mouse.current_position[0] + 0.5) * cell_size), cell_size / 2)
    pygame.draw.circle(closed_maze, pygame.Color(255, 0, 0), ((mouse.current_position[1] + 0.5) * cell_size, (mouse.current_position[0] + 0.5) * cell_size), cell_size / 2)
    if mouse.found_shortest:
        for i in range(len(mouse.shortest_path) - 1):
            pygame.draw.line(closed_maze, pygame.Color(0, 255, 0), ((mouse.shortest_path[i][1] + 0.5) * cell_size, (mouse.shortest_path[i][0] + 0.5) * cell_size), ((mouse.shortest_path[i + 1][1] + 0.5) * cell_size, (mouse.shortest_path[i + 1][0] + 0.5) * cell_size), 3)
            pygame.draw.line(open_maze, pygame.Color(0, 255, 0), ((mouse.shortest_path[i][1] + 0.5) * cell_size, (mouse.shortest_path[i][0] + 0.5) * cell_size), ((mouse.shortest_path[i + 1][1] + 0.5) * cell_size, (mouse.shortest_path[i + 1][0] + 0.5) * cell_size), 3)
            pygame.draw.line(true_maze, pygame.Color(0, 255, 0), ((mouse.shortest_path[i][1] + 0.5) * cell_size, (mouse.shortest_path[i][0] + 0.5) * cell_size), ((mouse.shortest_path[i + 1][1] + 0.5) * cell_size, (mouse.shortest_path[i + 1][0] + 0.5) * cell_size), 3)
    screen.blit(true_maze, (20, 20))
    screen.blit(open_maze, (340, 20))
    screen.blit(closed_maze, (660, 20))
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()