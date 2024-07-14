import pygame
import sys
import pytmx
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flufftopia")

# Load spritesheet
spritesheet = pygame.image.load("assets/Player/character.png").convert_alpha()

# Update frame parameters
frame_width = 64
frame_height = 64
num_frames = 9
scale_factor = 2

# Function to extract frames from the spritesheet and scale them
def get_frames(sheet, frame_width, frame_height, num_frames, scale_factor, start_x, start_y):
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(start_x + i * frame_width, start_y, frame_width, frame_height))
        scaled_frame = pygame.transform.scale(frame, (int(frame_width * scale_factor), int(frame_height * scale_factor)))
        frames.append(scaled_frame)
    return frames

# Player frames dictionary
player_frames = {
    'walking': {
        'left': get_frames(spritesheet, frame_width, frame_height, num_frames, scale_factor, 0, 64),
        'right': get_frames(spritesheet, frame_width, frame_height, num_frames, scale_factor, 0, 192),
        'up': get_frames(spritesheet, frame_width, frame_height, num_frames, scale_factor, 0, 0),
        'down': get_frames(spritesheet, frame_width, frame_height, num_frames, scale_factor, 0, 128),
    },
    'idle': {
        'left': get_frames(spritesheet, frame_width, frame_height, num_frames, scale_factor, 0, 64),
        'right': get_frames(spritesheet, frame_width, frame_height, num_frames, scale_factor, 0, 192),
        'up': get_frames(spritesheet, frame_width, frame_height, num_frames, scale_factor, 0, 0),
        'down': get_frames(spritesheet, frame_width, frame_height, num_frames, scale_factor, 0, 192),
    },
}

# Define player properties
player_x = screen_width // 2
player_y = screen_height // 2
player_animation = 'idle'
player_direction = 'down'
player_frame = 0
player_speed = 5
player_health = 100
player_max_health = 100
player_attack_damage = 10
player_score = 0
active_quest = None

# Load tiled map
tmx_data = pytmx.load_pygame("assets/Map/map.tmx")
map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight

# Function to draw the map
def draw_map():
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))



# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player position based on input keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        new_x = player_x - player_speed
        new_rect = pygame.Rect(new_x, player_y, frame_width * scale_factor, frame_height * scale_factor)
        if new_x > 0:
            player_x = new_x
            player_animation = 'walking'
            player_direction = 'left'
    elif keys[pygame.K_RIGHT]:
        new_x = player_x + player_speed
        new_rect = pygame.Rect(new_x, player_y, frame_width * scale_factor, frame_height * scale_factor)
        if new_x < screen_width - frame_width * scale_factor:
            player_x = new_x
            player_animation = 'walking'
            player_direction = 'right'
    elif keys[pygame.K_UP]:
        new_y = player_y - player_speed
        new_rect = pygame.Rect(player_x, new_y, frame_width * scale_factor, frame_height * scale_factor)
        if new_y > 0:
            player_y = new_y
            player_animation = 'walking'
            player_direction = 'up'
    elif keys[pygame.K_DOWN]:
        new_y = player_y + player_speed
        new_rect = pygame.Rect(player_x, new_y, frame_width * scale_factor, frame_height * scale_factor)
        if new_y < screen_height - frame_height * scale_factor:
            player_y = new_y
            player_animation = 'walking'
            player_direction = 'down'
    else:
        player_animation = 'idle'

    # Update player frame
    if player_animation == 'walking':
        player_frame = (player_frame + 1) % num_frames
    else:
        player_frame = 0

    
    # Draw the map
    screen.fill((0, 0, 0))  # Clear the screen with black before drawing
    draw_map()
  
    # Draw the player based on current animation and direction
    screen.blit(player_frames[player_animation][player_direction][player_frame], (player_x, player_y))

  
    pygame.display.flip()

# Clean up and close the game
pygame.quit()
sys.exit()
