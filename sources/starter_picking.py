import pygame
import random

from panel import Panel
from pokemon import Pokemon
from font import Font


POKEMON_NAME_FONT = Font("Oswald-Regular.ttf", 30)


STARTERS_LIST = {
    'plante': ['Bulbizarre', 'Arcko'],
    'feu': ['Salameche', 'Poussifeu'],
    'eau': ['Carapuce', 'Gobou']
}


class StarterPicking(Panel):

    def __init__(self, game):
        super().__init__(game=game,
                         path='assets/game/panels/starter_panel/')

        self.intro = Intro(self.game)

        self.starters = [
            Pokemon(
                name=random.choice(STARTERS_LIST[pk_type]),
                level=5,
                game=self.game
            )
            for pk_type in ('plante', 'feu', 'eau')
        ]

        self.pokeball_emps = PokeballEmps(self)

        self.drop_emp = self.img_load("drop_pk_emp")
        self.drop_rect = pygame.Rect(1017, 460, 248, 248)

        self.help_popup = HelpPopup(self)

    @property
    def is_intro(self):
        return self.intro.is_animating

    def update(self, possouris):
        self.intro.update(possouris)

        if not self.is_intro:
            self.display_drop_emp(self.game.screen)

            self.pokeball_emps.update(possouris)

            self.help_popup.update(possouris)

    def display_drop_emp(self, screen):
        if self.drop_rect.collidelist(self.pokeball_emps.emps_rect_list) != -1:
            screen.blit(self.drop_emp, self.drop_rect, (248, 0, 248, 248))
        else:
            screen.blit(self.drop_emp, self.drop_rect, (0, 0, 248, 248))

    def pick_starter(self, pokemon):
        self.game.player.team.add(pokemon)
        self.game.is_picking_starter = False
        self.game.is_playing = True

    def is_hovering_buttons(self, possouris):
        return self.intro.is_hovering_buttons(possouris) or \
               self.help_popup.is_hovering(possouris) or \
               self.pokeball_emps.is_hovering(possouris)

    def left_clic_interactions(self, possouris):
        if self.is_intro:
            self.intro.left_clic_interactions(possouris)
        else:
            self.pokeball_emps.left_clic_interactions(possouris)


class Intro(Panel):

    def __init__(self, game):
        super().__init__(game=game,
                         path='assets/game/panels/starter_panel/')

        self.background = Background(self)

        self.dresseur = Dresseur(self)

        self.text_box = TextBox(self)

        self.skip_button = SkipIntroButton(self)

        self.compteur = 0

    @property
    def is_animating(self):
        return self.compteur < 850

    def skip_animation(self):
        self.compteur = 850
        self.dresseur.skip_animation()
        self.text_box.skip_animation()

    def update(self, possouris):
        self.background.update()
        self.text_box.update()
        self.dresseur.update()
        self.skip_button.update(possouris)

        if self.is_animating:
            self.update_animations()

    def update_animations(self):
        self.compteur += 1

    def is_hovering_buttons(self, possouris):
        return self.skip_button.is_hovering(possouris)

    def left_clic_interactions(self, possouris):
        if self.skip_button.rect.collidepoint(possouris):
            self.skip_animation()


class Background:

    def __init__(self, panel):
        self.panel: Intro = panel

        self.image = self.panel.img_load('background')
        self.image.set_alpha(0)

    @property
    def alpha(self):
        return self.panel.compteur

    @property
    def is_fading(self):
        return self.image.get_alpha() < 255

    def skip_animation(self):
        self.image.set_alpha(255)

    def update(self):
        if self.is_fading:
            self.image.set_alpha(self.alpha)

        self.panel.game.screen.blit(self.image, (0, 0))


class Dresseur:

    def __init__(self, panel):
        self.panel: Intro = panel

        self.image = panel.img_load('maitre_dresseur')
        self.rect = pygame.Rect(845 + 410, 85, 411, 635)

        self.image.set_alpha(0)

    @property
    def is_fading(self):
        return self.image.get_alpha() < 255

    @property
    def is_moving(self):
        return self.rect.x > 845

    @property
    def alpha(self):
        return round(self.panel.compteur - 255) * 5.8

    def skip_animation(self):
        self.image.set_alpha(255)
        self.rect.x = 845

    def update(self):

        # Alpha
        if self.is_fading:
            self.image.set_alpha(self.alpha)

        # Pos
        if self.is_moving:
            self.rect.x -= 1.4

        self.panel.game.screen.blit(self.image, self.rect)


