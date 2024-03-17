import pygame
import pokemon


class StarterPanel:

    def __init__(self, game):
        self.game = game
        self.PATH = 'assets/game/panels/starter_panel/'

        # Chargement des fonts
        self.pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 30)

        # Chargement des images
        self.background = self.img_load('background').convert_alpha()

        self.aide_button = self.img_load('aide_button').convert_alpha()
        self.aide_button_rect = pygame.Rect(1213, 11, 55, 55)

        self.aide_popup = self.img_load('aide_popup')
        self.aide_popup_rect = pygame.Rect(586, 11, 624, 95)

        self.dresseur = self.img_load('maitre_dresseur').convert_alpha()
        self.dresseur_rect = pygame.Rect(845, 85, 411, 635)

        self.drop_pk_emp = self.img_load('drop_pk_emp')
        self.drop_pk_emp_rect = pygame.Rect(1017, 460, 248, 248)

        self.text_box = self.img_load('text_box').convert_alpha()
        self.text_box_rect = pygame.Rect(49, 519, 1102, 176)
        self.text1 = self.img_load('text1').convert_alpha()
        self.text2 = self.img_load('text2').convert_alpha()

        self.skip_intro_button = self.img_load('skip_intro_button')
        self.skip_intro_button_rect = pygame.Rect(992, 642, 253, 43)

        self.pk_emps = self.img_load('pk_emps').convert_alpha()
        self.pk_emps_rects = [
            pygame.Rect(43, 69, 284, 284),
            pygame.Rect(359, 69, 284, 284),
            pygame.Rect(676, 69, 284, 284),
        ]

        self.pokeball = self.img_load('pokeball').convert_alpha()

        self.pokemons = [pokemon.Pokemon(pk, 5, self.game) for pk in self.game.starters]
        self.pk_icons = [pygame.transform.scale(pk.get_icon(), (580, 290)) for pk in self.pokemons]
        self.pk_names = [self.pk_name_font.render(pk.get_name(), False, (255, 255, 255)) for pk in self.pokemons]

        # Variables d'animation
        self.compteur = 0

        # Variables de gestion d'interaction
        self.pk_move_mode = False
        self.pk_moving = None
        self.moving_pk_rel_possouris = (0, 0)

        # Variables de jeu
        self.discovered_pks = [
            False,
            False,
            False
        ]

    def update(self, surface, possouris):
        self.update_animations()

        surface.blit(self.background, (0, 0))

        self.update_text_box(surface)

        if self.pk_move_mode:
            self.update_dresseur(surface)
            self.update_drop_pk_emp(surface, possouris)
            self.update_pk_emps(surface, possouris)
        else:
            self.update_pk_emps(surface, possouris)
            self.update_dresseur(surface)
            self.update_drop_pk_emp(surface, possouris)

        self.update_intro_skip_button(surface, possouris)

        self.update_aide_button(surface, possouris)

        if self.compteur < 860:
            self.compteur += 1

        # Actualiser le curseur
        if self.is_hovering_buttons(possouris):
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update_animations(self):
        if self.compteur < 255:
            self.background.set_alpha(self.compteur)
        if self.compteur < 300:
            self.dresseur.set_alpha(round((self.compteur - 255)*5.8))
        if self.compteur < 320:
            self.text_box.set_alpha(round((self.compteur - 280)*6.375))
        if self.compteur < 350:
            self.text1.set_alpha(round((self.compteur - 300)*5.1))
        if 525 < self.compteur < 575:
            self.text1.set_alpha(round((575 - self.compteur) * 5.1))
        if self.compteur < 630:
            self.text2.set_alpha(round((self.compteur - 580) * 5.1))
        if self.compteur < 750:
            self.pk_emps.set_alpha(round((self.compteur - 680) * 3.66))
        if self.compteur < 800:
            self.pokeball.set_alpha(round((self.compteur - 780) * 12.75))
        if self.compteur < 850:
            self.drop_pk_emp.set_alpha(round((self.compteur - 830) * 12.75))
            self.aide_button.set_alpha(round((self.compteur - 830) * 12.75))

    def update_pk_emps(self, surface, possouris):
        surface.blit(self.pk_emps, self.pk_emps_rects[0])

        for i in range(3):
            self.update_pokemon(surface, possouris, i)

    def update_pokemon(self, surface, possouris, i):
        if not self.discovered_pks[i]:
            if self.pk_emps_rects[i].collidepoint(possouris) and self.compteur > 800:
                surface.blit(self.create_rect_alpha((274, 266), (255, 255, 255), 50),
                             (self.pk_emps_rects[i].x + 5, self.pk_emps_rects[i].y + 5))

                rect_contour = pygame.Surface((274, 266), pygame.SRCALPHA)
                pygame.draw.rect(rect_contour, (200, 200, 200), rect_contour.get_rect(), width=5)

                surface.blit(rect_contour,
                             (self.pk_emps_rects[i].x + 5, self.pk_emps_rects[i].y + 5))

            surface.blit(self.pokeball, self.pk_emps_rects[i])
        else:
            if self.pk_move_mode and self.pk_moving == i:
                pk_rect = pygame.Rect(possouris[0] - self.moving_pk_rel_possouris[0],
                                      possouris[1] - self.moving_pk_rel_possouris[1],
                                      290,
                                      292)

            else:
                pk_rect = self.pk_emps_rects[i].copy()

            surface.blit(self.pk_names[i], ((self.pk_emps_rects[i].w - self.pk_names[i].get_width())/2 + self.pk_emps_rects[i].x,
                                            365))

            if pk_rect.collidepoint(possouris):
                surface.blit(self.create_rect_alpha((240, 240), (255, 255, 255)), (pk_rect.x + 20, pk_rect.y + 20))

            if self.pk_move_mode and self.pk_moving == i:
                rect_contour = pygame.Surface((240, 240), pygame.SRCALPHA)
                pygame.draw.rect(rect_contour, (200, 200, 200), rect_contour.get_rect(), width=5)
                surface.blit(rect_contour, (pk_rect.x + 20, pk_rect.y + 20))

            surface.blit(self.pk_icons[i], (pk_rect.x, pk_rect.y - 20), (0, 0, 290, 290))

            if not self.pk_move_mode:
                if self.game.mouse_pressed[1] and pk_rect.collidepoint(possouris):
                    self.pk_move_mode = True
                    self.pk_moving = i
                    self.moving_pk_rel_possouris = (possouris[0] - pk_rect.x,
                                                    possouris[1] - pk_rect.y)
            else:
                if not self.game.mouse_pressed[1]:
                    if self.drop_pk_emp_rect.collidepoint(possouris):
                        self.game.player.add_team_pk(self.pokemons[self.pk_moving])
                        self.game.is_starter_selected = True

                    self.pk_moving = None
                    self.pk_move_mode = False

    def update_drop_pk_emp(self, surface, possouris):
        if self.pk_move_mode and self.drop_pk_emp_rect.collidepoint(possouris):
            surface.blit(self.drop_pk_emp, self.drop_pk_emp_rect, (248, 0, 248, 248))
        else:
            surface.blit(self.drop_pk_emp, self.drop_pk_emp_rect, (0, 0, 248, 248))

    def update_aide_button(self, surface, possouris):

        if self.aide_button_rect.collidepoint(possouris) and self.compteur > 850:
            surface.blit(self.aide_button, self.aide_button_rect, (55, 0, 55, 55))
            surface.blit(self.aide_popup, self.aide_popup_rect)
        else:
            surface.blit(self.aide_button, self.aide_button_rect, (0, 0, 55, 55))

    def update_text_box(self, surface):
        surface.blit(self.text_box, self.text_box_rect)

        surface.blit(self.text1, self.text_box_rect)

        surface.blit(self.text2, self.text_box_rect)

    def update_dresseur(self, surface):
        x = self.dresseur_rect.x + 300*1.2 + 50 - self.compteur*1.2
        if x < self.dresseur_rect.x:
            x = self.dresseur_rect.x

        y = self.dresseur_rect.y

        surface.blit(self.dresseur, (x, y))

    def update_intro_skip_button(self, surface, possouris):
        if 800 > self.compteur > 100:

            if self.skip_intro_button_rect.collidepoint(possouris):
                surface.blit(self.skip_intro_button, self.skip_intro_button_rect, (253, 0, 253, 43))
            else:
                surface.blit(self.skip_intro_button, self.skip_intro_button_rect, (0, 0, 253, 43))

    def skip_intro(self):
        self.compteur = 800
        self.background.set_alpha(255)
        self.pk_emps.set_alpha(255)
        self.dresseur.set_alpha(255)
        self.text_box.set_alpha(255)
        self.text1.set_alpha(0)
        self.text2.set_alpha(255)
        self.pokeball.set_alpha(255)
        self.drop_pk_emp.set_alpha(255)

    def is_hovering_buttons(self, possouris):
        if 850 > self.compteur > 100:
            if self.skip_intro_button_rect.collidepoint(possouris):
                return True
        elif self.compteur > 850:
            if self.aide_button_rect.collidepoint(possouris):
                return True
            elif self.pk_move_mode:
                return True
            else:
                for pk_rect in self.pk_emps_rects:
                    if pk_rect.collidepoint(possouris):
                        return True
        return False

    def left_clic_interactions(self, possouris):
        if self.compteur > 800:
            i = 0
            for rect in self.pk_emps_rects:
                if not self.discovered_pks[i]:
                    if rect.collidepoint(possouris):
                        self.discovered_pks[i] = True
                i += 1
        elif self.compteur > 100:
            if self.skip_intro_button_rect.collidepoint(possouris):
                self.skip_intro()

    def create_rect_alpha(self, dimensions, color, alpha=90):
        rect = pygame.Surface(dimensions)
        rect.set_alpha(alpha)
        rect.fill(color)
        return rect

    def img_load(self, file_path):
        return pygame.image.load(f'{self.PATH}{file_path}.png')


if __name__ == '__main__':

    FPS = 144
    screen = pygame.display.set_mode((1280, 720))
    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_caption("PMG || Pokemon Management Game")
    pygame.display.set_icon(icon)

    starter = StarterPanel(None)
    clock = pygame.time.Clock()

    running = True

    while running:
        posSouris = list(pygame.mouse.get_pos())

        starter.update(screen, posSouris)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                starter.left_clic_interactions(posSouris)

        clock.tick(FPS)

pygame.quit()