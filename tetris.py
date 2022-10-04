# ADJUST MOVEMENT OF FALLING BLOCK
import pygame
import random
from os import path

CELL = 30

WIDTH = 10 * CELL
HEIGHT = 20 * CELL
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()


img_dir = path.join(path.dirname(__file__), 'assets')

blocks = []

for i in range(0, 7):
    blocks.append(pygame.image.load(path.join(img_dir, "block" + str(i) + ".png")).convert())

sprite1 = pygame.sprite.Sprite()
sprite1.image = pygame.Surface((75, 75))
sprite1.image.fill((255, 0, 0))
sprite1.rect = sprite1.image.get_rect()

class Blockbit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(path.join(img_dir, "square1.png")).convert()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect.centerx = x
        self.rect.bottom = y
        
        self.speedx = 0
        self.speedy = CELL

        self.is_moving = True

        self.fall_frame = 0

        self.move_marker = 0
        self.move_divider = 4
        self.move_previous_key = 0

        self.rotate_marker = 0
        self.rotate_divider = 10
        self.rotate_previous_key = 0

    def update(self):

        if self.is_moving:
            
            if self.fall_frame == 60:
                self.fall_frame = 0
                self.rect.y += self.speedy
            
            else:
                self.fall_frame += 1
                

            keystate = pygame.key.get_pressed()

            if keystate[pygame.K_a]:
                if self.rotate_previous_key != pygame.K_a:
                    self.rotate_previous_key = pygame.K_a

                    self.image = pygame.transform.rotate(self.image, -90)
                    self.mask = pygame.mask.from_surface(self.image)

                    self.marker= self.fall_frame % self.rotate_divider
                else:
                    v = self.fall_frame % self.rotate_divider
                    if v == self.rotate_marker:
                        self.image = pygame.transform.rotate(self.image, -90)
                        self.mask = pygame.mask.from_surface(self.image)

            if keystate[pygame.K_LEFT]:
                if self.move_previous_key != pygame.K_LEFT:
                    self.move_previous_key = pygame.K_LEFT
                    self.speedx = -CELL
                    self.rect.x += self.speedx
                    self.move_marker = self.fall_frame % self.move_divider
                else:
                    v = self.fall_frame % self.move_divider
                    if v == self.move_marker:
                        self.speedx = -CELL
                        self.rect.x += self.speedx

            elif keystate[pygame.K_RIGHT]:
                if self.move_previous_key != pygame.K_RIGHT:
                    self.move_previous_key = pygame.K_RIGHT
                    self.speedx = CELL
                    self.rect.x += self.speedx
                    self.move_marker = self.fall_frame % self.move_divider
                else:
                    v = self.fall_frame % self.move_divider
                    if v == self.move_marker:
                        self.speedx = CELL
                        self.rect.x += self.speedx
            
            elif keystate[pygame.K_DOWN]:
                if self.move_previous_key != pygame.K_DOWN:
                    self.move_previous_key = pygame.K_DOWN
                    self.speedy = CELL
                    self.rect.y += self.speedy      
                    self.move_marker = self.fall_frame % self.move_divider
                else:
                    v = self.fall_frame % self.move_divider
                    if v == self.move_marker:
                        self.speedy = CELL
                        self.rect.y += self.speedy    
                
            else:
                self.previous_key = 0
        
        
        
class Borders(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, CELL))
        self.image.fill(WHITE)
    
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT

all_sprites = pygame.sprite.Group()
inactive_collision = pygame.sprite.Group()
#current_active_block = Blockbit(WIDTH / 2, 0)

active_blocks = pygame.sprite.Group()

def spawn():
    active_blocks.add(Blockbit(15+30, 0))
    active_blocks.add(Blockbit(15+0, 30))
    active_blocks.add(Blockbit(15+30, 30))
    active_blocks.add(Blockbit(15+60, 30))


border = Borders()

spawn()
all_sprites.add(border)
all_sprites.add(active_blocks)


test = pygame.sprite.Group()
#test.add(sprite1)
inactive_collision.add(border)



# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # Update
    
    block_previous_pos_y = []
    block_previous_pos_x = []
    for block in active_blocks:
        block_previous_pos_y.append(block.rect.y)
        block_previous_pos_x.append(block.rect.x)

    all_sprites.update()

    collision = pygame.sprite.groupcollide(active_blocks, inactive_collision, False, False)

    if collision: 
        #print(collision)
        i = 0
        for block in active_blocks:

            block.rect.x = block_previous_pos_x[i]
            block.rect.y = block_previous_pos_y[i]

            #if block in collision:
            #    if not block.rect.top >= collision[block][0].rect.bottom or block.rect.bottom <= collision[block][0].rect.top: 
                    
            i += 1

            active_blocks.remove(block)
            inactive_collision.add(block)
            block.is_moving = False

        spawn()
        all_sprites.add(active_blocks)
        
    
    sprite1.rect.center = pygame.mouse.get_pos()
    collide = pygame.sprite.spritecollide(sprite1, all_sprites, False)

    if collide:
        sprite1.image.fill((255, 255, 0))
    else:
        sprite1.image.fill((255, 0, 0))

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    test.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()