class TextBox:

    def __init__(self, panel):
        self.panel: Intro = panel

        self.box = self.panel.img_load('text_box')
        self.box_rect = pygame.Rect(49, 519, 1102, 176)

        self.text1 = self.panel.img_load('text1')
        self.text2 = self.panel.img_load('text2')

        self.box.set_alpha(0)
        self.text1.set_alpha(0)
        self.text2.set_alpha(0)

    @property
    def box_alpha(self):
        return round((self.panel.compteur - 280) * 6.375)
    
    @property
    def text1_alpha_in(self):
        return round((self.panel.compteur - 300) * 5.1)

    @property
    def text1_alpha_out(self):
        return round((575 - self.panel.compteur) * 5.1)

    @property
    def text2_alpha(self):
        return round((self.panel.compteur - 580) * 5.1)
    
    @property
    def is_box_fading(self):
        return self.panel.compteur > 280 and self.box.get_alpha() < 255
    
    @property
    def is_text1_fading_in(self):
        return 280 < self.panel.compteur < 525 and self.text1.get_alpha() < 255

    @property
    def is_text1_fading_out(self):
        return self.panel.compteur > 525 and self.text1.get_alpha() > 0
    
    @property
    def is_text2_fading(self):
        return self.panel.compteur > 580

    def skip_animation(self):
        self.box.set_alpha(255)
        self.text2.set_alpha(255)
    
    def update(self):
        if self.is_box_fading:
            self.box.set_alpha(self.box_alpha)

        if self.is_text1_fading_in:
            self.text1.set_alpha(self.text1_alpha_in)

        if self.is_text1_fading_out:
            self.text1.set_alpha(self.text1_alpha_out)

        if self.is_text2_fading:
            self.text2.set_alpha(self.text2_alpha)

        self.panel.game.screen.blit(self.box, self.box_rect)
        self.panel.game.screen.blit(self.text1, self.box_rect)
        self.panel.game.screen.blit(self.text2, self.box_rect)


class HelpPopup:

    def __init__(self, panel):
        self.panel: Intro = panel

        self.button = self.panel.img_load('aide_button')
        self.button_rect = pygame.Rect(1213, 11, 55, 55)

        self.popup = self.panel.img_load('aide_popup')
        self.popup_rect = pygame.Rect(586, 11, 624, 95)

    def update(self, possouris):
        if self.button_rect.collidepoint(possouris):
            self.panel.game.screen.blit(self.button, self.button_rect, (55, 0, 55, 55))
            self.panel.game.screen.blit(self.popup, self.popup_rect)
        else:
            self.panel.game.screen.blit(self.button, self.button_rect, (0, 0, 55, 55))

    def is_hovering(self, possouris):
        return self.button_rect.collidepoint(possouris) and not self.panel.is_intro


class SkipIntroButton:

    def __init__(self, panel):
        self.panel: Intro = panel

        self.image = self.panel.img_load('skip_intro_button')
        self.rect = pygame.Rect(992, 642, 253, 43)

        self.image.set_alpha(0)
        self.fading_speed = 5

    @property
    def is_fading(self):
        return self.image.get_alpha() < 255 and self.panel.compteur > 450

    @property
    def is_working(self):
        return self.panel.is_animating and self.panel.compteur > 475

    def update(self, possouris):
        if self.panel.is_animating:
            if self.rect.collidepoint(possouris):
                self.panel.game.screen.blit(self.image, self.rect, (253, 0, 253, 43))
            else:
                self.panel.game.screen.blit(self.image, self.rect, (0, 0, 253, 43))

            if self.is_fading:
                self.fade()

    def fade(self):
        self.image.set_alpha(self.image.get_alpha() + self.fading_speed)

    def is_hovering(self, possouris):
        return self.rect.collidepoint(possouris) and self.is_working


