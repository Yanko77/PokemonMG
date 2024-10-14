from panel import Panel


class StatersPanel(Panel):

    def __init__(self, game):
        super().__init__(game=game,
                         path='assets/game/panels/starter_panel/')

        # Chargement des fonts
        self.pk_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 30)

        # Chargement des images
        self.background = self.img_load('background')

        self.aide_button = self.img_load('aide_button')
        self.aide_button_rect = pygame.Rect(1213, 11, 624, 95)

        self.aide_popup = self.img_load('aide_popup')
        self.aide_popup_rect = pygame.Rect(586, 11, 624, 95)

        self.dresseur = self.img_load('maitre_dresseur')
        self.dresseur_rect = pygame.Rect(845, 85, 411, 635)

        self.drop_pk_emp = self.img_load('drop_pk_emp')
        self.drop_pk_emp_rect = pygame.Rect(1017, 460, 248, 248)

        self.text_box = self.img_load('text_box')
        self.text_box_rect = pygame.Rect(49, 519, 1102, 176)
        self.text1 = self.img_load('text1')
        self.text2 = self.img_load('text2')

        self.skip_intro_button = self.img_load('skip_intro_button')
        self.skip_intro_button_rect = pygame.Rect(992, 642, 253, 43)

        self.pk_emps = self.img_load('pk_emps')
        self.pk_emps_rects = [
            pygame.Rect(43, 69, 284, 284),
            pygame.Rect(359, 69, 284, 284),
            pygame.Rect(676, 69, 284, 284),
        ]

        self.pokeball = self.img_load('pokeball')

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

    def update(self, possouris):

        self.game.screen.blit()

    def update_animations(self):

        self.compteur += 1


class StartersPanelIntro(Panel):

    def __init__(self, game):
        super().__init__(game=game,
                         path='assets/game/panels/starter_panel/')

        self.background = self.img_load('background')

        self.dresseur = self.img_load('maitre_dresseur')
        self.dresseur_rect = pygame.Rect(845, 85, 411, 635)

        self.text_box = self.img_load('text_box')
        self.text_box_rect = pygame.Rect(49, 519, 1102, 176)
        self.text1 = self.img_load('text1')
        self.text2 = self.img_load('text2')

        self.skip_intro_button = self.img_load('skip_intro_button')
        self.skip_intro_button_rect = pygame.Rect(992, 642, 253, 43)

        self.compteur = 0