"""
Fichier gérant l'action Spawn du jeu.
"""

# Importation des modules
import pygame
import random

import pokemon
import objet


# Définition des classes
class SpawnPanel:
    """
    Classe représentant le panel d'action "Spawn".

    Dans ce panel, le joueur pourra :
    - Faire apparaître un pokémon en utilisant 1 action.
    - Capturer un pokémon apparu en utilisant une Pokéball de son sac.
    """
    def __init__(self, game, window):
        self.game = game
        self.window = window

        # Constantes
        self.PATH = 'assets/game/ingame_windows/Spawn/'
        
        self.min_spawning_pk_level = 2
        self.max_spawning_pk_level = 5
        self.spawning_pk_level_bonus = 0

        # Chargement des fonts
        self.infos_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 30)
        self.spawning_pk_level_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 25)

        # Chargement des images
        self.background = self.img_load('background')

        #
        self.button_aide = self.img_load('aide_button')
        self.button_aide_hover = self.img_load('aide_button_hover')
        self.button_aide_rect = self.button_aide.get_rect()
        self.button_aide_rect.x = 838
        self.button_aide_rect.y = 46

        self.aide_popup = self.img_load('aide_popup')

        #
        self.spawn_button = self.img_load('spawn_button')
        self.spawn_button_rect = self.spawn_button.get_rect()
        self.spawn_button_rect.x = 397
        self.spawn_button_rect.y = 312
        self.spawn_button_hover = self.img_load('spawn_button_hover')
        self.spawn_popup = self.img_load('spawn_popup')
        self.spawn_popup_lock = self.img_load('spawn_popup_lock')
        self.spawn_button_lock = self.img_load('spawn_button_lock')

        #
        self.catch_button = self.img_load('catch_button')
        self.catch_button_rect = self.catch_button.get_rect()
        self.catch_button_rect.x = 397
        self.catch_button_rect.y = 216
        self.catch_button_hover = self.img_load('catch_button_hover')
        self.catch_popup = self.img_load('catch_popup')
        self.catch_button_lock = self.img_load('catch_button_lock')
        self.catch_popup_lock = self.img_load('catch_popup_lock')

        #
        self.spawning_levels_button = self.img_load('spawning_levels_button')
        self.spawning_levels_button_rect = self.spawning_levels_button.get_rect()
        self.spawning_levels_button_rect.x = 32
        self.spawning_levels_button_rect.y = 102
        self.spawning_levels_button_hover = self.img_load('spawning_levels_button_hover')
        self.spawning_levels_popup = self.img_load('spawning_levels_popup')

        #
        self.spawning_pk_lock = self.img_load('locked')
        self.spawning_pk_hover = self.img_load('spawning_pk_hover')
        self.spawning_pk_rect = pygame.Rect(104, 117, 267, 267)
        self.SPAWNING_PK_RECT = pygame.Rect(104, 117, 267, 267)  # Version invariable du rect (utilisée comme backup)
        self.spawning_pk_hover_lock = self.img_load('spawning_pk_hover_lock')

        #
        self.spawn_confirm = self.img_load('confirm')
        self.spawn_confirm_rect = self.spawn_confirm.get_rect()
        self.spawn_confirm_rect.x = 391
        self.spawn_confirm_rect.y = 311
        self.spawn_confirm_hover = self.img_load('confirm_hover')
        self.spawn_confirm_popup_rect = pygame.Rect(398, 314, 338, 92)

        #
        self.catch_confirm = self.img_load('confirm')
        self.catch_confirm_rect = self.catch_confirm.get_rect()
        self.catch_confirm_rect.x = 391
        self.catch_confirm_rect.y = 214
        self.catch_confirm_hover = self.img_load('confirm_hover')
        self.catch_confirm_popup_rect = pygame.Rect(398, 217, 338, 92)

        # Initialisation des variables
        self.is_spawning_pk_lock = True
        self.spawning_pk = None

        self.spawning_pk_move_mode = False
        self.possouris_rel = [0, 0]  # Position relative de la souris par rapport au rect du pokémon lorsqu'il sera amené à bouger.
        self.saved_possouris = [0, 0]  # Position sauvegardée de la position de la souris lorsque le pokémon sera amené à bouger.

        self.boolspawn_confirm = False
        self.boolcatch_confirm = False

    # Méthodes liées à l'affichage

    def update(self, surface: pygame.Surface, possouris: list):
        """
        Méthode d'actualisation de l'affichage du panel Spawn.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        @in : window_pos, list → coordonnées de la fenêtre ingame
        """
        window_pos = self.window.basic_window_pos

        self.update_rect_pos(window_pos)
        self.update_spawning_pk_level()

        surface.blit(self.background, (window_pos[0] - 13, window_pos[1] - 21))

        if self.button_aide_rect.collidepoint(possouris):
            surface.blit(self.button_aide_hover, self.button_aide_rect)
            surface.blit(self.aide_popup, (492 + window_pos[0], 46 + window_pos[1]))
        else:
            surface.blit(self.button_aide, self.button_aide_rect)

        if self.spawn_button_rect.collidepoint(possouris):
            if self.boolspawn_confirm:
                surface.blit(self.spawn_confirm_hover, self.spawn_confirm_rect)
            else:
                if not self.spawning_pk_move_mode:
                    if self.game.player.actions > 0:
                        surface.blit(self.spawn_button_hover, self.spawn_button_rect)
                        surface.blit(self.spawn_popup, (507 + window_pos[0], 316 + window_pos[1]))
                    else:
                        surface.blit(self.spawn_button_lock, self.spawn_button_rect)
                        surface.blit(self.spawn_popup_lock, (507 + window_pos[0], 316 + window_pos[1]))
                else:
                    surface.blit(self.spawn_button_lock, self.spawn_button_rect)
        else:
            if self.boolspawn_confirm:
                surface.blit(self.spawn_confirm, self.spawn_confirm_rect)
                if not self.spawn_confirm_popup_rect.collidepoint(possouris):
                    self.boolspawn_confirm = False
            else:
                surface.blit(self.spawn_button, self.spawn_button_rect)

        if self.catch_button_rect.collidepoint(possouris):
            if self.boolcatch_confirm:
                surface.blit(self.catch_confirm_hover, self.catch_confirm_rect)
            else:
                if not self.spawning_pk_move_mode:
                    if self.spawning_pk is not None and self.game.player.find_sac_item_by_str("Poke_Ball") is not None:
                        if self.is_spawning_pk_lock:
                            surface.blit(self.catch_button_hover, self.catch_button_rect)
                            surface.blit(self.catch_popup, (507 + window_pos[0], 219 + window_pos[1]))
                        else:
                            surface.blit(self.catch_button_lock, self.catch_button_rect)
                            surface.blit(self.catch_popup_lock, (507 + window_pos[0], 219 + window_pos[1]))
                    else:
                        surface.blit(self.catch_button_lock, self.catch_button_rect)
                        surface.blit(self.catch_popup_lock, (507 + window_pos[0], 219 + window_pos[1]))
                else:
                    surface.blit(self.catch_button_lock, self.catch_button_rect)
        else:
            if self.boolcatch_confirm:
                surface.blit(self.catch_confirm, self.catch_confirm_rect)
                if not self.catch_confirm_popup_rect.collidepoint(possouris):
                    self.boolcatch_confirm = False
            else:
                surface.blit(self.catch_button, self.catch_button_rect)

        if self.spawning_levels_button_rect.collidepoint(possouris):
            surface.blit(self.spawning_levels_button_hover, self.spawning_levels_button_rect)
            surface.blit(self.spawning_levels_popup, (36 + window_pos[0], 46 + window_pos[1]))
        else:
            surface.blit(self.spawning_levels_button, self.spawning_levels_button_rect)

        if self.spawning_pk_rect.collidepoint(possouris):
            if self.is_spawning_pk_lock:
                surface.blit(self.spawning_pk_hover_lock, self.spawning_pk_rect)

        if self.is_spawning_pk_lock:
            if self.spawning_pk_rect.collidepoint(possouris):
                surface.blit(self.spawning_pk_hover_lock, self.spawning_pk_rect)
        else:
            if not self.spawning_pk_move_mode:
                if self.spawning_pk_rect.collidepoint(possouris):
                    if self.game.mouse_pressed[1]:
                        self.spawning_pk_move_mode = True
                        self.possouris_rel = [0, 0]
                        self.saved_possouris = possouris

            else:
                if not self.game.mouse_pressed[1]:
                    self.spawning_pk_move_mode = False

                    if self.game.classic_panel.PK_RECTS[0].collidepoint(possouris):
                        self.spawning_pk_in_team(0)
                    elif self.game.classic_panel.PK_RECTS[1].collidepoint(possouris):
                        self.spawning_pk_in_team(1)
                    elif self.game.classic_panel.PK_RECTS[2].collidepoint(possouris):
                        self.spawning_pk_in_team(2)
                    elif self.game.classic_panel.PK_RECTS[3].collidepoint(possouris):
                        self.spawning_pk_in_team(3)
                    elif self.game.classic_panel.PK_RECTS[4].collidepoint(possouris):
                        self.spawning_pk_in_team(4)
                    elif self.game.classic_panel.PK_RECTS[5].collidepoint(possouris):
                        self.spawning_pk_in_team(5)
                else:
                    self.possouris_rel = (possouris[0] - self.saved_possouris[0], possouris[1] - self.saved_possouris[1])
                    self.spawning_pk_rect.x = self.SPAWNING_PK_RECT.x + self.possouris_rel[0]
                    self.spawning_pk_rect.y = self.SPAWNING_PK_RECT.y + self.possouris_rel[1]

            if self.spawning_pk_rect.collidepoint(possouris):
                surface.blit(self.spawning_pk_hover, self.spawning_pk_rect)

        if self.spawning_pk is not None:
            surface.blit(pygame.transform.scale(self.spawning_pk.icon_image, (600, 300)),
                         (self.spawning_pk_rect.x - 19, self.spawning_pk_rect.y - 47), (0, 0, 300, 300))
            if not self.button_aide_rect.collidepoint(possouris):
                surface.blit(self.infos_font.render('Pokemon : ' + self.spawning_pk.name, False, (255, 255, 255)), (570 + window_pos[0], 90 + window_pos[1]))
                surface.blit(self.infos_font.render('Level : ' + str(self.spawning_pk.level), False, (255, 255, 255)),
                             (570 + window_pos[0], 125 + window_pos[1]))

        if self.is_spawning_pk_lock:
            surface.blit(self.spawning_pk_lock, (74 + window_pos[0], 85 + window_pos[1]))

    def update_rect_pos(self, window_pos: list):
        """
        Méthode d'actualisation de la position sur l'écran des rects par rapport à la position de la fenêtre ingame.

        @in : window_pos, list → coordonnées de la fenêtre ingame
        """
        self.button_aide_rect.x = 838 + window_pos[0]
        self.button_aide_rect.y = 46 + window_pos[1]
        self.spawn_button_rect.x = 397 + window_pos[0]
        self.spawn_button_rect.y = 312 + window_pos[1]
        self.catch_button_rect.x = 397 + window_pos[0]
        self.catch_button_rect.y = 216 + window_pos[1]
        self.spawning_levels_button_rect.x = 32 + window_pos[0]
        self.spawning_levels_button_rect.y = 102 + window_pos[1]
        if not self.spawning_pk_move_mode:
            self.spawning_pk_rect.x = 104 + window_pos[0]
            self.spawning_pk_rect.y = 117 + window_pos[1]
            self.SPAWNING_PK_RECT.x = 104 + window_pos[0]
            self.SPAWNING_PK_RECT.y = 117 + window_pos[1]
        self.spawn_confirm_rect.x = 391 + window_pos[0]
        self.spawn_confirm_rect.y = 311 + window_pos[1]
        self.spawn_confirm_popup_rect = pygame.Rect(398 + window_pos[0], 314 + window_pos[1], 338, 92)
        self.catch_confirm_rect.x = 391 + window_pos[0]
        self.catch_confirm_rect.y = 214 + window_pos[1]
        self.catch_confirm_popup_rect = pygame.Rect(398 + window_pos[0], 217 + window_pos[1], 338, 92)

    # Méthodes essentielles

    def spawn_pk(self):
        """
        Méthode qui permet de faire apparaître un pokémon.
        """
        spawning_pk_lv = random.randint(self.min_spawning_pk_level, self.max_spawning_pk_level)

        self.spawning_pk = pokemon.Pokemon(self.get_spawning_pokemon(self.game.player.level, spawning_pk_lv),
                                           spawning_pk_lv,
                                           self.game)
        self.is_spawning_pk_lock = True

        self.game.player.use_action()
        self.game.notif(f'{self.spawning_pk.name} est apparu !', (0, 200, 0))

    def catch_pk(self):
        """
        Méthode qui permet d'attraper un pokémon.
        """
        pokeball_index = self.game.player.find_sac_item_by_str('Poke_Ball')
        if pokeball_index is not None:
            if random.randint(0, 99) > 10:
                self.is_spawning_pk_lock = False
                self.game.notif(f'{self.spawning_pk.name} a été capturé !', (0, 0, 200))
            else:
                self.game.notif(f"{self.spawning_pk.name} s'est échappé.", (255, 0, 0))

            self.game.player.sac[pokeball_index].quantite -= 1
            if self.game.player.sac[pokeball_index].quantite == 0:
                self.game.player.remove_item_sac(pokeball_index)

        else:
            self.game.notif('Nécessite une pokéball', (255, 0, 0))
            
    # Méthodes liées aux calculs
    
    def update_spawning_pk_level(self):
        """
        Méthode d'actualisation du niveau minimal et maximal du pokémon lorsqu'il apparait.
        """
        min_lv = round((self.game.player.level ** 1.9) * 0.22 + 4 + self.spawning_pk_level_bonus)

        if not min_lv == self.min_spawning_pk_level:
            if min_lv >= 100:
                min_lv = 99
            self.min_spawning_pk_level = min_lv

        max_lv = round((self.game.player.level ** 1.9) * 0.40 + 7 + self.spawning_pk_level_bonus)

        if not max_lv == self.max_spawning_pk_level:
            if max_lv >= 100:
                max_lv = 99
            self.max_spawning_pk_level = max_lv
    
    def get_valable_pokemons(self, player_level: int, spawning_pk_level: int) -> list:
        """
        Méthode qui renvoie la liste des noms des pokémons pouvant potentiellement apparaitre en fonction du niveau du
            joueur et du niveau prédéfini d'apparition du pokémon.

        @in : player_level, int
        @in : spawning_pk_level, int
        @out : valable_pks, list
        """
        valable_pks = []

        for pokemon_infos in self.game.pokemons_list.values():
            if pokemon_infos[9] <= player_level and pokemon_infos[11] < spawning_pk_level < pokemon_infos[12]:
                valable_pks.append(pokemon_infos[0])

        return valable_pks

    def get_pk_rarity(self, pokemon_name: str) -> int:
        """
        Méthode qui retourne la valeur de rareté du pokémon utilisée dans l'algorithme permettant de déterminer le
            pokémon qui apparaitra.

        @in : pokemon_name, str → Nom du pokémon
        @out : pokemon_rarity, int → Valeur de rareté
        """
        pokemon_rarity = self.game.pokemons_list[pokemon_name][1]
        pokemon_rarity = 100 - pokemon_rarity
        return pokemon_rarity

    def get_total_spawn_chances(self, valable_pks: list) -> int:
        """
        Méthode qui retourne la somme des valeurs de toutes les raretés cumulées des pokémons dont le nom figure dans la
            liste des pokémon pouvant potentiellement apparaitre.

        @in : valables_pks, list
        @out : total_rarity, int
        """
        total_rarity = 0
        for pokemon_name in valable_pks:
            pokemon_rarity = self.get_pk_rarity(pokemon_name)
            total_rarity += pokemon_rarity
        return total_rarity

    def get_spawning_pokemon(self, player_level: int, spawning_pk_lv: int) -> str:
        """
        Méthode qui retourne le pokémon qui apparait.
        Il est déterminé à partir du niveau du joueur et du niveau d'apparition du pokémon.

        @in : player_level, int
        @in : spawning_pk_lv, int
        @out : pokemon, str → nom du pokémon qui apparait.

        """
        valables_pokemons = self.get_valable_pokemons(player_level, spawning_pk_lv)

        generated_number = random.randint(0, self.get_total_spawn_chances(valables_pokemons))
        max_spawn_value = 0
        for pokemon in valables_pokemons:
            max_spawn_value += self.get_pk_rarity(pokemon)
            if max_spawn_value < generated_number:
                pass
            else:
                return pokemon
            
    # Méthodes annexes

    def spawning_pk_in_team(self, team_i: int):
        """
        Méthode d'ajout du pokémon spawn dans l'équipe.

        @in : team_i, int → indice de l'emplacement dans l'équipe
        """
        if self.game.player.team[team_i] is None:
            self.game.player.team[team_i] = self.spawning_pk
            self.spawning_pk = None
            self.is_spawning_pk_lock = True
            
    def img_load(self, file_name: str) -> pygame.Surface:
        """
        Méthode de chargement d'une image.
        
        @in : file_name, str
        @out : pygame.Surface
        """
        return pygame.image.load(f'{self.PATH}{file_name}.png')
            
    # Méthodes basiques

    def reset(self):
        """
        Méthode de réinitialisation du panel.
        Utilisée lors de l'initialisation d'un nouveau tour de jeu.
        """
        self.spawning_pk = None
        self.is_spawning_pk_lock = True

    def close(self):
        """
        Méthode classique qui éxécute tout ce qu'il faut faire lorsque le panel est fermé.
        """
        pass

    # Méthodes de gestion des intéractions

    def left_clic_interactions(self, possouris: list):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.spawn_button_rect.collidepoint(possouris):

            if self.game.player.actions > 0:
                if not self.boolspawn_confirm:
                    self.boolspawn_confirm = True
                else:
                    self.spawn_pk()
                    self.boolspawn_confirm = False
            else:
                self.game.notif('Action nécessaire', (255, 0, 0))
        elif self.catch_button_rect.collidepoint(possouris):

            if self.spawning_pk is not None:
                if self.game.player.find_sac_item_by_str('Poke_Ball') is not None:

                    if self.is_spawning_pk_lock:
                        if not self.boolcatch_confirm:
                            self.boolcatch_confirm = True
                        else:
                            self.catch_pk()
                            self.boolcatch_confirm = False
                    else:
                        self.game.notif('Pokémon déjà accessible', (255, 0, 0))
                else:
                    self.game.notif('Nécessite une pokéball', (255, 0, 0))
            else:
                self.game.notif('Pokémon à attraper nécessaire', (255, 0, 0))

    def right_clic_interactions(self, posssouris: list):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic droit de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.spawning_pk_rect.collidepoint(posssouris):
            self.game.classic_panel.pokemon_info_mode = True
            self.game.classic_panel.pokemon_info = self.spawning_pk

    def is_hovering_buttons(self, possouris: list):
        """
        Méthode qui retourne True si la souris est positionnée sur un bouton du panel.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.button_aide_rect.collidepoint(possouris):
            return True
        if self.catch_button_rect.collidepoint(possouris):
            return True
        if self.spawn_button_rect.collidepoint(possouris):
            return True
        if self.spawning_levels_button_rect.collidepoint(possouris):
            return True
        if self.spawning_pk_rect.collidepoint(possouris) and not self.is_spawning_pk_lock:
            return True
        return False
