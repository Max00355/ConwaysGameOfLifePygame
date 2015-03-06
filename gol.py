import pygame
import copy

class GOL:
    def __init__(self):
        self.liveCells = []
        self.lines = []
        self.deadCells = []
        self.res = (800, 600)
        self.cellSize = 10
        self.screen = pygame.display.set_mode(self.res)
        self.stepping = False
        self.cell = pygame.transform.scale(pygame.image.load("cell.png").convert(), (self.cellSize, self.cellSize)) 
    def game(self):
        self.createDeadCells()
        while True:
            self.screen.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    __import__("sys").exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for x in self.deadCells:
                        if x.collidepoint(pos):
                            self.deadCells.remove(x)
                            self.liveCells.append(x)
                            break
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.stepping = not self.stepping
                    elif event.key == pygame.K_r:
                        self.liveCells = []
                        self.createDeadCells()

            for x in self.liveCells:
                self.screen.blit(self.cell, (x.x, x.y))
            
            for l in self.lines:
                pygame.draw.line(self.screen, (200,200,200), l[0], l[1])

            if self.stepping:
                self.step() 
            pygame.display.update()
            pygame.time.wait(15) 
    
    def createDeadCells(self):
        y = 0
        while y <= self.res[1]:
            x = 0
            while x <= self.res[0]:
                self.deadCells.append(pygame.Rect(x, y, self.cellSize, self.cellSize))
                x += self.cellSize
                self.lines.append([(x, 0), (x, self.res[1])])
            self.lines.append([(0, y), (self.res[0], y)])

            y += self.cellSize

    def step(self):
        liveCells = copy.copy(self.liveCells)
        deadCells = copy.copy(self.deadCells)

        for cell in liveCells:
            neighbors = self.countNeighbors(cell, liveCells)
            if neighbors < 2 or neighbors > 3:
                self.liveCells.remove(cell)
                self.deadCells.append(cell)
        
        for cell in deadCells:
            neighbors = self.countNeighbors(cell, liveCells)
            if neighbors == 3:
                self.deadCells.remove(cell)
                self.liveCells.append(cell)

    def countNeighbors(self, on, liveCells):
        topleft = pygame.Rect(on.x - self.cellSize, on.y - self.cellSize, self.cellSize, self.cellSize)
        topright = pygame.Rect(on.x + self.cellSize, on.y - self.cellSize, self.cellSize, self.cellSize)
        bottomleft = pygame.Rect(on.x - self.cellSize, on.y + self.cellSize, self.cellSize, self.cellSize)
        bottomright = pygame.Rect(on.x + self.cellSize, on.y + self.cellSize, self.cellSize, self.cellSize)
        top = pygame.Rect(on.x, on.y - self.cellSize, self.cellSize, self.cellSize)
        left = pygame.Rect(on.x - self.cellSize, on.y, self.cellSize, self.cellSize)
        bottom = pygame.Rect(on.x, on.y + self.cellSize, self.cellSize, self.cellSize)
        right = pygame.Rect(on.x + self.cellSize, on.y, self.cellSize, self.cellSize)
        neighbors = 0
        if topleft.collidelist(liveCells) != -1:
            neighbors += 1
        if topright.collidelist(liveCells) != -1:
            neighbors += 1
        if top.collidelist(liveCells) != -1:
            neighbors += 1
        if bottomleft.collidelist(liveCells) != -1:
            neighbors += 1
        if bottomright.collidelist(liveCells) != -1:
            neighbors += 1
        if bottom.collidelist(liveCells) != -1:
            neighbors += 1
        if left.collidelist(liveCells) != -1:
            neighbors += 1
        if right.collidelist(liveCells) != -1:
            neighbors += 1

        return neighbors

if __name__ == "__main__":
    GOL().game()



