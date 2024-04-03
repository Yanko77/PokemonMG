"""
Fichier gérant les objets du jeu
"""

# Importation des modules
import pygame

# Définition des classes


class Objet:
    """
        Classe représentant un objet du jeu.

        Un objet est défini par :
        - son nom, str
        - la game dans laquelle il intervient, game.Game
        - sa quantité, int
    """

    def __init__(self, name, game, quantite=1):
        self.game = game
        self.line = self.get_line()

        # NOM
        self.name = name[0].upper() + name[1:]
        self.name_ = get_name_(self.name)  # Nom affichable

        # IMAGE
        self.icon_image = pygame.image.load(f'assets/icons/items/{self.name}.png')

        # QUANTITE
        self.quantite = quantite

        # SPAWN INFOS
        spawn_infos = self.line[1].split(':')
        spawn_quantite_infos = spawn_infos[2].split('-')

        self.boolSpawn = spawn_infos[0]
        self.spawn_rarity = spawn_infos[1]
        self.spawn_quantite = (spawn_quantite_infos[0],
                               spawn_quantite_infos[1])

        # CATEGORIE
        self.categorie = self.line[2]

        # FONCTIONNEMENT
        self.fonctionnement = self.line[3].split(':')[0]
        self.target_pk = 'all'

        # BUY INFOS
        buy_infos = self.line[4].split(':')

        self.boolBuy = int(buy_infos[0])
        if self.boolBuy:
            self.buy_price = int(buy_infos[1])
        else:
            self.buy_price = float('inf')

        # SELL INFOS
        sell_infos = self.line[5].split(':')

        self.boolSell = int(sell_infos[0])
        if self.boolSell:
            self.boolVariableSellPrice = sell_infos[1][0] == 'v'
            if self.boolVariableSellPrice:
                self.sell_price = [int(sell_infos[1].split(':')[0]),
                                   int(sell_infos[1].split(':')[1])]
            else:
                self.sell_price = int(sell_infos[1])

        # EFFECTS
        self.effects = {
            'Use': {
                'full_heal': False,
                'heal': 0,  # Instant healing
                'stats': {  # Bonus stats
                    'flat': {
                        'pv': 0,
                        'atk': 0,
                        'def': 0,
                        'vit': 0
                    },
                    'percent': {
                        'pv': 0,
                        'atk': 0,
                        'def': 0,
                        'vit': 0
                    }

                },
                'status': {  # Status removing
                    'Sommeil': False,
                    'Brulure': False,
                    'Confusion': False,
                    'Gel': False,
                    'Poison': False,
                    'Paralysie': False
                },
                'level': 0,  # Level up
                'revive': False  # Revive
            },
            'Give': {
                'attaque': {  # Bonus sur les attaques
                    'type': 'All',
                    'percent_bonus': 0,
                },
                'stats': {  # Bonus sur les stats
                    'flat': {
                        'pv': 0,
                        'atk': 0,
                        'def': 0,
                        'vit': 0
                    },
                    'percent': {
                        'pv': 0,
                        'atk': 0,
                        'def': 0,
                        'vit': 0
                    }
                },
                'heal': {  # Delayed instant healing
                    'percent_activate': 0,
                    'value': 0
                },
                'endfight_heal': {
                    'full_heal': False,
                    'value': 0
                },
                'first_chance': 0,
            },
            'Enable': {
                'all_shiny': False,
                'max_action_bonus': 0,
            }
        }

        self.set_effects()

    def get_line(self):
        """
        Méthode qui renvoie la ligne du fichier contenant en brut les informations concernant l'objet.

        @out: list
        """

        with open('all_objets.txt') as file:
            for line in file.readlines():
                if str(line.split()[0]) == str(self.name):
                    return line.split(maxsplit=6)

    def set_effects(self):
        """
        Méthode d'initialisation des effets spéciaux de l'objet.
        """
        effects_list = self.line[6].split('|')
        for effect in effects_list:
            effect_infos = effect.split(':')

            if self.fonctionnement == 'Use':
                # bonus stats
                if effect_infos[0] == 'b':
                    self.effects['Use']['stats']['flat'][effect_infos[1]] = int(effect_infos[2])

                # Instant heal
                elif effect_infos[0] == 'h':
                    self.effects['Use']['heal'] = int(effect_infos[1])  # nb_pv

                # Multiplicateur de stats
                elif effect_infos[0] == 'm':
                    self.effects['Use']['stats']['percent'][effect_infos[1]] = int(effect_infos[2])

                # Effets de status retirés
                elif effect_infos[0] == 's':
                    if effect_infos[1] == 'all':
                        self.effects['Use']['status'] = {
                            'Sommeil': True,
                            'Brulure': True,
                            'Confusion': True,
                            'Gel': True,
                            'Poison': True,
                            'Paralysie': True
                        }
                    else:
                        self.effects['Use']['status'][effect_infos[1]] = True

                # Instant full heal
                elif effect_infos[0] == 'full_h':
                    self.effects['Use']['full_heal'] = True

                # Level up
                elif effect_infos[0] == 'l':
                    self.effects['Use']['level'] = int(effect_infos[1])

            elif self.fonctionnement == 'Give':

                # Puissance bonus des attaques
                if effect_infos[0] == 'p':
                    self.effects['Give']['attaque']['type'] = effect_infos[1]
                    self.effects['Give']['attaque']['percent_bonus'] = int(effect_infos[2])

                # Instant heal (avec poucentage d'activation)
                elif effect_infos[0] == 'h':
                    self.effects['Give']['heal']['percent_activate'] = int(effect_infos[1].split("-")[1][:-1])
                    self.effects['Give']['heal']['value'] = int(effect_infos[1].split("-")[0])

                # Multiplicateur de stats (en pourcentage)
                elif effect_infos[0] == 'm':
                    if effect_infos[1] == 'all':
                        self.effects['Give']['stats']['percent'] = {'pv': int(effect_infos[2]),
                                                                    'atk': int(effect_infos[2]),
                                                                    'def': int(effect_infos[2]),
                                                                    'vit': int(effect_infos[2])}
                    else:
                        self.effects['Give']['stats']['percent'][effect_infos[1]] = int(effect_infos[2])

                # Instant heal de fin de combat
                elif effect_infos[0] == 'endfight_heal':
                    if effect_infos[1] == 'full':
                        self.effects['Give']['endfight_heal']['full_heal'] = True
                    else:
                        self.effects['Give']['endfight_heal']['value'] = int(effect_infos[1])

                # Chances d'attaquer en premier en combat
                elif effect_infos[0] == 'first_chance':
                    self.effects['Give']['first_chance'] = int(effect_infos[1])

            elif self.fonctionnement == 'Enable':

                if effect_infos[0] == "max_actions":
                    self.effects["Enable"]["max_action_bonus"] = int(effect_infos[1])

                elif effect_infos[0] == "all_shiny":
                    self.effects["Enable"]["all_shiny"] = True

            if effect_infos[0] == 'target':
                self.target_pk = effect_infos[1]


# Fonctions

def get_name_(name):
    """
    Fonction de reformatage du nom.
    Permet de convertir le nom interne au jeu en nom affichable pour le joueur.
    Retourne le nom à afficher.

    Format : Les '_' deviennent des ' '

    @in : name, str → nom de l'objet
    @out : name_, str
    """

    return str.replace(name, '_', ' ')
