from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid
import sys
import pygame
import random


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

class GridVisualizer:
    width = 10
    height = 10
    width_block_size = int(WINDOW_WIDTH / width)
    height_block_size = int(WINDOW_HEIGHT / height)
    
    def __init__(self) -> None:
        self.grid = []
        self.start = None
        self.end = None
        self.path = None
        
        for i in range((self.width)):
            self.grid.append([])
            for _ in range(self.height):
                self.grid[i].append(1)
            
        self.start = self.get_random_node() # Start Node
        self.end = self.get_random_node() # End Node


    def get_random_node(self) -> tuple:
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        if self.grid[x][y] == 0:
            self.get_random_node()
            
        return (x, y)
    
    def draw(self):
        for x in range(0, WINDOW_WIDTH, self.width_block_size):
            for y in range(0, WINDOW_HEIGHT, self.height_block_size):
                # Draw the grid
                border = pygame.Rect(x, y, self.width_block_size, self.height_block_size)
                pygame.draw.rect(SCREEN, BLACK, border, 1)
                
                block = pygame.Rect(x + 1, y + 1, self.width_block_size - 2, self.height_block_size - 2)
                if self.grid[int(x / self.width_block_size)][int(y / self.height_block_size)] == 0:
                    pygame.draw.rect(SCREEN, BLACK, block, 0)
                
        self.draw_start_and_end()
        
    def draw_start_and_end(self):
        pygame.draw.rect(SCREEN, RED, (self.start[0] * self.width_block_size + 1, self.start[1] * self.height_block_size + 1, self.width_block_size - 2, self.height_block_size - 2), 0)            
        pygame.draw.rect(SCREEN, BLUE, (self.end[0] * self.width_block_size + 1, self.end[1] * self.height_block_size + 1, self.width_block_size - 2, self.height_block_size - 2), 0)
        
        
    def draw_path(self):
        self.width_block_size = int(WINDOW_WIDTH / self.width)
        self.height_block_size = int(WINDOW_HEIGHT / self.height)
        for node in self.path:
            pygame.draw.rect(SCREEN, GREEN, (node[0] * self.width_block_size + 1, node[1] * self.height_block_size + 1, self.width_block_size - 2, self.height_block_size - 2), 0)
        self.draw_start_and_end()
        
    def find_path(self):
        grid = Grid(matrix=self.grid)
        start = grid.node(*self.start)
        end = grid.node(*self.end)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, grid)
        print('operations:', runs, 'path length:', len(path))
        print(grid.grid_str(path=path, start=start, end=end))
        self.path = path
        self.draw_path()

def main():
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(WHITE)

    game_grid = GridVisualizer()
    game_grid.draw()
    game_grid.find_path()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:                        
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    SCREEN.fill(WHITE)
                    game_grid = GridVisualizer()
                    game_grid.draw()
                    game_grid.find_path()
            

        pygame.display.update()


            
if __name__ == '__main__':
    main()