class PokeballEmps:

    def __init__(self, panel):
        self.panel: StarterPicking = panel

        self.image = self.panel.img_load('pk_emps')
        self.rect = pygame.Rect(43, 69, 284 * 3, 284 * 3)

        self.pk_emps = [
            PokemonEmp(self, 43, self.panel.starters[0]),
            PokemonEmp(self, 359, self.panel.starters[1]),
            PokemonEmp(self, 676, self.panel.starters[2])
        ]

    @property
    def is_emp_moving(self):
        for emp in self.pk_emps:
            if emp.is_moving:
                return True
        return False

    @property
    def emps_rect_list(self):
        return [emp.rect for emp in self.pk_emps]

    def update(self, possouris):
        self.panel.game.screen.blit(self.image, self.rect)

        for emp in self.pk_emps:
            emp.update(possouris)

    def is_hovering(self, possouris):
        for emp in self.pk_emps:
            if emp.is_hovering(possouris):
                return True

        return False

    def left_clic_interactions(self, possouris):
        for emp in self.pk_emps:
            emp.left_clic_interactions(possouris)


class PokemonEmp:

    def __init__(self, group, pos_x, pokemon):
        self.group: PokeballEmps = group

        self.RECT = pygame.Rect(pos_x, 69, 284, 284)
        self.rect = pygame.Rect.copy(self.RECT)

        self.pokeball = self.group.panel.img_load('pokeball')

        self.hover_rect = HoverRect(self)

        self.pokemon = pokemon
        self.pokemon_icon = self.pokemon.get_icon((290, 290))
        self.pokemon_name = POKEMON_NAME_FONT.render(self.pokemon.name)
        self.pokemon_name_rect = (self.rect.x + (self.rect.w - self.pokemon_name.get_width()) / 2,
                                  365,
                                  284,
                                  40)

        self.saved_moving_possouris = (0, 0)

        self.is_discovered = False
        self.is_moving = False

    @property
    def pokemon_icon_rect(self):
        return pygame.Rect(self.rect.x,
                           self.rect.y - 20,
                           290,
                           290)

    def discover(self):
        self.is_discovered = True

    def update(self, possouris):
        screen = self.group.panel.game.screen

        self.check_moving(possouris)

        if self.is_moving:
            self.move(possouris)

        self.hover_rect.update(possouris)

        if not self.is_discovered:
            self.display_pokeball(screen)
        else:
            self.display_pokemon(screen)

    def display_pokemon(self, screen):
        screen.blit(self.pokemon_icon, self.pokemon_icon_rect)
        screen.blit(self.pokemon_name, self.pokemon_name_rect)

    def display_pokeball(self, screen):
        screen.blit(self.pokeball, self.rect)

    def check_moving(self, possouris):
        game = self.group.panel.game

        if not self.is_moving:
            if game.mouse_pressed[1] and self.rect.collidepoint(possouris):
                if not self.group.is_emp_moving:
                    self.is_moving = True
                    self.saved_moving_possouris = (possouris[0] - self.RECT.x, possouris[1] - self.RECT.y)

        else:
            if not game.mouse_pressed[1]:
                self.is_moving = False

                if self.rect.colliderect(self.group.panel.drop_rect):
                    self.group.panel.pick_starter(self.pokemon)
                else:
                    self.reset_rect()

    def move(self, possouris):
        self.rect.topleft = (
            possouris[0] - self.saved_moving_possouris[0],
            possouris[1] - self.saved_moving_possouris[1]
        )

    def reset_rect(self):
        self.rect = pygame.Rect.copy(self.RECT)

    def is_hovering(self, possouris):
        return self.rect.collidepoint(possouris) and not self.group.panel.is_intro

    def left_clic_interactions(self, possouris):
        if self.rect.collidepoint(possouris):
            self.discover()


class HoverRect:

    def __init__(self, emp):
        self.emp: PokemonEmp = emp

        self.rect_image = self.emp.group.panel.create_rect_alpha(
            (
                self.emp.rect.w - 30,
                self.emp.rect.h - 30
            ),
            (255, 255, 255),
            alpha=50
        )

    def update(self, possouris):
        if self.emp.rect.collidepoint(possouris):
            self.emp.group.panel.game.screen.blit(
                self.rect_image,
                (self.emp.rect.x + 15, self.emp.rect.y + 15)
                )
