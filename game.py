import os
import sys
import pygame as pg
import itertools

from constants       import *
from settings        import load_settings, save_settings
from game_state      import GameState
from level_loader    import load_level
from entities.pacman import PacMan
from entities.ghost  import Ghost
from menu            import Menu

class Game:
    def __init__(self):
        pg.init()
        #Налаштування вікна та завантаження логотипу
        self.settings = load_settings()
        w, h = self.settings["resolution"]
        self.screen = pg.display.set_mode((w, h))
        pg.display.set_caption("Pac-Man")

        logo_path = os.path.join("data", "pacman_logo.png")
        if not os.path.isfile(logo_path):
            print(f"Логотип не знайдено: {logo_path}")
            sys.exit()
        self.logo = pg.image.load(logo_path).convert_alpha()
        logo_w = int(w * 0.6)
        logo_h = int(self.logo.get_height() * (logo_w / self.logo.get_width()))
        self.logo = pg.transform.scale(self.logo, (logo_w, logo_h))

        #Меню
        self.menu = Menu(self.screen)
        self.menu.options = ["Start Game", "Difficulty", "Resolution", "Exit"]
        self.diff_menu = Menu(self.screen)
        self.diff_menu.options = ["Normal", "Hard", "Back"]
        self.res_menu = Menu(self.screen)
        self.res_menu.options = ["800x600", "1280x720", "1600x900", "Back"]
        self.game_over_menu = Menu(self.screen)
        self.game_over_menu.options = ["Retry", "Main Menu"]
        self.victory_menu = Menu(self.screen)
        self.victory_menu.options = ["Retry", "Main Menu"]

        #Загальні
        self.clock = pg.time.Clock()
        self.font  = pg.font.Font(None, 28)
        self.state = GameState.MENU

        #Ігрові змінні
        self.level_idx = 1
        self.score     = 0
        self.lives     = 3

        #Підготовка рівня
        self._load_level()
        level_path = f"levels/level{self.level_idx}.txt"
        with open(level_path, encoding="utf-8") as f:
            lines = [ln.rstrip("\n") for ln in f if ln.strip()]
        self.map_cols = len(lines[0])
        self.map_rows = len(lines)
        self.map_surface = pg.Surface((self.map_cols * TILE,
                                       self.map_rows * TILE))

    def _load_level(self):
        path = f"levels/level{self.level_idx}.txt"
        walls, coins, power, portals, ppos, gpos = load_level(path)
        self.walls, self.coins, self.power, self.portals = walls, coins, power, portals

        maxg = 4 if self.settings.get("difficulty", "normal") == "hard" else 2
        selected_gpos = gpos[:maxg]

        speed = 150 if self.settings["difficulty"] == "normal" else 180
        self.player = PacMan(ppos, speed)
        self.ghosts = [Ghost(pos, i, 120, self.walls)
                       for i, pos in enumerate(selected_gpos)]

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    running = False

                # — Обробка меню
                if self.state == GameState.MENU:
                    choice = self.menu.handle_event(e)
                    if choice == "Start Game":
                        self.score = 0; self.lives = 3; self.level_idx = 1
                        self._load_level()
                        self.state = GameState.PLAY
                    elif choice == "Difficulty":
                        self.state = GameState.DIFFICULTY
                    elif choice == "Resolution":
                        self.state = GameState.RESOLUTION
                    elif choice == "Exit":
                        running = False

                elif self.state == GameState.DIFFICULTY:
                    choice = self.diff_menu.handle_event(e)
                    if choice in ("Normal", "Hard"):
                        self.settings["difficulty"] = choice.lower()
                        save_settings(self.settings)
                        self.state = GameState.MENU
                    elif choice == "Back":
                        self.state = GameState.MENU

                elif self.state == GameState.RESOLUTION:
                    choice = self.res_menu.handle_event(e)
                    if choice and choice.endswith(("x600","x720","x900")):
                        w, h = map(int, choice.split("x"))
                        self.settings["resolution"] = [w, h]
                        save_settings(self.settings)
                        self.screen = pg.display.set_mode((w, h))
                        for m in (self.menu, self.diff_menu, self.res_menu, self.game_over_menu, self.victory_menu):
                            m.screen = self.screen
                        self.state = GameState.MENU
                    elif choice == "Back":
                        self.state = GameState.MENU

                elif self.state == GameState.GAME_OVER_MENU:
                    choice = self.game_over_menu.handle_event(e)
                    if choice == "Retry":
                        self.score = 0; self.lives = 3
                        self._load_level()
                        self.state = GameState.PLAY
                    elif choice == "Main Menu":
                        self.state = GameState.MENU

                elif self.state == GameState.VICTORY_MENU:
                    choice = self.victory_menu.handle_event(e)
                    if choice == "Retry":
                        self.score = 0; self.lives = 3
                        self._load_level()
                        self.state = GameState.PLAY
                    elif choice == "Main Menu":
                        self.state = GameState.MENU

                elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    if self.state == GameState.PLAY:
                        self.state = GameState.PAUSE
                    elif self.state == GameState.PAUSE:
                        self.state = GameState.PLAY

            if self.state == GameState.PLAY:
                self.update(dt)

            # Рендеринг
            self.screen.fill(BLACK)

            if self.state == GameState.MENU:
                self.screen.fill(YELLOW)
                x = (self.screen.get_width() - self.logo.get_width()) // 2
                self.screen.blit(self.logo, (x, 40))
                self.menu.draw()

            elif self.state == GameState.DIFFICULTY:
                self.screen.fill(YELLOW)
                x = (self.screen.get_width() - self.logo.get_width()) // 2
                self.screen.blit(self.logo, (x, 40))
                self.diff_menu.draw()

            elif self.state == GameState.RESOLUTION:
                self.screen.fill(YELLOW)
                x = (self.screen.get_width() - self.logo.get_width()) // 2
                self.screen.blit(self.logo, (x, 40))
                self.res_menu.draw()

            else:
                self.draw_game()
                if self.state == GameState.PAUSE:
                    txt = self.font.render("Paused", True, WHITE)
                    self.screen.blit(txt, txt.get_rect(center=self.screen.get_rect().center))
                elif self.state == GameState.GAME_OVER_MENU:
                    txt = self.font.render("Game Over", True, RED)
                    self.screen.blit(txt, txt.get_rect(center=(self.screen.get_width()//2,50)))
                    self.game_over_menu.draw()
                elif self.state == GameState.VICTORY_MENU:
                    txt = self.font.render("You Win!", True, WHITE)
                    self.screen.blit(txt, txt.get_rect(center=(self.screen.get_width()//2,50)))
                    self.victory_menu.draw()

            pg.display.flip()

        pg.quit()

    def update(self, dt):
        # Рух пакмена та warp
        self.player.update(dt, self.walls + self.portals)
        max_x = self.map_cols * TILE
        if self.player.rect.right < 0:
            self.player.rect.left = max_x
        elif self.player.rect.left > max_x:
            self.player.rect.right = 0

        # Збір монет і PowerPellets
        for c in list(self.coins):
            if self.player.rect.collidepoint(c.pos):
                self.coins.remove(c)
                self.score += 10
        for p in list(self.power):
            if self.player.rect.collidepoint(p.pos):
                self.power.remove(p)
                for g in self.ghosts:
                    g.set_frightened(8.0)

        # Рух привидів + варп + колізії
        for g in self.ghosts:
            g.update(dt, self.walls, self.player)
            if g.rect.right < 0:
                g.rect.left = max_x
            elif g.rect.left > max_x:
                g.rect.right = 0
            if g.rect.colliderect(self.player.rect):
                if g.frightened_timer > 0:
                    self.score += 200
                    g.respawn()
                else:
                    self.lives -= 1
                    if self.lives > 0:
                        self.player.respawn()
                        for gh in self.ghosts:
                            gh.respawn()
                    else:
                        self.state = GameState.GAME_OVER_MENU
                break

        # Win
        if not self.coins and not self.power:
            self.state = GameState.VICTORY_MENU

    def draw_game(self):
        self.map_surface.fill(BLACK)
        for w in self.walls:
            self.map_surface.blit(w.image, w.rect)
        for obj in itertools.chain(self.coins, self.power):
            obj.draw(self.map_surface)
        self.player.draw(self.map_surface)
        for g in self.ghosts:
            g.draw(self.map_surface)

        win_w, win_h = self.screen.get_size()
        scaled = pg.transform.scale(self.map_surface, (win_w, win_h - 40))
        self.screen.blit(scaled, (0, 0))

        # нижній худ
        score_txt = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_txt = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_txt, (10, win_h - 30))
        self.screen.blit(lives_txt, (win_w - lives_txt.get_width() - 10, win_h - 30))
