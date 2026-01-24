import pygame

class Camera:
    def __init__(self, screen_width, screen_height):
        self.w = screen_width
        self.h = screen_height
        self.x = 0
        self.y = 0

    def follow(self, target_rect, level_size):
        level_w, level_h = level_size

        # direct-follow camera
        self.x = target_rect.centerx - self.w // 2
        self.y = target_rect.centery - self.h // 2

        # clamp to level bounds
        self.x = max(0, min(self.x, level_w - self.w))
        self.y = max(0, min(self.y, level_h - self.h))

    def apply(self, rect):
        return pygame.Rect(rect.x - self.x, rect.y - self.y, rect.w, rect.h)

    def apply_point(self, x, y):
        return (x - self.x, y - self.y)