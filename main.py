from cmath import sqrt
import random
import pygame, sys


WIDTH, HEIGHT = 900, 500
BORDER = 10
BOX = pygame.Rect(BORDER, BORDER, WIDTH - 2 * BORDER, HEIGHT - 2 * BORDER)
# telling pygame to make a new window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Physics Simulator")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)

FPS = 60
DELTA_TIME = 1 / FPS
GRAVITY = 200
ENERGY_CONSERVED = .75 # percent

particles = []

def main():
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(100)
        
        
        WIN.fill(RED)
        pygame.draw.rect(WIN, BLACK, BOX)
        
        for particle in particles:
            update(particle)
        
        for event in pygame.event.get():
            # Checking if quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                print("Physics Simulator has been quit!")
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                p = Particle(pos,50)
                particles.append(p)

        pygame.display.update()
    
def update(particle):
    
    particle.force = [0,0]
    
    check_wall_collision(particle)
    check_collisions(particle)  
    
    particle.velocity[0] = particle.velocity[0] + particle.force[0] * DELTA_TIME / particle.mass
    particle.velocity[1] = particle.velocity[1] + particle.force[1] * DELTA_TIME / particle.mass
    
    particle.position[0] = particle.position[0] + particle.velocity[0] * DELTA_TIME 
    particle.position[1] = particle.position[1] + particle.velocity[1] * DELTA_TIME
    
    #print(particle.position)
    particle.update_cords()
    particle.draw()

def check_collisions(particle):
    
    for point in particles:
        if(point != particle):
            particle.check_if_collides(point)
    
    
    pass


def check_wall_collision(particle):
    collision = False
    # top
    if(particle.top <= BOX.top):
        particle.velocity[1] = abs(particle.velocity[1])
        particle.force[1] += -particle.force[1]
        collision = True
        
    # bottom
    if(particle.bottom >= BOX.bottom):
        particle.velocity[1] = -1 * abs(particle.velocity[1])
        particle.force[1] += -particle.force[1]
        collision = True
        
    # left
    if(particle.left <= BOX.left):
        particle.velocity[0] = abs(particle.velocity[0])
        particle.force[0] += -particle.force[0]
        collision = True
    
    # right
    if(particle.right >= BOX.right):
        particle.velocity[0] = -1 * abs(particle.velocity[0])
        particle.force[0] += -particle.force[0]
        collision = True
        

class Particle:
    
    def __init__(self, position, radius, mass=1):
        self.position = list(position)
        self.velocity = [random.randint(-750,750),random.randint(-750,750)]
        self.force = [0,0]
        self.mass = mass
        self.radius = radius
        self.top = position[1] - radius
        self.bottom = position[1] + radius
        self.left = position[0] - radius
        self.right = position[0] + radius
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def update_cords(self):
        self.top = self.position[1] - self.radius
        self.bottom = self.position[1] + self.radius
        self.left = self.position[0] - self.radius
        self.right = self.position[0] + self.radius
        
    def draw(self):
        pygame.draw.circle(WIN, self.color, self.position, self.radius)

    def change_color(self):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def check_if_collides(self, particle):
        x1 = self.position[0]
        x2 = particle.position[0]
        y1 = self.position[1]
        y2 = particle.position[1]
        collides = (abs(sqrt( (x2 - x1) ** 2 +  (y2 - y1) ** 2))) <= (self.radius + particle.radius)
        if(collides):
            self.change_color()
            particle.change_color()
        
        
        
        
        
if __name__ == "__main__":
    main()