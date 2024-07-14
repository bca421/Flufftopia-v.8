import pygame
import sys
import pytmx

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 16
MAP_WIDTH = 100
MAP_HEIGHT = 100
ZOOM_LEVEL = 5  # Initial zoom level (2x)

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flufftopia RPG")

# Load spritesheet
spritesheet = pygame.image.load("assets/Player/character.png").convert_alpha()

# Load TMX map
tmx_data = pytmx.load_pygame("assets/Map/map.tmx")

# Function to draw map tiles
def draw_map(surface, tmx_data, camera_x, camera_y, zoom):
    tile_size = TILE_SIZE * zoom
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen_x = (x * tile_size) - camera_x
                    screen_y = (y * tile_size) - camera_y
                    surface.blit(pygame.transform.scale(tile, (tile_size, tile_size)), (screen_x, screen_y))

# Function to extract frames from spritesheet and scale them
def get_frames(sheet, frame_width, frame_height, num_frames, scale_factor, start_x, start_y):
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(start_x + i * frame_width, start_y, frame_width, frame_height))
        scaled_frame = pygame.transform.scale(frame, (int(frame_width * scale_factor), int(frame_height * scale_factor)))
        frames.append(scaled_frame)
    return frames

# Update frame parameters
frame_width = 64
frame_height = 64
num_frames = 9
scale_factor = 1.5

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

# Initialize player properties
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_animation = 'idle'
player_direction = 'down'
player_frame = 0
player_speed = 5

# Find player start position from TMX object layer
player_start = None
for obj in tmx_data.objects:
    if obj.name == 'player_start':
        player_start = obj
        break

if player_start:
    player_x = player_start.x
    player_y = player_start.y

# Initialize camera position
camera_x = player_x * ZOOM_LEVEL - SCREEN_WIDTH // 2
camera_y = player_y * ZOOM_LEVEL - SCREEN_HEIGHT // 2

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        new_x = player_x - player_speed
        if new_x > 0:
            player_x = new_x
            player_animation = 'walking'
            player_direction = 'left'
    elif keys[pygame.K_RIGHT]:
        new_x = player_x + player_speed
        if new_x < SCREEN_WIDTH - frame_width * scale_factor:
            player_x = new_x
            player_animation = 'walking'
            player_direction = 'right'
    elif keys[pygame.K_UP]:
        new_y = player_y - player_speed
        if new_y > 0:
            player_y = new_y
            player_animation = 'walking'
            player_direction = 'up'
    elif keys[pygame.K_DOWN]:
        new_y = player_y + player_speed
        if new_y < SCREEN_HEIGHT - frame_height * scale_factor:
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

    # Center the camera on the player
    camera_x = player_x * ZOOM_LEVEL - SCREEN_WIDTH // 2
    camera_y = player_y * ZOOM_LEVEL - SCREEN_HEIGHT // 2

    screen.fill((0, 0, 0))
    draw_map(screen, tmx_data, camera_x, camera_y, ZOOM_LEVEL)

    # Draw the player based on current animation and direction
    screen.blit(player_frames[player_animation][player_direction][player_frame], (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
