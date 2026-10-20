import pygame, sys  
from pygame.locals import * 

pygame.init()  
clock = pygame.time.Clock()  
pygame.display.set_caption("game")  

WINDOW_SIZE = (600, 400)  
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300,200))

# Make sure "coocoo.png" is in the same folder as this script
player_image = pygame.image.load("coocoo.png")
player_image.set_colorkey((255, 255, 255))  # Set white as the transparent color

dirt_image = pygame.image.load("dirt.png")
grass_image = pygame.image.load("grass.png")

game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

def check_collision(rect, tiles):
    for tile in tiles:
        if rect.colliderect(tile):
            return True
    return False


def move(rect, movement, tiles):
    global player_y_momentum

    # Resolve horizontal and vertical movement separately so the player can
    # slide along platforms without passing through them.
    rect.x += movement[0]
    for tile in tiles:
        if rect.colliderect(tile):
            if movement[0] > 0:
                rect.right = tile.left
            elif movement[0] < 0:
                rect.left = tile.right

    rect.y += movement[1]
    for tile in tiles:
        if rect.colliderect(tile):
            if movement[1] > 0:
                rect.bottom = tile.top
            elif movement[1] < 0:
                rect.top = tile.bottom
            player_y_momentum = 0

    return rect


moving_right = False 
moving_left = False  

player_location = [50, 50]
player_y_momentum = 0

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())

while True:      
    # 1. Clear the screen with a background color
    display.fill((146, 244, 255))

    title_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '2':
                display.blit(grass_image, (x * 16, y * 16))
            if tile == '1':
                display.blit(dirt_image, (x * 16, y * 16))
            if tile != '0':
                tile_rect = pygame.Rect(x * 16, y * 16, 16, 16)
                title_rects.append(tile_rect)
            x += 1
        y += 1
        
   
    

    player_movement = [0,0]
    if moving_right:
        player_movement[0] += 2
    if moving_left: 
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect = move(player_rect, player_movement, title_rects)
    
    display.blit(player_image, (player_rect.x, player_rect.y))
                                                                    

    # 3. Draw game elements
    # FIXED: Replaced player_location with player_rect to keep drawing accurate to collisions


          
    # 4. Handle events
    for event in pygame.event.get():         
        if event.type == QUIT:             
            pygame.quit()            
            sys.exit()            
            
        if event.type == KEYDOWN:               
            if event.key == K_RIGHT:                   
                moving_right = True               
            if event.key == K_LEFT:                   
                moving_left = True            
            if event.key == K_UP:
                player_y_momentum = -5  # Adjust jump strength as needed    
        if event.type == KEYUP:               
            if event.key == K_RIGHT:                   
                moving_right = False               
            if event.key == K_LEFT:                   
                moving_left = False                           
                
    # 5. Update display and lock framerate
    surf = pygame.transform.scale(display, screen.get_size())
    screen.blit(surf, (0, 0))
    pygame.display.update()     
    clock.tick(60)
