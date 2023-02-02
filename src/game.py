import pygame
from pygame.time import Clock
from models import *
import random

WIDTH, HEIGHT = 720, 480
PLAYER_DIM = (40, 40)
FLOOR_DIM = (720, 50)
BOUNDARY_DIM = (2, 480)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (100, 0, 100)

MOVE_SPEED = 10
FPS = 30

bullets_of_player1 = []
bullets_of_player2 = []
obstacles = []

class DualStrike:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Dual Strike")

        self.game_over = False

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen_rect = self.screen.get_rect()
        self.boundary = GameObject(BLACK, BOUNDARY_DIM, (WIDTH // 2, 0))

        self.clock = Clock()
        self.time = 0
        self.cur = self.time

        self.player1 = Player(RED, PLAYER_DIM, (60, 280))
        self.player2 = Player(GREEN, PLAYER_DIM, (WIDTH - PLAYER_DIM[0] - 60, 280))

        self.floor_top = GameObject(BLACK, FLOOR_DIM, (0, 0))
        self.floor_bottom = GameObject(BLACK, FLOOR_DIM, (0, 430))

        global obstacles
        obstacles = [Obstacle(PURPLE, (random.randint(0, 690), self.floor_top.rect.height), 2) for _ in range(0, 5)]
    
    def main_loop(self):
        while True:
            if self.player1.health <= 0 or self.player2.health <= 0:
                self.game_over = True
            if self.game_over:
                self._game_over()
            else:
                self._handle_input()
                self._game_logic()
                self._draw()
            

    @property
    def gameObjects(self):
        return [*obstacles, *bullets_of_player1, *bullets_of_player2, self.player1, self.player2, self.floor_top, self.floor_bottom, self.boundary]

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    self.player2.shoot("right")
                if event.key == pygame.K_f:
                    self.player1.shoot("left")
        
        events = pygame.key.get_pressed()

        if events[pygame.K_a] and self.player1.rect.x > 0:
            self.player1.rect.move_ip(-MOVE_SPEED, 0)
        if events[pygame.K_d] and self.player1.rect.x + self.player1.rect.width < self.screen_rect.width // 2:
            self.player1.rect.move_ip(MOVE_SPEED, 0)
        if events[pygame.K_w] and self.player1.rect.y > self.floor_top.rect.height:
            self.player1.rect.move_ip(0, -MOVE_SPEED)
        if events[pygame.K_s] and self.player1.rect.y + self.player1.rect.height < self.floor_bottom.rect.y:
            self.player1.rect.move_ip(0, MOVE_SPEED)

        if events[pygame.K_LEFT] and self.player2.rect.x > self.screen_rect.width // 2:
            self.player2.rect.move_ip(-MOVE_SPEED, 0)
        if events[pygame.K_RIGHT] and self.player2.rect.x + self.player2.rect.width < self.screen_rect.width:
            self.player2.rect.move_ip(MOVE_SPEED, 0)
        if events[pygame.K_UP] and self.player2.rect.y > self.floor_top.rect.height:
            self.player2.rect.move_ip(0, -MOVE_SPEED)
        if events[pygame.K_DOWN] and self.player2.rect.y + self.player2.rect.height < self.floor_bottom.rect.y:
            self.player2.rect.move_ip(0, MOVE_SPEED)
        

    def _game_logic(self):
        global obstacles

        for obj in self.gameObjects:
            obj.move()

        for bullet in bullets_of_player2[:]:
            if self.player1.collide_with(bullet) or bullet.rect.x < 0:
                bullets_of_player2.remove(bullet)
                if self.player1.collide_with(bullet):
                    self.player1.decrease_health(bullet)
                break
            for obstacle in obstacles:
                if bullet.collide_with(obstacle):
                    bullets_of_player2.remove(bullet)
                    break
        
        for bullet in bullets_of_player1[:]:
            if self.player2.collide_with(bullet) or bullet.rect.x > self.screen_rect.width:
                bullets_of_player1.remove(bullet)
                if self.player2.collide_with(bullet):
                    self.player2.decrease_health(bullet)
                break
            for obstacle in obstacles:
                if bullet.collide_with(obstacle):
                    bullets_of_player1.remove(bullet)
                    break
        
        for obstacle in obstacles[:]:
            if obstacle.collide_with(self.player1):
                self.player1.decrease_health(obstacle)
            if obstacle.collide_with(self.player2):
                self.player2.decrease_health(obstacle)
        
        if self.time % 2 == 0 and self.cur != self.time:
            temp_list = [Obstacle(PURPLE, (random.randint(0, 690), 0), 2) for _ in range(0, random.randint(2, 5))]
            obstacles += temp_list
            self.cur = self.time
        
        for obstacle in obstacles[:]:
            if obstacle.rect.y == self.floor_bottom.rect.y:
                obstacles.remove(obstacle)


    def _draw(self):
        self.screen.fill(WHITE)
        
        for obj in self.gameObjects:
            obj.draw(self.screen)

        self.player1.show_health(self.screen, (20, 15))
        self.player2.show_health(self.screen, (
            self.screen_rect.width-(self.player2.health_text.get_rect().width + 20)
            , 15))

        self.time = pygame.time.get_ticks() // 1000
        self.clock.tick(FPS)
        pygame.display.flip()
    
    def _game_over(self):
        self.game_over_font = pygame.font.SysFont("timesnewroman", 20)
        self.game_over_background = pygame.Surface((WIDTH, HEIGHT))
        self.game_over_background.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    global bullets_of_player1, bullets_of_player2, obstacles
                    self.game_over = False
                    self.player1 = Player(RED, PLAYER_DIM, (60, 280))
                    self.player2 = Player(GREEN, PLAYER_DIM, (WIDTH - PLAYER_DIM[0] - 60, 280))
                    bullets_of_player1, bullets_of_player2, obstacles = [], [], []

        if self.player1.health <= 0:
            self.game_over_text = self.game_over_font.render("Player 2 (Green) has won", False, GREEN)
            self.play_again_text = self.game_over_font.render("Press R to play again", False, GREEN)

        elif self.player2.health <= 0:
            self.game_over_text = self.game_over_font.render("Player 1 (Red) has won", False, RED)
            self.play_again_text = self.game_over_font.render("Press R to play again", False, RED)

        bg_rect =self.game_over_background.get_rect()
        text_dimension = self.game_over_text.get_size()
        play_again_dimension = self.play_again_text.get_size()

        bg_center_x, bg_center_y = bg_rect.center
        text_width, text_height = text_dimension
        play_again_width, play_again_height = play_again_dimension

        self.game_over_background.blit(self.game_over_text, (bg_center_x - (text_width // 2), bg_center_y - (text_height // 2)))
        self.game_over_background.blit(self.play_again_text, (bg_center_x - (play_again_width // 2), bg_center_y + (play_again_height // 2)))
        self.screen.blit(self.game_over_background, (0, 0))

        self.clock.tick(FPS)
        pygame.display.flip()
