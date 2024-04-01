"""
Fichier gérant les objets du jeu.
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

        self.name = name[0].upper() + name[1:]
        self.name_ = self.reformate_name(self.name)
        self.icon_image = pygame.image.load(f'assets/icons/items/{self.name}.png')
        self.quantite = int(quantite)

        self.line = self.find_item_line()

        self.boolSpawnable = int(self.line[1].split(':')[0])
        self.rarity = int(self.line[1].split(':')[1])
        self.quantite_at_spawn = (int(self.line[1].split(':')[2].split('-')[0]),
                                  int(self.line[1].split(':')[2].split('-')[1]))

        self.categorie = self.line[2]
        self.fonctionnement = self.line[3].split(':')[0]

        self.effect = None
        self.heal_value = 0
        self.type = None
        self.multiplicateur_attaque_dmg = 1
        self.stat = None
        self.bonus_stat = 0
        self.pv_pourcent_activate = None
        self.removed_status = {
            'Sommeil': False,
            'Brulure': False,
            'Confusion': False,
            'Gel': False,
            'Poison': False,
            'Paralysie': False}
        self.multiplicateur_pvmax = 1
        self.heal_after_each_fight = 0
        self.target_pokemon = 'All'
        self.multiplicateur_stats = {
            'pv': 1,
            'atk': 1,
            'def': 1,
            'vit': 1
        }
        self.bonus_lv = 0
        self.bool_revive_effect = False

        self.set_special_effects()

        self.can_be_sell = int(self.line[5].split(':')[0])

        self.sell_price = float('inf')

        if self.can_be_sell:
            if self.line[5].split(':')[1] == 'v':
                self.bool_variable_sell_price = True
                self.variable_sell_price = [int(self.line[5].split(':')[2].split('-')[0]), int(self.line[5].split(':')[2].split('-')[1])]
            else:
                self.bool_variable_sell_price = False
                self.variable_sell_price = [int(self.line[5].split(':')[1]),
                                            int(self.line[5].split(':')[1])]
                self.sell_price = int(self.line[5].split(':')[1])
        else:
            self.bool_variable_sell_price = False

        self.can_be_buy = int(self.line[4].split(':')[0])
        self.buy_price = float('inf')
        if self.can_be_buy:
            self.buy_price = int(self.line[4].split(':')[1])

        self.set_sell_price()

        self.desc_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 17)
        self.description = self.line[6][:-1]
        self.description = self.reformate_desc(self.description)

    # Méthodes d'initialisation

    def set_special_effects(self):
        """
        Méthode d'initialisation des effets spéciaux de l'objet.
        """
        if self.fonctionnement in ('Use', 'Give'):
            self.effect = self.line[3].split(':')[1]
            if self.effect == 'special':
                if self.name == 'Collier_Agathe':
                    self.multiplicateur_pvmax = 0.80
                    self.heal_after_each_fight = 10000
                elif self.name == 'Casquette_de_Nathan':
                    self.target_pokemon = 'Tyranocif'
                    self.multiplicateur_stats = {
                        'pv': 1.25,
                        'atk': 1.25,
                        'def': 1.25,
                        'vit': 1.25
                    }
                elif self.name == 'Caillou':
                    self.multiplicateur_stats['vit'] = 0.99
            else:
                if self.effect == 'h':
                    if self.fonctionnement == 'Give':
                        self.heal_value = int(self.line[3].split(':')[2].split('-')[0])
                        self.pv_pourcent_activate = int(self.line[3].split(':')[2].split('-')[1][:-1])
                    else:
                        self.heal_value = int(self.line[3].split(':')[2])
                elif self.effect == 'b':
                    self.stat = self.line[3].split(':')[2]
                    if self.stat == 'pv':
                        self.bonus_stat = 1
                        self.multiplicateur_stats['pv'] = 1.05
                    else:
                        self.bonus_stat = 5
                elif self.effect == 'p':
                    self.type = self.line[3].split(':')[2]
                    self.multiplicateur_attaque_dmg = 1.20
                elif self.effect == 's':
                    if self.line[3].split(':')[2] == 'All':
                        self.removed_status = {
                            'Sommeil': True,
                            'Brulure': True,
                            'Confusion': True,
                            'Gel': True,
                            'Poison': True,
                            'Paralysie': True}
                    else:
                        self.removed_status[self.line[3].split(':')[2]] = True
                elif self.effect == 'revive':
                    self.bool_revive_effect = True
                    self.heal_value = 1000
                else:  # self.effect == l
                    self.bonus_lv = int(self.line[3].split(':')[2])

    def reformate_name(self, name: str) -> str:
        """
        Méthode de reformatage du nom.
        Permet de convertir le nom interne au jeu en nom affichable pour le joueur.

        @in : name, str → nom de l'objet
        @out : reformated_name, str
        """
        reformated_name = ''

        if name == 'Collier_agathe':  # Exception pour cet objet
            reformated_name = "Collier d'Agathe"
        else:
            for c in name:
                if c == '_':
                    reformated_name += ' '
                else:
                    reformated_name += c

        return reformated_name

    def reformate_desc(self, desc):
        """
        Méthode de reformatage de la description de l'objet pour l'affichage dans le sac et la boutique d'objets.

        @in : desc, str
        @out: list
        """
        l1 = desc
        l2 = ''
        l3 = ''

        while self.desc_font.render(l1, False, (0, 0, 0)).get_rect().w > 400:
            l2 = l1.split()[-1] + ' ' + l2
            l1 = l1[:-(len(l1.split()[-1]) + 1)]
        while self.desc_font.render(l2, False, (0, 0, 0)).get_rect().w > 400:
            l3 = l2.split()[-1] + ' ' + l3
            l2 = l2[:-(len(l2.split()[-1]) + 1)]

        return l1, l2, l3

    def set_quantite_at_spawn(self):
        """
        Méthode qui détermine la quantité au spawn de l'objet.
        """
        self.quantite = random.randint(self.quantite_at_spawn[0], self.quantite_at_spawn[1])

    def find_item_line(self):
        """
        Méthode qui renvoie la ligne du fichier contenant en brut les informations concernant l'objet.

        @out: list
        """
        with open('all_objets.txt') as file:
            for line in file.readlines():
                if str(line.split()[0]) == str(self.name):
                    return line.split(maxsplit=6)

    # Méthodes d'action

    def enable_item(self):
        """
        Méthode d'activation de l'objet, s'il est activable.
        """
        if self.fonctionnement == 'Enable':
            if self.name in ('Velo', 'Pokeflute'):
                self.game.rise_max_actions_value()

            if self.name == 'Charme_Chroma':
                print('Activation du charme Chroma')
                self.game.always_shiny_on = True

            self.quantite -= 1

    # Méthodes d'actualisation

    def set_sell_price(self):
        """
        Méthode d'actualisation du prix de vente.
        Utile notamment pour les gérer le principe de prix variables du marché
        """
        self.sell_price = self.get_sell_price()

        if self.sell_price > self.buy_price:
            self.can_be_buy = False

    def get_sell_price(self):
        return self.game.get_item_price(self)


