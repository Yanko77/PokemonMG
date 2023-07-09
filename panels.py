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
        self.is_pname_modif = False
        self.change_player_name_mode = False

        self.background = pygame.image.load('assets/game/panels/classic_panel/background.png')
        self.mode_changement_pseudo_image = pygame.image.load('assets/game/panels/classic_panel/'
                                                              'mode_changement_pseudo.png')
        self.curseur_changement_pseudo = image.CursorChangePseudoMode()

        self.font = pygame.font.Font('assets/fonts/impact.ttf', 50)
        self.font_size2 = pygame.font.Font('assets/fonts/impact.ttf', 25)
        self.font_size3 = pygame.font.Font('assets/fonts/(Unranked) Bdeogale.ttf', 70)

        self.pokemon_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 25)
        self.pokemon_level_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 15)
        self.pokemon_hp_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 18)

        self.player = player
        self.player_name = self.player.name

        self.player_name_image = self.font.render(self.player_name, False, (15, 0, 124))
        self.player_name_indication = self.font_size2.render("(cliquer pour modifier)", False, (15, 0, 124))
        self.player_lv_image = self.font_size3.render(str(self.player.level), False, (124, 124, 124))

        self.player_name_rect = pygame.Rect(656, 12, 399, 51)
        self.player_name_hover = pygame.image.load("assets/game/panels/classic_panel/player_name_hover.png")

        self.alphabet_pixels = {}

        self.current_ig_window_name = 'Starters'
        self.ingame_window = ingame_windows.IngameWindow(self.current_ig_window_name)

        self.buttons = image.ClassicGamePanelButtons()

    def update(self, surface, possouris):

        surface.blit(self.background, (0, 0))
        surface.blit(self.font.render(self.player.name, False, (15, 0, 124)), (662, 10))
        if self.change_player_name_mode:
            self.curseur_changement_pseudo.update(surface, self.calcul_player_name_pixels())
        if not self.is_pname_modif:
            surface.blit(self.player_name_indication, (760, 30))

        if self.player.level >= 10:
            surface.blit(self.player_lv_image, (955, 73))
        else:
            surface.blit(self.player_lv_image, (965, 73))

        self.update_team_pokemons(surface)
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
            if self.ingame_window.is_minimized:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.ingame_window.is_open:
                if self.ingame_window.is_hovering_buttons(possouris):
                    if not pygame.mouse.get_cursor() == pygame.SYSTEM_CURSOR_HAND:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    if not pygame.mouse.get_cursor() == pygame.SYSTEM_CURSOR_ARROW:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if self.change_player_name_mode:
            surface.blit(self.mode_changement_pseudo_image, (0, 0))

        self.ingame_window.update(surface, possouris)

    def update_player_name(self, current_player_name):
        if not self.player_name == current_player_name:
            self.player_name = current_player_name

    def update_player_lv(self):
        self.player_lv_image = self.font_size3.render(str(self.player.level), False, (124, 124, 124))

    def update_team_pokemons(self, surface):
        # Pokemon 1
        if self.player.team[0] is not None:
            surface.blit(self.player.team[0].icon_image, (900, 270), (0, 0, 64, 64))
            surface.blit(self.pokemon_name_font.render(self.player.team[0].name, False, (0, 0, 0)), (970, 288))
            surface.blit(self.pokemon_level_font.render('Lv.' + str(self.player.team[0].level), False, (0, 0, 0)), (960, 317))
            pygame.draw.rect(surface, (35, 35, 35), pygame.Rect(1100, 301, 150, 17))
            pygame.draw.rect(surface, (42, 214, 0), pygame.Rect(1100, 301, self.player.team[0].health/self.player.team[0].pv*150, 17))
            surface.blit(self.pokemon_hp_font.render(str(self.player.team[0].health) + "/" + str(self.player.team[0].pv), False, (0, 0, 0)), (1100, 315))

        # Pokemon 2 ( +73px )
        if self.player.team[1] is not None:
            surface.blit(self.player.team[1].icon_image, (900, 343), (0, 0, 64, 64))
            surface.blit(self.pokemon_name_font.render(self.player.team[1].name, False, (0, 0, 0)), (970, 361))
            surface.blit(self.pokemon_level_font.render('Lv.' + str(self.player.team[1].level), False, (0, 0, 0)), (960, 390))
            pygame.draw.rect(surface, (35, 35, 35), pygame.Rect(1100, 374, 150, 17))
            pygame.draw.rect(surface, (42, 214, 0), pygame.Rect(1100, 374, self.player.team[1].health / self.player.team[1].pv * 150, 17))
            surface.blit(self.pokemon_hp_font.render(str(self.player.team[1].health) + "/" + str(self.player.team[1].pv), False, (0, 0, 0)), (1100, 388))

        # Pokemon 3 ( +73px )
        if self.player.team[2] is not None:
            surface.blit(self.pokemon_name_font.render(self.player.team[2].name, False, (0, 0, 0)), (970, 434))
            surface.blit(self.pokemon_level_font.render('Lv.' + str(self.player.team[2].level), False, (0, 0, 0)), (960, 463))
            pygame.draw.rect(surface, (35, 35, 35), pygame.Rect(1100, 447, 150, 17))
            pygame.draw.rect(surface, (42, 214, 0), pygame.Rect(1100, 447, self.player.team[2].health / self.player.team[2].pv * 150, 17))
            surface.blit(
                self.pokemon_hp_font.render(str(self.player.team[2].health) + "/" + str(self.player.team[2].pv), False, (0, 0, 0)), (1100, 461))

        # Pokemon 4 ( +73px )
        if self.player.team[3] is not None:
            surface.blit(self.pokemon_name_font.render(self.player.team[3].name, False, (0, 0, 0)), (970, 507))
            surface.blit(self.pokemon_level_font.render('Lv.' + str(self.player.team[3].level), False, (0, 0, 0)), (960, 536))
            pygame.draw.rect(surface, (35, 35, 35), pygame.Rect(1100, 520, 150, 17))
            pygame.draw.rect(surface, (42, 214, 0), pygame.Rect(1100, 520, self.player.team[3].health / self.player.team[3].pv * 150, 17))
            surface.blit(
                self.pokemon_hp_font.render(str(self.player.team[3].health) + "/" + str(self.player.team[3].pv), False, (0, 0, 0)), (1100, 534))

        # Pokemon 5 ( +73px )
        if self.player.team[4] is not None:
            surface.blit(self.pokemon_name_font.render(self.player.team[4].name, False, (0, 0, 0)), (970, 580))
            surface.blit(self.pokemon_level_font.render('Lv.' + str(self.player.team[4].level), False, (0, 0, 0)), (960, 609))
            pygame.draw.rect(surface, (35, 35, 35), pygame.Rect(1100, 593, 150, 17))
            pygame.draw.rect(surface, (42, 214, 0), pygame.Rect(1100, 593, self.player.team[4].health / self.player.team[4].pv * 150, 17))
            surface.blit( self.pokemon_hp_font.render(str(self.player.team[4].health) + "/" + str(self.player.team[4].pv), False, (0, 0, 0)), (1100, 607))

        # Pokemon 6 ( +73px )
        if self.player.team[5] is not None:
            surface.blit(self.pokemon_name_font.render(self.player.team[5].name, False, (0, 0, 0)), (970, 653))
            surface.blit(self.pokemon_level_font.render('Lv.' + str(self.player.team[5].level), False, (0, 0, 0)), (960, 682))
            pygame.draw.rect(surface, (35, 35, 35), pygame.Rect(1100, 666, 150, 17))
            pygame.draw.rect(surface, (42, 214, 0), pygame.Rect(1100, 666, self.player.team[5].health / self.player.team[5].pv * 150, 17))
            surface.blit(self.pokemon_hp_font.render(str(self.player.team[5].health) + "/" + str(self.player.team[5].pv), False, (0, 0, 0)), (1100, 680))

    def calcul_player_name_pixels(self):
        pixels = 0
        for c in self.player_name:
            pixels += self.alphabet_pixels[c]
            pixels += 5

        return pixels

    def def_alphabet_pixels(self, alphabet_pixels):
        self.alphabet_pixels = alphabet_pixels
