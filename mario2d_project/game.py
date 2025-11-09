import pygame
import threading
import random

# -------------------- CONFIGURACIÓN --------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PLAYER_SIZE = 50
PLAYER_COLOR = (255, 0, 0)
PLAYER_SPEED = 5
JUMP_SPEED = -15
GRAVITY = 1
MAX_JUMPS = 2

PLATFORM_COLOR = (139, 69, 19)
ENEMY_COLOR = (0, 255, 0)
COIN_COLOR = (255, 255, 0)

NUM_ENEMIES = 5
NUM_COINS = 10
LEVEL_LENGTH = 2000  # ancho total del nivel

# -------------------- INICIALIZACIÓN --------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini Mario 2D")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# -------------------- OBJETOS --------------------
player_rect = pygame.Rect(100, SCREEN_HEIGHT - PLAYER_SIZE - 50, PLAYER_SIZE, PLAYER_SIZE)
player_vel_y = 0
jumps_left = MAX_JUMPS
lives = 3
score = 0
camera_x = 0  # desplazamiento de la cámara

# Crear plataformas a lo largo del nivel
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT - 20, LEVEL_LENGTH, 20),
    pygame.Rect(300, 450, 200, 20),
    pygame.Rect(700, 350, 200, 20),
    pygame.Rect(1200, 400, 200, 20),
    pygame.Rect(1600, 300, 150, 20)
]

enemies = [pygame.Rect(random.randint(300, LEVEL_LENGTH-50), 430, 40, 40) for _ in range(NUM_ENEMIES)]
coins = [pygame.Rect(random.randint(200, LEVEL_LENGTH-50), random.randint(200, 500), 20, 20) for _ in range(NUM_COINS)]

enemy_lock = threading.Lock()
coin_lock = threading.Lock()

# -------------------- FUNCIONES HILOS --------------------
def move_enemies():
    while True:
        enemy_lock.acquire()
        try:
            for e in enemies:
                e.x += random.choice([-2, 2])
                if e.x < 0:
                    e.x = 0
                if e.x > LEVEL_LENGTH - e.width:
                    e.x = LEVEL_LENGTH - e.width
        finally:
            enemy_lock.release()
        pygame.time.wait(100)

def move_coins():
    while True:
        coin_lock.acquire()
        try:
            for c in coins:
                c.y += random.choice([-1, 1])
                if c.y < 50:
                    c.y = 50
                if c.y > SCREEN_HEIGHT - 50:
                    c.y = SCREEN_HEIGHT - 50
        finally:
            coin_lock.release()
        pygame.time.wait(200)

threading.Thread(target=move_enemies, daemon=True).start()
threading.Thread(target=move_coins, daemon=True).start()

# -------------------- BUCLE PRINCIPAL --------------------
running = True
while running:
    clock.tick(FPS)
    on_ground = False

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and jumps_left > 0:
                player_vel_y = JUMP_SPEED
                jumps_left -= 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.x > 0:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_rect.x < LEVEL_LENGTH - PLAYER_SIZE:
        player_rect.x += PLAYER_SPEED

    # Física jugador
    player_vel_y += GRAVITY
    player_rect.y += player_vel_y

    # Colisión con plataformas
    for plat in platforms:
        if player_rect.colliderect(plat) and player_vel_y >= 0:
            player_rect.bottom = plat.top
            player_vel_y = 0
            on_ground = True
            jumps_left = MAX_JUMPS

    if player_rect.bottom >= SCREEN_HEIGHT:
        player_rect.bottom = SCREEN_HEIGHT
        player_vel_y = 0
        on_ground = True
        jumps_left = MAX_JUMPS

    # Colisión con enemigos
    enemy_lock.acquire()
    try:
        for e in enemies:
            if player_rect.colliderect(e):
                lives -= 1
                player_rect.x = 100
                player_rect.y = SCREEN_HEIGHT - PLAYER_SIZE - 50
    finally:
        enemy_lock.release()

    # Colisión con monedas
    coin_lock.acquire()
    try:
        for c in coins[:]:
            if player_rect.colliderect(c):
                score += 10
                coins.remove(c)
    finally:
        coin_lock.release()

    # Ajustar cámara
    camera_x = max(0, player_rect.x - SCREEN_WIDTH // 2)
    camera_x = min(camera_x, LEVEL_LENGTH - SCREEN_WIDTH)

    # Dibujar
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, PLAYER_COLOR, (player_rect.x - camera_x, player_rect.y, PLAYER_SIZE, PLAYER_SIZE))

    for plat in platforms:
        pygame.draw.rect(screen, PLATFORM_COLOR, (plat.x - camera_x, plat.y, plat.width, plat.height))

    enemy_lock.acquire()
    try:
        for e in enemies:
            pygame.draw.rect(screen, ENEMY_COLOR, (e.x - camera_x, e.y, e.width, e.height))
    finally:
        enemy_lock.release()

    coin_lock.acquire()
    try:
        for c in coins:
            pygame.draw.circle(screen, COIN_COLOR, (c.x - camera_x + 10, c.y + 10), 10)
    finally:
        coin_lock.release()

    # HUD
    hud = font.render(f"Lives: {lives}  Score: {score}", True, (255, 255, 255))
    screen.blit(hud, (10, 10))

    pygame.display.flip()

    # Game over
    if lives <= 0:
        running = False

pygame.quit()
