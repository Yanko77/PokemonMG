"""
Fichier gérant les pokémons du jeu.
"""

# Importation des modules

import pygame
import random
import objet
import game_infos
import attaques
import csv


# Définiton des classes.


class Pokemon:
    """
    Classe représentant un Pokémon du jeu.

    Un Pokémon est défini par :
    - son nom, str
    - son niveau, int
    - la game dans laquelle il intervient, game.Game
    - s'il est shiny ou non, bool
    - l'objet qu'il porte, objet.Objet / None
    """

    def __init__(self, name, level, game, is_shiny=None, objet_tenu=None):
        self.game = game

        self.name = name[0].upper() + name[1:].lower()
        self.is_shiny = self.def_shiny(is_shiny)
        self.id = self.game.get_init_pokemon_id()
        self.random_seed = self.generate_random_seed_number()

        self.objet_tenu = objet_tenu
        self.status = {
            'Sommeil': False,
            'Brulure': False,
            'Confusion': False,
            'Gel': False,
            'Poison': False,
            'Paralysie': False
        }

        self.infos = self.get_infos()

        self.level = int(level)
        self.rarity = self.infos[1]
        self.min_spawn_lv = self.infos[11]
        self.max_spawn_lv = self.infos[12]

        self.type = self.infos[2]
        self.type2 = self.infos[10]

        self.bonus_pvmax = 0
        self.multiplicateur_pvmax = 1
        self.pv = round(((2 * self.infos[
            3] * self.level) / 100 + self.level + 10) + self.bonus_pvmax) * self.multiplicateur_pvmax  # PV MAX
        self.health = self.pv + self.bonus_pvmax  # PV ACTUELS

        self.bonus_attack = 0
        self.multiplicateur_attack = 1
        self.base_attack = round(
            ((2 * int(self.infos[4]) * self.level) / 100 + 5) + self.bonus_attack) * self.multiplicateur_attack
        self.attack = self.base_attack

        self.bonus_defense = 0
        self.multiplicateur_defense = 1
        self.base_defense = round(
            ((2 * int(self.infos[5]) * self.level) / 100 + 5) + self.bonus_defense) * self.multiplicateur_defense
        self.defense = self.base_defense

        self.bonus_speed = 0
        self.multiplicateur_speed = 1
        self.base_speed = round(
            ((2 * int(self.infos[6]) * self.level) / 100 + 5) + self.bonus_speed) * self.multiplicateur_speed
        self.speed = self.base_speed

        self.evolution_level = int(self.infos[7])
        self.evolution_name = str(self.infos[8])
        if "/" in self.evolution_name:
            evolutions_name_list = self.evolution_name.split("/")
            r = random.Random()
            r.seed(self.random_seed)
            self.evolution_name = r.choice(evolutions_name_list)
            # print("Evolution future:", self.evolution_name)
        self.min_p_lv = int(self.infos[9])
        self.is_alive = True
        self.is_vulnerable = True

        if self.is_shiny:
            # print(self.name, 'est shiny !!')
            self.icon_image = pygame.image.load(f'assets/icons/pokemons/{self.name}_.png')
        else:
            self.icon_image = pygame.image.load(f'assets/icons/pokemons/{self.name}.png')

        self.passive_heal = 0

        self.attaque_pool_line = self.find_attaque_pool_line()
        self.attaque_pool = self.init_attaque_pool()

    def get_infos(self) -> tuple:
        """
        Retourne toutes les infos concernant le pokémon
        """

        return self.game.pokemons_list[self.name]

    def find_attaque_pool_line(self) -> list:
        """
        Retourne le nom des attaques du pool d'attaque du pokémon (issu de pokemon_attaque_pool.txt)
        """
        with open('pokemon_attaque_pool.txt') as file:
            for line in file.readlines():
                if line.split()[0] == self.name:
                    return line.split()[1].split(',')

    def init_attaque_pool(self) -> list:
        """
        Méthode d'initialisation du pool d'attaque du pokémon.

        @out : attaque_pool, list
        """
        attaque_pool = [None, None, None, None]
        if len(self.attaque_pool_line) <= 4:
            i = 0
            for attaque_name in self.attaque_pool_line:
                attaque_pool[i] = (attaques.Attaque(attaque_name))
                i += 1

        else:
            attaque_name_list = random.sample(self.attaque_pool_line, 4)
            i = 0
            for attaque_name in attaque_name_list:
                attaque_pool[i] = (attaques.Attaque(attaque_name))
                i += 1

        return attaque_pool

    def level_up(self, nb_lv=1):
        """
        Méthode d'augmentation du niveau du pokémon.

        @in : nb_lv, int → nombre de niveaux d'augmentation.
        """
        self.level += nb_lv
        diff = self.pv - self.health
        self.pv = round((round((2 * int(
            self.infos[3]) * self.level) / 100 + self.level + 10) + self.bonus_pvmax) * self.multiplicateur_pvmax)
        self.health = self.pv - diff
        self.base_attack = round(
            (round((2 * int(self.infos[4]) * self.level) / 100 + 5) + self.bonus_attack) * self.multiplicateur_attack)
        self.base_defense = round(
            (round((2 * int(self.infos[5]) * self.level) / 100 + 5) + self.bonus_defense) * self.multiplicateur_defense)
        self.base_speed = round(
            (round((2 * int(self.infos[6]) * self.level) / 100 + 5) + self.bonus_speed) * self.multiplicateur_speed)

        self.attack = self.base_attack
        self.defense = self.base_defense
        self.speed = self.base_speed

    def set_bonus_stats(self, bonus_stats: tuple):
        """
        Methode qui applique les bonus stats prise en paramètre d'entrée, de la forme:
        (pvmax_bonus,
        atk_bonus,
        def_bonus,
        speed_bonus,
        pvmax_multiplicateur,
        atk_multiplicateur,
        def_multiplicateur,
        speed_multiplicateur)

        @in : bonus_stats, tuple
        """
        stats = bonus_stats

        self.bonus_pvmax = int(stats[0])
        self.bonus_attack = int(stats[1])
        self.bonus_defense = int(stats[2])
        self.bonus_speed = int(stats[3])
        self.multiplicateur_pvmax = float(stats[4])
        self.multiplicateur_attack = float(stats[5])
        self.multiplicateur_defense = float(stats[6])
        self.multiplicateur_speed = float(stats[7])

        # Application des bonus
        diff = self.pv - self.health
        self.pv = round((round((2 * int(
            self.infos[3]) * self.level) / 100 + self.level + 10) + self.bonus_pvmax) * self.multiplicateur_pvmax)
        self.health = self.pv - diff
        self.base_attack = round(
            (round((2 * int(self.infos[4]) * self.level) / 100 + 5) + self.bonus_attack) * self.multiplicateur_attack)
        self.base_defense = round(
            (round((2 * int(self.infos[5]) * self.level) / 100 + 5) + self.bonus_defense) * self.multiplicateur_defense)
        self.base_speed = round(
            (round((2 * int(self.infos[6]) * self.level) / 100 + 5) + self.bonus_speed) * self.multiplicateur_speed)

        self.attack = self.base_attack
        self.defense = self.base_defense
        self.speed = self.base_speed

    def evolution(self):
        """
        Méthode permettant de faire évoluer le pokémon.
        Renvoie un pokémon : son évolution s'il peut évoluer, lui sinon.

        @out: pokemon.Pokemon
        """
        if self.evolution_name == '0':
            print("Ce pokémon n'a pas d'évolution(s)")
            return self
        else:
            if self.level >= self.evolution_level:
                evol = Pokemon(self.evolution_name, self.level, self.game, self.is_shiny, objet_tenu=self.objet_tenu)
                evol.set_bonus_stats(self.get_bonus_stats())
                return evol
            else:
                return self

    def full_heal(self):
        """
        Méthode de régénération des pv actuels du pokémon.
        """
        self.health = self.pv

    def get_save_infos(self, delimiter: str = ',') -> str:
        """
        Méthode qui renvoie la ligne à écrire dans le fichier de sauvegarde pour stocker l'ensemble des infos qui le définissent.

        @in : delimiter, str → délimiteur choisi pour l'écriture des infos. Varie selon le fichier.

        Exemple :
         Format : Name, level, id, objet, is_shiny, health, all_bonus_stats, is_alive, attaque_pool

            "Pikachu,10,5,None,False,18,0/0/0/0/1/1/1/1,True,Griffe:25/Vive-Attaque:15/None/None"
        """

        assert delimiter not in (' ', ':', '/'), "Séparateur déjà utilisé, causera des erreurs de split"

        item = self.objet_tenu
        if item is None:
            item = 'None'
        else:
            item = item.name

        return f"{self.get_name()}{delimiter}{self.get_level()}{delimiter}{self.get_id()}{delimiter}{item}{delimiter}{self.is_shiny}{delimiter}{self.health}{delimiter}{self.get_bonus_stats_backup()}{delimiter}{self.is_alive}{delimiter}{self.get_attaque_pool_backup()}"

    def get_bonus_stats(self) -> tuple:
        return self.bonus_pvmax, self.bonus_attack, self.bonus_defense, self.bonus_speed, self.multiplicateur_pvmax, self.multiplicateur_attack, self.multiplicateur_defense, self.multiplicateur_speed

    def get_bonus_stats_backup(self) -> str:
        """
        Retourne l'expression à écrire dans le fichier de sauvegarde pour stocker les valeurs des stats bonus du pokémon.

        @out: str
        """
        all_bonus_stat = self.get_bonus_stats()
        all_bonus_stat_backup = ""
        for bonus in all_bonus_stat:
            all_bonus_stat_backup += f'{bonus}/'

        return all_bonus_stat_backup[:-1]

    def get_attaque_pool_backup(self) -> str:
        """
        Retourne l'expression à écrire dans le fichier de sauvegarde pour stocker le pool d'attaque du pokémon.

        @out : str
        """
        attaque_pool = [None, None, None, None]
        i = 0
        for att in self.attaque_pool:
            if att is not None:
                attaque_pool[i] = f"{att.name}:{att.pp}"
            i += 1

        attaque_pool_backup = ""
        for attaque_infos in attaque_pool:
            if attaque_infos is None:
                attaque_pool_backup += "None/"
            else:
                attaque_pool_backup += f"{attaque_infos}/"

        return attaque_pool_backup[:-1]

    def load_save_infos(self, save_infos: list):
        """
        Methode qui charge les informations sauvegardées du pokémon.

        @in : save_infos, list
        """

        self.id = int(save_infos[2])
        self.health = int(save_infos[5])
        stats = save_infos[6].split('/')
        self.bonus_pvmax = int(stats[0])
        self.bonus_attack = int(stats[1])
        self.bonus_defense = int(stats[2])
        self.bonus_speed = int(stats[3])
        self.multiplicateur_pvmax = float(stats[4])
        self.multiplicateur_attack = float(stats[5])
        self.multiplicateur_defense = float(stats[6])
        self.multiplicateur_speed = float(stats[7])

        # Application des bonus
        diff = self.pv - self.health
        self.pv = round((round((2 * int(
            self.infos[3]) * self.level) / 100 + self.level + 10) + self.bonus_pvmax) * self.multiplicateur_pvmax)
        self.health = self.pv - diff
        self.base_attack = round(
            (round((2 * int(self.infos[4]) * self.level) / 100 + 5) + self.bonus_attack) * self.multiplicateur_attack)
        self.base_defense = round(
            (round((2 * int(self.infos[5]) * self.level) / 100 + 5) + self.bonus_defense) * self.multiplicateur_defense)
        self.base_speed = round(
            (round((2 * int(self.infos[6]) * self.level) / 100 + 5) + self.bonus_speed) * self.multiplicateur_speed)

        self.attack = self.base_attack
        self.defense = self.base_defense
        self.speed = self.base_speed

        self.is_alive = save_infos[7] == 'True'
        attaque_pool = []
        for att in save_infos[8].split("/"):
            if att == 'None':
                attaque_pool.append(None)
            else:
                attaque_pool.append(attaques.Attaque(att.split(":")[0], pp=int(att.split(":")[1])))

        self.attaque_pool = attaque_pool

    def get_id(self):
        return self.id

    def get_stats(self):
        return self.pv, self.attack, self.defense, self.speed

    def get_level(self):
        return self.level

    def get_type(self):
        return self.type

    def get_type2(self):
        return self.type2

    def get_name(self):
        return self.name

    def get_icon(self):
        return self.icon_image

    def get_attaque_pool(self):
        return self.attaque_pool

    def heal(self, value):
        """
        Méthode de régénération des pv actuels du pokémon.

        @in : value, int → nombre de pv à régénérer
        """
        self.health += value
        if self.health > self.pv:
            self.health = self.pv

    def damage(self, amount):
        """
        Méthode faisant subir au pokémon des dégats

        @in : amount, int → nombre de points de pv en dégats subis
        """

        self.health -= amount
        if self.health <= 0:
            self.is_alive = False
            self.health = 0

    def attaque(self, pokemon, attaque) -> list:
        """
        Attaque le pokémon renseigné en parametre avec l'attaque prise en entrée.

        Renvoie une liste contenant :
            - True si l'attaque a abouti, False sinon
            - None si l'attaque n'a pas appliqué d'effet à personne, (<nom_effet>, <self ou pokemon>) sinon

        @in : pokemon, pokemon.Pokemon → pokémon défenseur qui subira l'attaque
        @in : attaque, attaques.Attaque → attaque lancée
        @out : list
        """

        attaque_infos = []

        precision_value = random.randint(0, 99)
        print(f'{attaque.name}: {attaque.precision} | {precision_value}')
        if precision_value < attaque.precision:

            degats = 0
            if attaque.puissance != 0 and pokemon.is_vulnerable:

                cm = 1
                # Calcul avec stab ( attaque de type maternel )
                if attaque.type in [self.type, self.type2]:
                    cm *= 1.5

                # Calcul avec affinités des types
                cm *= game_infos.get_mutiliplicateur(attaque.type, pokemon.type)

                if not pokemon.type2 == 'NoType':
                    cm *= game_infos.get_mutiliplicateur(attaque.type, pokemon.type2)

                # Calcul avec taux de crit
                t = round(int(self.infos[6]) / 2) * attaque.taux_crit
                ncrit = random.randint(0, 256)
                if ncrit < t:
                    crit = True
                else:
                    crit = False

                if crit:
                    cm *= (2 * self.level + 5) / (self.level + 5)
                    # print(f'CRITIQUE DE {self.name}')

                if self.objet_tenu is not None:
                    if self.objet_tenu.effects['Give']['attaque']['type'] == attaque.type or self.objet_tenu.effects['Give']['attaque']['type'] == 'All':
                        cm *= (1 + self.objet_tenu.effects['Give']['attaque']['percent_bonus']/100)
                random_cm = random.randint(85, 100)
                cm = cm * random_cm / 100

                puissance = 0

                if attaque.puissance == "level":
                    puissance = self.level

                elif attaque.puissance == "pv*0.5":
                    puissance = pokemon.health // 2
                elif attaque.bool_special_puissance:
                    if attaque.special_puissance[0] == 'v':
                        if self.speed <= pokemon.speed:
                            puissance = int(attaque.puissance.split("-")[0])
                        else:
                            puissance = int(attaque.puissance.split("-")[1])
                    elif attaque.special_puissance[0] == 'r':
                        values = attaque.special_puissance[1].split("-")
                        puissance = random.randint(int(values[0]), int(values[1]))
                    elif attaque.special_puissance == 'ennemy_pv':
                        if pokemon.health == 1:
                            degats = 1
                        else:
                            degats = round(pokemon.health * attaque.puissance)

                    else:
                        puissance = attaque.puissance
                else:
                    puissance = attaque.puissance

                if degats == 0:
                    if attaque.special_puissance == 'c':
                        degats = attaque.puissance
                    elif attaque.puissance == "effort":
                        degats = pokemon.pv - self.health
                    elif attaque.special_effect[0] == "use_opponent_attack_stat":
                        degats = round(
                            (((((self.level * 0.4 + 2) * pokemon.attack * puissance) / self.defense) / 50) + 2) * cm)
                    else:
                        degats = round(
                            (((((self.level * 0.4 + 2) * self.attack * puissance) / self.defense) / 50) + 2) * cm)

                pokemon.damage(degats)

            for effet in attaque.special_effect:
                if not effet[0] == 'None':
                    if effet[0] == 'taken_dmg':
                        value = int(effet[1])
                        self.is_vulnerable = False
                        self.damage(value)
                    elif effet[0] == 'heal_on_maxpv':
                        coef = float(effet[1])
                        self.health += round(self.pv * coef)
                        if self.health > self.pv:
                            self.health = self.pv
                    elif effet[0] == 'heal_on_atk':
                        coef = float(effet[1][:-4])
                        self.heal(round(degats * coef))
                    elif effet[0] == 'self.pv':
                        self.damage(round(degats * float(effet[1][:-4])))
                    elif effet[0] == 'self-status':
                        r_value = random.randint(0, 99)
                        if r_value < int(effet[2]):
                            self.status[effet[1]] = True
                            attaque_infos = [True, (effet[1], self)]

            if pokemon.is_vulnerable:
                if attaque.special_effect[0][0] == "status":
                    r = random.randint(0, 99)
                    if r < int(attaque.special_effect[0][2]):
                        pokemon.status[attaque.special_effect[0][1]] = True
                        # print(attaque.special_effect[0][1], 'appliqué sur', pokemon.name)
                        attaque_infos = [True, (attaque.special_effect[0][1], pokemon)]
                    else:
                        attaque_infos = [True, None]
                else:
                    attaque_infos = [True, None]
            else:
                attaque_infos = [True, None]

        else:
            print(f'{attaque.name_} ratée')
            attaque_infos = [False, None]

        return attaque_infos

    def reset_status(self):
        """
        Méthode qui réinitialise les status du pokémon.
        """
        self.status = {
            'Sommeil': False,
            'Brulure': False,
            'Confusion': False,
            'Gel': False,
            'Poison': False,
            'Paralysie': False
        }

    def reset_attaque_fight(self):
        """
        Méthode qui reset les effets des attaques du pokémon en combat.
        """
        for attaque in self.attaque_pool:
            if attaque is not None:
                if attaque.bool_special_precision:
                    if attaque.special_precision[0] == 'd':
                        attaque.precision = int(attaque.special_precision[1].split("-")[0])

    def reset_turn_effects(self):
        """
        Reset les effets de combat du pokémon ne durant qu'un tour.
        """
        self.is_vulnerable = True

    def apply_turn_effects(self):
        """
        Methode qui applique les effets de tour de fight.
        """
        self.heal(self.passive_heal)

    def update_item_turn_effects(self):
        """
        Methode qui actualise les effets des objets à la fin d'un tour de combat.
        """

        assert self.objet_tenu is not None, "Erreur: tentative d'update sur un objet inexistant"

        if self.is_alive:
            if self.objet_tenu.effects['Give']['heal']['percent_activate'] != 0:
                if self.health <= self.pv * self.objet_tenu.effects['Give']['heal']['percent_activate'] / 100:
                    self.heal(self.objet_tenu.effects['Give']['heal']['value'])

                    self.objet_tenu = None

    def reset_stats(self):
        """
        Méthode qui reset les stats modifiées en combat.
        """
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.speed = self.base_speed

    def use_item(self, item):
        """
        Méthode d'utilisation d'un objet sur le pokémon.

        @in : item, objet.Objet
        """
        item.use(self)

    def give_item(self, item):
        """
        Méthode d'attachement d'un objet au pokémon.
        Applique les effets bonus de l'objet.

        @in : item, objet.Objet
        """
        self.objet_tenu = objet.Objet(item.name, self.game)

        item.give(self)

    def remove_item(self):
        if self.objet_tenu is not None:
            self.objet_tenu.remove(self)
            self.game.player.add_sac_item(self.objet_tenu)
            self.objet_tenu = None

    def def_shiny(self, is_shiny):
        """
        Méthode qui détermine si le pokémon est shiny ou pas.
        Retourn un booléen.

        @in : is_shiny, bool
        @out : bool
        """
        if self.game.player.always_shiny_on:
            return True
        elif is_shiny is None:
            n = random.randint(1, 256)
            if n == 137:
                return True
            else:
                return False
        elif is_shiny:
            return True
        else:
            return False

    def generate_random_seed_number(self):
        """
        Méthode qui détermine la seed random associée au pokémon.
        """
        return int(str(random.randint(0, 255))
                   + str(random.randint(0, 255))
                   + str(random.randint(0, 255))
                   + str(random.randint(0, 255)))


if __name__ == "__main__":
    pass
