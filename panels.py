import pygame
import ingame_windows
import image


class StartGamePanel:

    def __init__(self):
        self.panel = pygame.image.load('assets/accueil/panels/start_game/panel.png')

        self.new_game_button = pygame.image.load('assets/accueil/panels/start_game/new_game_button.png')
        self.new_game_button_rect = self.new_game_button.get_rect()
        self.new_game_button_rect.x = 791
        self.new_game_button_rect.y = 508
        self.new_game_button_h = pygame.image.load('assets/accueil/panels/start_game/new_game_button_hover.png')

        self.load_game_button = pygame.image.load('assets/accueil/panels/start_game/load_game_button.png')
        self.load_game_button_rect = self.load_game_button.get_rect()
        self.load_game_button_rect.x = 130
        self.load_game_button_rect.y = 508
        self.load_game_button_h = pygame.image.load('assets/accueil/panels/start_game/load_game_button_hover.png')

        self.x_button = pygame.image.load('assets/accueil/panels/start_game/x_button.png')
        self.x_button_rect = self.x_button.get_rect()
        self.x_button_rect.x = 1144
        self.x_button_rect.y = 68
        self.x_button_h = pygame.image.load('assets/accueil/panels/start_game/x_button_hover.png')

    def update(self, surface, possouris, basic_accueil):
        surface.blit(self.panel, (0, 0))

        if self.new_game_button_rect.collidepoint(possouris) and not basic_accueil:
            surface.blit(self.new_game_button_h, self.new_game_button_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.new_game_button, self.new_game_button_rect)

        if self.load_game_button_rect.collidepoint(possouris) and not basic_accueil:
            surface.blit(self.load_game_button_h, self.load_game_button_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.load_game_button, self.load_game_button_rect)

        if self.x_button_rect.collidepoint(possouris) and not basic_accueil:
            surface.blit(self.x_button_h, self.x_button_rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            surface.blit(self.x_button, self.x_button_rect)

        if not (self.x_button_rect.collidepoint(possouris) or self.new_game_button_rect.collidepoint(possouris)
                or self.load_game_button_rect.collidepoint(possouris)):

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


class ClassicGamePanel:

    def __init__(self, player):
        self.background = pygame.image.load('assets/game/panels/classic_panel/background.png')
        self.mode_changement_pseudo_image = pygame.image.load('assets/game/panels/classic_panel/'
                                                              'mode_changement_pseudo.png')
        self.curseur_changement_pseudo = image.CursorChangePseudoMode()

        self.font = pygame.font.Font('assets/fonts/impact.ttf', 50)
        self.font_size2 = pygame.font.Font('assets/fonts/impact.ttf', 25)
        self.font_size3 = pygame.font.Font('assets/fonts/(Unranked) Bdeogale.ttf', 70)

        self.player = player
        self.player_name = self.player.name

        self.player_name_image = self.font.render(self.player_name, False, (15, 0, 124))
        self.player_name_indication = self.font_size2.render("(cliquer pour modifier)", False, (15, 0, 124))
        self.player_lv_image = self.font_size3.render(str(self.player.level), False, (124, 124, 124))

        self.is_pname_modif = False

        self.player_name_rect = pygame.Rect(656, 12, 399, 51)
        self.player_name_hover = pygame.image.load("assets/game/panels/classic_panel/player_name_hover.png")
        self.change_player_name_mode = False

        self.alphabet_pixels = {}

        self.current_ig_window_name = 'Unknown'
        self.ingame_window = ingame_windows.IngameWindow(self.current_ig_window_name)

        self.buttons = image.ClassicGamePanelButtons()

    def update(self, surface, possouris):

        surface.blit(self.background, (0, 0))
        surface.blit(self.player_name_image, (662, 10))
        if self.player.level >= 10:
            surface.blit(self.player_lv_image, (955, 73))
        else:
            surface.blit(self.player_lv_image, (965, 73))

        if not self.is_pname_modif:
            surface.blit(self.player_name_indication, (760, 30))

        self.buttons.update(surface, possouris, self.ingame_window)

        # Interactions
        if not self.ingame_window.main_window_rect.collidepoint(possouris):

            if self.player_name_rect.collidepoint(possouris):
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                surface.blit(self.player_name_hover, (0, 0))
            elif self.buttons.is_hovering_button(possouris):
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif not self.buttons.is_hovering_button(possouris):
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        else:
            if self.ingame_window.is_hovering_buttons(possouris):
                if not pygame.mouse.get_cursor() == pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                if not pygame.mouse.get_cursor() == pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if self.change_player_name_mode:
            surface.blit(self.mode_changement_pseudo_image, (0, 0))
            self.curseur_changement_pseudo.update(surface, self.calcul_player_name_pixels())

        self.ingame_window.update(surface, possouris)

    def update_player_name(self, current_player_name):
        if not self.player_name == current_player_name:
            self.player_name = current_player_name
            self.player_name_image = self.font.render(self.player_name, False, (15, 0, 124))

    def update_player_lv(self):
        self.player_lv_image = self.font_size3.render(str(self.player.level), False, (124, 124, 124))

    def calcul_player_name_pixels(self):
        pixels = 0
        for c in self.player_name:
            pixels += self.alphabet_pixels[c]
            pixels += 5

        return pixels

    def def_alphabet_pixels(self, alphabet_pixels):
        self.alphabet_pixels = alphabet_pixels
