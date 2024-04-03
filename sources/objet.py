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
                'endfight_heal': 0,
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
        if self.fonctionnement == 'Use':
            pass
        elif self.fonctionnement == 'Give':
            pass
        elif self.fonctionnement == 'Enable':
            pass



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
