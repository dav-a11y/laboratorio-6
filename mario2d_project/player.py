import pygame

class Player:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.vel_y = 0
        self.on_ground = False

    def move(self, keys):
        # Movimiento horizontal
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Gravedad y salto
        self.vel_y += 1
        self.rect.y += self.vel_y

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15

        # Limitar al suelo
        if self.rect.bottom >= 580:
            self.rect.bottom = 580
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
