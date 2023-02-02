import pygame
from pygame.math import Vector2

class GameObject:
    def __init__(self, color, dim, pos, vel=0):
        self.color = color
        self.dim = Vector2(dim)
        self.pos = Vector2(pos)
        self.vel = vel
        self.rect = pygame.Rect(self.pos, self.dim)        
    
    def move(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=-1)
    
    def collide_with(self, other):
        return pygame.Rect.colliderect(self.rect, other.rect)

class Player(GameObject):
    def __init__(self, color, dim, pos, vel=0):
        super().__init__(color, dim, pos, vel)       
        self.health = 1000

        self.font = pygame.font.SysFont('timesnewroman', 20)
        self.health_text = self.font.render(str(self.health), False, color, (0, 0, 0))

    def shoot(self, shoot_pos):
        from game import bullets_of_player1, bullets_of_player2
        
        if shoot_pos == "left":
            bullets_of_player1.append(Bullet(self.color, (self.rect.x + self.rect.width, self.rect.y + self.rect.width // 2), 3, shoot_pos))

        if shoot_pos == "right":
            bullets_of_player2.append(Bullet(self.color, (self.rect.x - 5, self.rect.y + self.rect.width // 2), -3, shoot_pos))
    
    def decrease_health(self, collided_obj):
        if type(collided_obj) is Bullet:
            self.health -= 50
        if type(collided_obj) is Obstacle:
            self.health -= 3
    
    def show_health(self, surface, pos):
        self.health_text = self.font.render(str(self.health), False, self.color, (0, 0, 0))
        surface.blit(self.health_text, pos)


class Bullet(GameObject):
    def __init__(self, color, pos, vel, shoot_dir):
        self.shoot_dir = shoot_dir
        super().__init__(color, (10, 6), pos, vel)

    def move(self):
        if self.shoot_dir == "right":
            self.vel -= 2
        if self.shoot_dir == "left":
            self.vel += 2
        self.rect.move_ip((self.vel, 0))

class Obstacle(GameObject):
    def __init__(self, color, pos, vel):
        super().__init__(color, Vector2(30, 30), pos, vel)
    
    def move(self):
        self.rect.move_ip(0, self.vel)