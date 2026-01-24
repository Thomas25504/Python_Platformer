
import pygame

from config import *



class Player:
    def __init__(self, pos: pygame.Vector2):
        self.rect = pygame.Rect(pos.x, pos.y, int(TILE_SIZE * 0.8), int(TILE_SIZE * 0.9))
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False

        #track whether space is currently held
        self.jump_held = False

    def handle_input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_a]:
            self.vel.x = -MOVE_SPEED
        if keys[pygame.K_d]:
            self.vel.x = MOVE_SPEED

        #read whether space is held
        self.jump_held = keys[pygame.K_SPACE]

    def do_jump(self):
        # Jump only when grounded - no double jumps
        self.vel.y = -JUMP_SPEED
        self.on_ground = False

    def apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > 20:
            self.vel.y = 20

    def move_and_collide(self, solids):
        # X axis
        self.rect.x += int(self.vel.x)
        for s in solids:
            if self.rect.colliderect(s):
                if self.vel.x > 0:
                    self.rect.right = s.left
                elif self.vel.x < 0:
                    self.rect.left = s.right

        # Y axis
        self.rect.y += int(self.vel.y)
        self.on_ground = False
        for s in solids:
            if self.rect.colliderect(s):
                if self.vel.y > 0:  # falling
                    self.rect.bottom = s.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:  # jumping up
                    self.rect.top = s.bottom
                    self.vel.y = 0

    def update(self, keys, solids):
        self.handle_input(keys)
        self.apply_gravity()
        self.move_and_collide(solids)

        # if space is held and player is on ground, jump
        if self.jump_held and self.on_ground:
            self.do_jump()
