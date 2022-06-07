from tabnanny import check
from turtle import update
import pygame, sys


WIDTH, HEIGHT = 900, 500
FLOOR = HEIGHT - 10
# telling pygame to make a new window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Physics Simulator")

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAVITY = 9.8

blocks = pygame.sprite.Group()

def main():
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        
        WIN.fill(BLACK)
        pygame.draw.rect(WIN, WHITE, pygame.Rect(0,FLOOR, WIDTH, 10))
        
        blocks.update()
        
        
        for event in pygame.event.get():
            # Checking if quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                print("Physics Simulator has been quit!")
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                blocks.add(Square(pos[0],pos[1]))

        pygame.display.update()
    
    
    

class Square(pygame.sprite.Sprite):
    
    velocity = 0
    force = 0
    
    def __init__(self, x, y, height=50, width=50, mass=10):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.mass = mass
        self.rect = pygame.Rect(self.x, self.y, self.height, self.width)
        self.draw()
    
    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
    
    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.rect)
        
    def update(self):
        self.force = 0
        self.force = GRAVITY * self.mass
        # Euler integration
        self.velocity += self.force * 1 / self.mass
        self.y += self.velocity * 1 
        
        
        self.checkFloorCollision()
        self.rect = pygame.Rect(self.x, self.y, self.height, self.width)
        self.draw()
    
    def checkFloorCollision(self): 
        if(self.velocity != 0 and self.y + self.height >= FLOOR):
            self.y = FLOOR - self.height
            self.velocity = -1 * self.velocity
            #print(self.velocity)
            self.update()

    def collided_with_another_rect(self, rect):
        """ Assumes rectangles are same size or that this rectangle is smaller than the other rectangle"""
        if self.x > (rect.x + rect.width):
            # Is to the right of the other rectangle
            return False
        elif (self.x + self.width) < rect.x:
            # is to the left of the other rectangle
            return False
        elif (self.y + self.height) < rect.y:
            # is above the other rectangle
            return False
        elif self.y > (rect.y + rect.height):
            # is below the other rectangle
            return False
        else:
            return True

    
    


    
if __name__ == "__main__":
    main()