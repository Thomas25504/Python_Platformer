# main.py
from __future__ import annotations
import pygame
import sys

from config import *
from levelLoad import *
from player import Player
from camera import Camera


def draw_centered_text(screen, font, text, y, color=COLOR_TEXT):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(SCREEN_W // 2, y))
    screen.blit(surf, rect)


def draw_button_rect(screen, rect, base_color, hover_color, mouse_pos, border_radius=12):
    """Draw a rect button that changes color on hover. Returns True if hovered."""
    hovered = rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, hover_color if hovered else base_color, rect, border_radius=border_radius)
    return hovered


def draw_checkmark(screen, center, size, color, thickness=4):
    cx, cy = center
    x1, y1 = cx - size // 2, cy
    x2, y2 = cx - size // 6, cy + size // 3
    x3, y3 = cx + size // 2, cy - size // 3

    pygame.draw.line(screen, color, (x1, y1), (x2, y2), thickness)
    pygame.draw.line(screen, color, (x2, y2), (x3, y3), thickness)


def compute_unlocked_upto(completed_levels: set[int], unlock_all: bool, max_level: int) -> int:
    if unlock_all:
        return max_level

    i = 1
    while i in completed_levels:
        i += 1

    unlocked = min(i, max_level)
    return max(unlocked, 1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Platformer (Levels + Key/Exit)")
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont(None, 64)
    font = pygame.font.SysFont(None, 28)
    font_small = pygame.font.SysFont(None, 22)

    state = STATE_MENU
    completed_levels: set[int] = set()

    current_level_num: int | None = None
    level: LevelData | None = None
    player: Player | None = None
    camera: Camera | None = None
    has_key = False

    # NEW: unlock-all toggle
    unlock_all = False

    # Buttons (menu)
    btn_w, btn_h = 320, 60
    start_btn = pygame.Rect((SCREEN_W - btn_w)//2, 300, btn_w, btn_h)
    quit_btn = pygame.Rect((SCREEN_W - btn_w)//2, 380, btn_w, btn_h)

    # Level select layout + pagination
    levels_per_page = 5
    current_page = 0
    base_y = 220
    gap = 70
    back_btn = pygame.Rect(20, 20, 140, 45)

    def level_rect_for_index(idx_on_page: int) -> pygame.Rect:
        y = base_y + idx_on_page * gap
        return pygame.Rect((SCREEN_W - btn_w)//2, y, btn_w, btn_h)

    # unlock-all option button + page nav
    unlock_btn = pygame.Rect((SCREEN_W - btn_w)//2, 600, btn_w, 55)
    nav_w, nav_h = 140, 55
    prev_btn = pygame.Rect(unlock_btn.x - nav_w - 30, 600, nav_w, nav_h)
    next_btn = pygame.Rect(unlock_btn.right + 30, 600, nav_w, nav_h)

    def start_level(n: int):
        nonlocal current_level_num, level, player, camera, has_key, state
        current_level_num = n
        level = load_level(LEVEL_FILES[n])
        player = Player(level.spawn)
        camera = Camera(SCREEN_W, SCREEN_H)
        has_key = False
        state = STATE_PLAYING

    while True:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        max_level = len(LEVEL_FILES)
        unlocked_upto = compute_unlocked_upto(completed_levels, unlock_all, max_level)
        page_count = max(1, (max_level + levels_per_page - 1) // levels_per_page)
        current_page = min(current_page, page_count - 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == STATE_PLAYING:
                        state = STATE_LEVEL_SELECT
                    elif state == STATE_LEVEL_COMPLETE:
                        state = STATE_LEVEL_SELECT
                    elif state == STATE_LEVEL_SELECT:
                        state = STATE_MENU

                if state == STATE_PLAYING:
                    if event.key == pygame.K_r and current_level_num is not None:
                        start_level(current_level_num)

                if state == STATE_LEVEL_COMPLETE:
                    if event.key == pygame.K_RETURN:
                        state = STATE_LEVEL_SELECT

                # Page navigation in Level Select
                if state == STATE_LEVEL_SELECT:
                    if event.key == pygame.K_RIGHT:
                        current_page = min(current_page + 1, page_count - 1)
                    elif event.key == pygame.K_LEFT:
                        current_page = max(current_page - 1, 0)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                
                # Menu clicks
                if state == STATE_MENU:
                    if start_btn.collidepoint(mx, my):
                        state = STATE_LEVEL_SELECT
                    elif quit_btn.collidepoint(mx, my):
                        pygame.quit()
                        sys.exit()

                elif state == STATE_LEVEL_SELECT:
                    if back_btn.collidepoint(mx, my):
                        state = STATE_MENU

                    # toggle unlock-all
                    elif unlock_btn.collidepoint(mx, my):
                        unlock_all = not unlock_all

                    # page navigation buttons
                    elif prev_btn.collidepoint(mx, my):
                        current_page = max(current_page - 1, 0)
                    elif next_btn.collidepoint(mx, my):
                        current_page = min(current_page + 1, page_count - 1)

                    else:
                        start_n = current_page * levels_per_page + 1
                        end_n = min(start_n + levels_per_page, max_level + 1)
                        for idx, n in enumerate(range(start_n, end_n)):
                            rect = level_rect_for_index(idx)
                            if rect.collidepoint(mx, my) and n <= unlocked_upto:
                                start_level(n)

                elif state == STATE_LEVEL_COMPLETE:
                    if back_btn.collidepoint(mx, my):
                        state = STATE_LEVEL_SELECT

       
        # Draw / Update
        screen.fill(COLOR_BG)

        if state == STATE_MENU:
            draw_centered_text(screen, font_big, "BLOCK PLATFORMER", 140)
            draw_centered_text(screen, font, "Main Menu", 200, COLOR_HEADER)

            draw_button_rect(screen, start_btn, COLOR_PANEL, COLOR_PANEL_HOVER, mouse_pos, border_radius=12)
            draw_button_rect(screen, quit_btn, COLOR_PANEL, COLOR_PANEL_HOVER, mouse_pos, border_radius=12)
            draw_centered_text(screen, font, "Start", start_btn.centery)
            draw_centered_text(screen, font, "Quit", quit_btn.centery)

            draw_centered_text(
                screen, font_small,
                "Controls: A/D move, hold SPACE to jump, R restart, ESC back",
                640, COLOR_TEXT_WARM
            )

        elif state == STATE_LEVEL_SELECT:
            draw_centered_text(screen, font_big, "LEVEL SELECT", 120)

            draw_button_rect(screen, back_btn, COLOR_PANEL_DARK, COLOR_PANEL_DARK_HOVER, mouse_pos, border_radius=10)
            screen.blit(font.render("Back", True, COLOR_TEXT), (back_btn.x + 35, back_btn.y + 10))

            # Determine page slice
            start_n = current_page * levels_per_page + 1
            end_n = min(start_n + levels_per_page, max_level + 1)

            # Level buttons (page-based; show locked state if needed)
            for idx, n in enumerate(range(start_n, end_n)):
                rect = level_rect_for_index(idx)
                is_unlocked = n <= unlocked_upto
                is_done = n in completed_levels

                if is_unlocked:
                    draw_button_rect(screen, rect, COLOR_PANEL, COLOR_PANEL_HOVER, mouse_pos, border_radius=12)
                    label = f"Level {n}"
                    draw_centered_text(screen, font, label, rect.centery, COLOR_TEXT)

                    if is_done:
                        tick_center = (rect.right - 35, rect.centery)
                        draw_checkmark(screen, tick_center, size=22, color=COLOR_EXIT_UNLOCKED, thickness=4)
                else:
                    pygame.draw.rect(screen, COLOR_PANEL_DARK, rect, border_radius=12)
                    label = f"Level {n}  LOCKED"
                    draw_centered_text(screen, font, label, rect.centery, COLOR_TEXT_MUTED)

                    if is_done:
                        tick_center = (rect.right - 35, rect.centery)
                        draw_checkmark(screen, tick_center, size=22, color=COLOR_TEXT_MUTED, thickness=4)

            # Unlock-all toggle button
            unlock_label = f"Unlock All Levels: {'ON' if unlock_all else 'OFF'}"
            draw_button_rect(screen, unlock_btn, COLOR_PANEL_DARK, COLOR_PANEL_DARK_HOVER, mouse_pos, border_radius=12)
            draw_centered_text(screen, font, unlock_label, unlock_btn.centery, COLOR_TEXT)

            # Page controls
            draw_button_rect(screen, prev_btn, COLOR_PANEL_DARK, COLOR_PANEL_DARK_HOVER, mouse_pos, border_radius=10)
            draw_button_rect(screen, next_btn, COLOR_PANEL_DARK, COLOR_PANEL_DARK_HOVER, mouse_pos, border_radius=10)
            screen.blit(font.render("Prev", True, COLOR_TEXT), (prev_btn.x + 28, prev_btn.y + 14))
            screen.blit(font.render("Next", True, COLOR_TEXT), (next_btn.x + 26, next_btn.y + 14))

            page_label = f"Page {current_page + 1} / {page_count}"
            draw_centered_text(screen, font_small, page_label, prev_btn.centery - 30, COLOR_TEXT_MUTED)

            hint = f"Use Prev/Next or Arrows to change pages. Unlocked: 1–{unlocked_upto}"
            draw_centered_text(screen, font_small, hint, 680, COLOR_TEXT_MUTED)

        elif state == STATE_PLAYING:
            assert level is not None and player is not None and camera is not None and current_level_num is not None

            # update
            player.update(keys, level.solids)

            # key pickup
            if level.key_rect is not None and (not has_key) and player.rect.colliderect(level.key_rect):
                has_key = True

            # win condition
            if level.exit_rect is not None and player.rect.colliderect(level.exit_rect) and has_key:
                completed_levels.add(current_level_num)
                state = STATE_LEVEL_COMPLETE

            # camera follow
            camera.follow(player.rect, level.size_px)

            # draw solids
            for s in level.solids:
                pygame.draw.rect(screen, COLOR_SOLID, camera.apply(s))

            # draw key if not collected
            if level.key_rect is not None and not has_key:
                pygame.draw.rect(screen, COLOR_KEY, camera.apply(level.key_rect))

            # draw exit: red if no key, green if has key
            if level.exit_rect is not None:
                color = COLOR_EXIT_UNLOCKED if has_key else COLOR_EXIT_LOCKED
                pygame.draw.rect(screen, color, camera.apply(level.exit_rect))

            # draw player
            pygame.draw.rect(screen, COLOR_PLAYER, camera.apply(player.rect))

            # UI
            ui1 = f"Level {current_level_num} | Key: {'YES' if has_key else 'NO'}"
            ui2 = "A/D move | hold SPACE to jump | R restart | ESC level select"
            screen.blit(font.render(ui1, True, COLOR_TEXT), (10, 10))
            screen.blit(font_small.render(ui2, True, COLOR_UI_ACCENT), (10, 40))

        elif state == STATE_LEVEL_COMPLETE:
            assert current_level_num is not None
            draw_centered_text(screen, font_big, f"LEVEL {current_level_num} COMPLETE!", 220)
            draw_centered_text(screen, font, "You escaped with the key.", 290, COLOR_TEXT_MUTED)
            draw_centered_text(screen, font_small, "Press ENTER to return to Level Select (or ESC).", 350, COLOR_TEXT_MUTED)

            draw_button_rect(screen, back_btn, COLOR_PANEL_DARK, COLOR_PANEL_DARK_HOVER, mouse_pos, border_radius=10)
            screen.blit(font.render("Levels", True, COLOR_TEXT), (back_btn.x + 32, back_btn.y + 10))

        pygame.display.flip()


if __name__ == "__main__":
    main()