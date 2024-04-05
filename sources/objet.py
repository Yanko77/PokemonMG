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

        # NOM
        self.name = name[0].upper() + name[1:]
        self.name_ = get_name_(self.name)  # Nom affichable

        # IMAGE
        self.icon_image = pygame.image.load(f'assets/icons/items/{self.name}.png')

        # QUANTITE
        self.quantite = quantite

        # LINE
        self.line = self.get_line()

        # SPAWN INFOS
        spawn_infos = self.line[1].split(':')

        self.boolSpawn = int(spawn_infos[0])
        if self.boolSpawn:
            self.spawn_rarity = int(spawn_infos[1])
            spawn_quantite_infos = spawn_infos[2].split('-')
            self.spawn_quantite = (int(spawn_quantite_infos[0]),
                                   int(spawn_quantite_infos[1]))

        # CATEGORIE
        self.categorie = self.line[2]

        # FONCTIONNEMENT
        self.fonctionnement = self.line[3].split(':')[0]
        self.target_pokemon = 'all'

        # BUY INFOS
        buy_infos = self.line[4].split(':')

        self.boolBuy = int(buy_infos[0])
        if self.boolBuy:
            self.buy_price = int(buy_infos[1])
        else:
            self.buy_price = None

        # SELL INFOS
        sell_infos = self.line[5].split(':')

        self.boolSell = int(sell_infos[0])
        if self.boolSell:
            self.boolVariableSellPrice = sell_infos[1][0] == 'v'
            if self.boolVariableSellPrice:
                self.variable_sell_price = [int(sell_infos[1].split('-')[0][1:]),
                                            int(sell_infos[1].split('-')[1])]
                self.sell_price = 0
                self.set_sell_price()
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
                'degats_subis': {
                    'all_attaques': {
                        'type': 'All',  # Type d'attaque dont les degats sont altérés
                        'percent': 0,  # Pourcentage de dégats subis en moins
                        },
                    'super_efficace_attaques': {
                        'type': 'All',  # Type d'attaque dont les degats sont altérés
                        'percent': 0,  # Pourcentage de dégats subis en moins
                    }
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
                'max_actions_bonus': 0,
            }
        }

        self.set_effects()

        # DESCRIPTION
        self.desc_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 17)
        self.description = self.reformate_desc(self.line[7][:-1])

    def get_line(self):
        """
        Méthode qui renvoie la ligne du fichier contenant en brut les informations concernant l'objet.

        @out: list
        """

        with open('all_objets.csv') as file:
            for line in file.readlines():
                if str(line.split(",")[0]) == str(self.name):
                    return line.split(",", maxsplit=7)

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
                    
                # Revive
                elif effect_infos[0] == 'revive':
                    self.effects['Use']['revive'] = True

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
                
                # Dégats subis en moins
                elif effect_infos[0] == 'degats_subis':
                    if effect_infos[1] == 'all_attaques':
                        self.effects['Give']['degats_subis']['all_attaques']['type'] = effect_infos[2]
                        self.effects['Give']['degats_subis']['all_attaques']['percent'] = int(effect_infos[3])
                    elif effect_infos[1] == 'super_efficace':
                        self.effects['Give']['degats_subis']['super_efficace_attaques']['type'] = effect_infos[2]
                        self.effects['Give']['degats_subis']['super_efficace_attaques']['percent'] = int(effect_infos[3])

            elif self.fonctionnement == 'Enable':
                if effect_infos[0] == "max_actions":
                    self.effects["Enable"]["max_actions_bonus"] = int(effect_infos[1])

                elif effect_infos[0] == "all_shiny":
                    self.effects["Enable"]["all_shiny"] = True

            if effect_infos[0] == 'target':
                self.target_pokemon = effect_infos[1]

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
        self.quantite = random.randint(self.spawn_quantite[0], self.spawn_quantite[1])

    # Méthodes d'action

    def enable(self):
        """
        Méthode d'activation de l'objet, s'il est activable.
        """
        print(self.fonctionnement)
        if self.fonctionnement == 'Enable':
            print(self.effects['Enable']['all_shiny'])
            if self.effects['Enable']['all_shiny']:
                self.game.player.always_shiny_on = True

            elif self.effects['Enable']['max_actions_bonus'] != 0:
                self.game.player.rise_max_actions_value(self.effects['Enable']['max_actions_bonus'])
            print(self.effects['Enable']['max_actions_bonus'])

            self.quantite -= 1

    def use(self, pokemon):
        """
        Méthode d'utilisation de l'objet sur un pokémon.

        @in : pokemon, pokemon.Pokemon
        """
        print(self.effects['Use']['revive'])
        if self.effects['Use']['revive']:
            pokemon.is_alive = True
            print('oui')

        if self.effects['Use']['full_heal']:
            pokemon.health = pokemon.pv

        if self.effects['Use']['level'] != 0:
            pokemon.level_up(self.effects['Use']['level'])

        if self.effects['Use']['heal'] != 0:
            pokemon.heal(self.effects['Use']['heal'])

        for status in self.effects['Use']['status']:
            if self.effects['Use']['status'][status]:
                pokemon.status[status] = False

        # STATS
        # Flat
        pokemon.bonus_pvmax += self.effects['Use']['stats']['flat']['pv']
        pokemon.pv += self.effects['Use']['stats']['flat']['pv']
        pokemon.health += self.effects['Use']['stats']['flat']['pv']

        pokemon.bonus_attack += self.effects['Use']['stats']['flat']['atk']
        pokemon.attack += self.effects['Use']['stats']['flat']['atk']

        pokemon.bonus_defense += self.effects['Use']['stats']['flat']['def']
        pokemon.defense += self.effects['Use']['stats']['flat']['def']

        pokemon.bonus_speed += self.effects['Use']['stats']['flat']['vit']
        pokemon.speed += self.effects['Use']['stats']['flat']['vit']

        # Percent
        diff = pokemon.pv - pokemon.health
        pokemon.bonus_pvmax += pokemon.pv * (1 + self.effects['Use']['stats']['percent']['pv'] / 100) - pokemon.pv
        pokemon.pv *= (1 + self.effects['Use']['stats']['percent']['pv'] / 100)
        pokemon.health = pokemon.pv - diff
        pokemon.pv = int(round(pokemon.pv))
        pokemon.health = int(round(pokemon.health))

        pokemon.bonus_attack += pokemon.attack * (1 + self.effects['Use']['stats']['percent']['atk'] / 100) - pokemon.attack
        pokemon.attack *= (1 + self.effects['Use']['stats']['percent']['atk'] / 100)
        pokemon.base_attack *= (1 + self.effects['Use']['stats']['percent']['atk'] / 100)
        pokemon.attack = int(round(pokemon.attack))
        pokemon.base_attack = int(round(pokemon.base_attack))

        pokemon.bonus_attack += pokemon.defense * (1 + self.effects['Use']['stats']['percent']['def'] / 100) - pokemon.defense
        pokemon.defense *= (1 + self.effects['Use']['stats']['percent']['def'] / 100)
        pokemon.base_defense *= (1 + self.effects['Use']['stats']['percent']['def'] / 100)
        pokemon.defense = int(round(pokemon.defense))
        pokemon.base_defense = int(round(pokemon.base_defense))

        pokemon.bonus_speed *= pokemon.speed * (1 + self.effects['Use']['stats']['percent']['vit'] / 100) - pokemon.speed
        pokemon.speed *= (1 + self.effects['Use']['stats']['percent']['vit'] / 100)
        pokemon.base_speed *= (1 + self.effects['Use']['stats']['percent']['vit'] / 100)
        pokemon.speed = int(round(pokemon.speed))
        pokemon.base_speed = int(round(pokemon.base_speed))

        self.quantite -= 1

    def give(self, pokemon):
        """
        Méthode permettant d'appliquer les effets de l'objet lorsqu'on give l'objet à un pokémon.

        @in : pokemon, pokemon.Pokemon
        """

        # STATS
        # Flat
        pokemon.bonus_pvmax += self.effects['Give']['stats']['flat']['pv']
        pokemon.pv += self.effects['Give']['stats']['flat']['pv']

        pokemon.bonus_attack += self.effects['Give']['stats']['flat']['atk']
        pokemon.attack += self.effects['Give']['stats']['flat']['atk']

        pokemon.bonus_defense += self.effects['Give']['stats']['flat']['def']
        pokemon.defense += self.effects['Give']['stats']['flat']['def']

        pokemon.bonus_speed += self.effects['Give']['stats']['flat']['vit']
        pokemon.speed += self.effects['Give']['stats']['flat']['vit']

        # Percent
        pokemon.multiplicateur_pvmax *= (1 + self.effects['Give']['stats']['percent']['pv']/100)
        pokemon.pv *= (1 + self.effects['Give']['stats']['percent']['pv']/100)
        pokemon.health *= (1 + self.effects['Give']['stats']['percent']['pv']/100)
        pokemon.pv = int(round(pokemon.pv))
        pokemon.health = int(round(pokemon.health))

        pokemon.multiplicateur_attack *= (1 + self.effects['Give']['stats']['percent']['atk'] / 100)
        pokemon.attack *= (1 + self.effects['Give']['stats']['percent']['atk'] / 100)
        pokemon.base_attack *= (1 + self.effects['Give']['stats']['percent']['atk'] / 100)
        pokemon.attack = int(round(pokemon.attack))
        pokemon.base_attack = int(round(pokemon.base_attack))

        pokemon.multiplicateur_defense *= (1 + self.effects['Give']['stats']['percent']['def'] / 100)
        pokemon.defense *= (1 + self.effects['Give']['stats']['percent']['def'] / 100)
        pokemon.base_defense *= (1 + self.effects['Give']['stats']['percent']['def'] / 100)
        pokemon.defense = int(round(pokemon.defense))
        pokemon.base_defense = int(round(pokemon.base_defense))

        pokemon.multiplicateur_speed *= (1 + self.effects['Give']['stats']['percent']['vit'] / 100)
        pokemon.speed *= (1 + self.effects['Give']['stats']['percent']['vit'] / 100)
        pokemon.base_speed *= (1 + self.effects['Give']['stats']['percent']['vit'] / 100)
        pokemon.speed = int(round(pokemon.speed))
        pokemon.base_speed = int(round(pokemon.base_speed))

        self.quantite -= 1

    def remove(self, pokemon):
        """
        Méthode permettant de réinitialiser les bonus apportés par l'objet lorsqu'il est retiré.

        @in : pokemon, pokemon.Pokemon
        """

        # STATS
        # Flat
        pokemon.bonus_pvmax -= self.effects['Give']['stats']['flat']['pv']
        pokemon.pv -= self.effects['Give']['stats']['flat']['pv']

        pokemon.bonus_attack -= self.effects['Give']['stats']['flat']['atk']
        pokemon.attack -= self.effects['Give']['stats']['flat']['atk']

        pokemon.bonus_defense -= self.effects['Give']['stats']['flat']['def']
        pokemon.defense -= self.effects['Give']['stats']['flat']['def']

        pokemon.bonus_speed -= self.effects['Give']['stats']['flat']['vit']
        pokemon.speed -= self.effects['Give']['stats']['flat']['vit']

        # Percent
        pokemon.multiplicateur_pvmax /= (1 + self.effects['Give']['stats']['percent']['pv'] / 100)
        pokemon.pv /= (1 + self.effects['Give']['stats']['percent']['pv'] / 100)
        pokemon.health /= (1 + self.effects['Give']['stats']['percent']['pv'] / 100)
        pokemon.pv = int(round(pokemon.pv))
        pokemon.health = int(round(pokemon.health))

        pokemon.multiplicateur_attack /= (1 + self.effects['Give']['stats']['percent']['atk'] / 100)
        pokemon.attack /= (1 + self.effects['Give']['stats']['percent']['atk'] / 100)
        pokemon.base_attack /= (1 + self.effects['Give']['stats']['percent']['atk'] / 100)
        pokemon.attack = int(round(pokemon.attack))
        pokemon.base_attack = int(round(pokemon.base_attack))

        pokemon.multiplicateur_defense /= (1 + self.effects['Give']['stats']['percent']['def'] / 100)
        pokemon.defense /= (1 + self.effects['Give']['stats']['percent']['def'] / 100)
        pokemon.base_defense /= (1 + self.effects['Give']['stats']['percent']['def'] / 100)
        pokemon.defense = int(round(pokemon.defense))
        pokemon.base_defense = int(round(pokemon.base_defense))

        pokemon.multiplicateur_speed /= (1 + self.effects['Give']['stats']['percent']['vit'] / 100)
        pokemon.speed /= (1 + self.effects['Give']['stats']['percent']['vit'] / 100)
        pokemon.base_speed /= (1 + self.effects['Give']['stats']['percent']['vit'] / 100)
        pokemon.speed = int(round(pokemon.speed))
        pokemon.base_speed = int(round(pokemon.base_speed))

    # Méthodes d'actualisation

    def set_sell_price(self):
        """
        Méthode d'actualisation du prix de vente.
        Utile notamment pour les gérer le principe de prix variables du marché
        """
        if self.boolSell:
            self.sell_price = self.get_sell_price()
                
            if self.buy_price is not None:
                if self.sell_price > self.buy_price:
                    self.boolBuy = False
                else:
                    self.boolBuy = True

    def get_sell_price(self):
        return self.game.get_item_price(self)

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
