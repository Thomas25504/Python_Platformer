
from dataclasses import dataclass

from config import *
import pygame

@dataclass
class LevelData:
    solids: list
    spawn: pygame.Vector2
    key_rect: pygame.Rect | None
    exit_rect: pygame.Rect | None
    size_px: tuple[int, int]
    raw_lines: list[str]

def load_level(path: str) -> LevelData:
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    solids: list[pygame.Rect] = []
    spawn = pygame.Vector2(0, 0)
    key_rect = None
    exit_rect = None

    for row, line in enumerate(lines):
        for col, ch in enumerate(line):
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            if ch == "#":
                solids.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif ch == "P":
                spawn = pygame.Vector2(x, y)
            elif ch == "K":
                key_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            elif ch == "E":
                exit_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    level_w = (max((len(line) for line in lines), default=0)) * TILE_SIZE
    level_h = len(lines) * TILE_SIZE

    return LevelData(
        solids=solids,
        spawn=spawn,
        key_rect=key_rect,
        exit_rect=exit_rect,
        size_px=(level_w, level_h),
        raw_lines=lines
    )