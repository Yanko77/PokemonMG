import pygame
import random
import objet
import game_infos
import attaques
import csv


class Pokemon:

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
        self.pv = round((2 * self.infos[3] * self.level)/100 + self.level + 10) + self.bonus_pvmax  # PV MAX
        self.health = self.pv + self.bonus_pvmax  # PV ACTUELS

        self.bonus_attack = 0
        self.multiplicateur_attack = 1
        self.base_attack = round((2 * int(self.infos[4]) * self.level)/100 + 5) + self.bonus_attack
        self.attack = self.base_attack

        self.bonus_defense = 0
        self.multiplicateur_defense = 1
        self.base_defense = round((2 * int(self.infos[5]) * self.level)/100 + 5) + self.bonus_defense
        self.defense = self.base_defense

        self.bonus_speed = 0
        self.multiplicateur_speed = 1
        self.base_speed = round((2 * int(self.infos[6]) * self.level)/100 + 5) + self.bonus_speed
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
            self.icon_image = pygame.image.load(f'assets/game/pokemons_icons/{self.name}_.png')
        else:
            self.icon_image = pygame.image.load(f'assets/game/pokemons_icons/{self.name}.png')

        self.bonus_attaque_type = None
        self.multiplicateur_bonus_attaque = 1

        self.item_pourcent_hp_activate = None
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

    def init_attaque_pool(self):
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
        self.level += nb_lv
        diff = self.pv - self.health
        self.pv = round((round((2*int(self.infos[3])*self.level)/100 + self.level + 10) + self.bonus_pvmax) * self.multiplicateur_pvmax)
        self.health = self.pv - diff
        self.base_attack = round((round((2 * int(self.infos[4]) * self.level)/100 + 5) + self.bonus_attack) * self.multiplicateur_attack)
        self.base_defense = round((round((2 * int(self.infos[5]) * self.level)/100 + 5) + self.bonus_defense) * self.multiplicateur_defense)
        self.base_speed = round((round((2 * int(self.infos[6]) * self.level)/100 + 5) + self.bonus_speed) * self.multiplicateur_speed)

    def evolution(self):
        if self.evolution_name == '0':
            print("Ce pokémon n'a pas d'évolution(s)")
            return self
        else:
            if self.level >= self.evolution_level:
                return Pokemon(self.evolution_name, self.level, self.game, self.is_shiny, objet_tenu=self.objet_tenu)
            else:
                return self

    def full_heal(self):
        self.health = self.pv

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

    def heal(self, value):
        self.health += value
        if self.health > self.pv:
            self.health = self.pv

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.is_alive = False
            self.health = 0

    def attaque(self, pokemon, attaque) -> list:
        """
        Attaque le pokémon renseigné en parametre avec l'attaque prise en entrée.
        Renvoie une liste contenant :
            - True si l'attaque a abouti, False sinon
            - 'None' si l'attaque n'a pas appliqué d'effet à personne, (<nom_effet>, <self ou pokemon>) sinon
        """

        precision_value = random.randint(0, 100)
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
                    print(f'CRITIQUE DE {self.name}')

                if self.objet_tenu is not None:
                    if self.objet_tenu.type is None or self.objet_tenu.type == attaque.type:
                        cm *= self.objet_tenu.multiplicateur_attaque_dmg
                        print(f"Augmentation des dégats de l'attaque de {self.objet_tenu.multiplicateur_attaque_dmg*100}%")
                random_cm = random.randint(85, 100)
                cm = cm * random_cm / 100

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
                    else:
                        puissance = attaque.puissance
                else:
                    puissance = attaque.puissance

                if attaque.special_puissance == 'c':
                    degats = attaque.puissance
                elif attaque.puissance == "effort":
                    degats = pokemon.pv - self.health
                elif attaque.puissance == "ennemy_pv":
                    degats = pokemon.pv*2
                else:
                    degats = round((((((self.level * 0.4 + 2) * self.attack * puissance) / self.defense) / 50) + 2) * cm)

                pokemon.damage(degats)

            for effet in attaque.special_effect:
                if not effet[0] == 'None':
                    if effet[0] == 'taken_dmg':
                        value = int(effet[1])
                        self.is_vulnerable = False
                        self.damage(value)
                    elif effet[0] == 'heal_on_maxpv':
                        coef = float(effet[1])
                        self.health += round(self.pv*coef)
                        if self.health > self.pv:
                            self.health = self.pv
                    elif effet[0] == 'heal_on_atk':
                        coef = float(effet[1][:-4])
                        self.heal(round(degats*coef))
                    elif effet[0] == 'self.pv':
                        self.damage(round(degats*float(effet[1][:-4])))

            if pokemon.is_vulnerable:
                if attaque.special_effect[0][0] == "status":
                    r = random.randint(0, 99)
                    if r < int(attaque.special_effect[0][2]):
                        pokemon.status[attaque.special_effect[0][1]] = True
                        print(attaque.special_effect[0][1], 'appliqué sur', pokemon.name)
                        return [True, (attaque.special_effect[0][1], pokemon)]
                    else:
                        return [True, None]
                else:
                    return [True, None]
            else:
                return [True, None]

        else:
            print(f'{attaque.name_} ratée')
            return [False, None]

    def reset_status(self):
        self.status = {
            'Sommeil': False,
            'Brulure': False,
            'Confusion': False,
            'Gel': False,
            'Poison': False,
            'Paralysie': False
            }

    def reset_attaque_fight(self):
        for attaque in self.attaque_pool:
            if attaque is not None:
                print(1)
                if attaque.bool_special_precision:
                    print(2)
                    if attaque.special_precision[0] == 'd':
                        print(3)
                        attaque.precision = int(attaque.special_precision[1].split("-")[0])

    def reset_turn_effects(self):
        self.is_vulnerable = True

    def update_item_turn_effects(self):
        """
        Methode qui actualise les effets des objets à la fin d'un tour de combat
        """

        assert self.objet_tenu is not None, "Erreur: tentative d'update sur un objet inexistant"

        if self.is_alive:
            if self.item_pourcent_hp_activate is not None:
                print(self.pv*self.item_pourcent_hp_activate/100)
                if self.health <= self.pv*self.item_pourcent_hp_activate/100:
                    self.health += self.objet_tenu.heal_value
                    if self.health > self.pv:
                        self.health = self.pv

                    self.objet_tenu = None

    def reset_stats(self):
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.speed = self.base_speed

    def use_item(self, item):

        if item.bool_revive_effect:
            self.is_alive = True

        if self.is_alive:
            self.heal(item.heal_value)

        self.bonus_attaque_type = item.type
        self.multiplicateur_bonus_attaque = item.multiplicateur_attaque_dmg
        if item.stat == 'pv':
            self.pv += item.bonus_stat
            self.health += item.bonus_stat
            self.bonus_pvmax += item.bonus_stat
        elif item.stat == 'atk':
            self.attack += item.bonus_stat
            self.bonus_attack += item.bonus_stat
        elif item.stat == 'def':
            self.defense += item.bonus_stat
            self.bonus_defense += item.bonus_stat
        elif item.stat == 'vit':
            self.speed += item.bonus_stat
            self.bonus_speed += item.bonus_stat

        for status in self.status:
            if item.removed_status[status]:
                self.status[status] = False

        self.pv = round(self.pv * item.multiplicateur_pvmax)
        self.health = round(self.health * item.multiplicateur_pvmax)

        for stat in item.multiplicateur_stats:
            if not item.multiplicateur_stats[stat] == 1:
                if stat == 'pv':
                    diff = self.pv - self.health
                    self.multiplicateur_pvmax = item.multiplicateur_stats[stat]
                    self.pv = round(self.pv * item.multiplicateur_stats[stat])
                    self.health = self.pv - diff
                elif stat == 'atk':
                    self.multiplicateur_attack = item.multiplicateur_stats[stat]
                    self.attack = round(self.attack * item.multiplicateur_stats[stat])
                elif stat == 'def':
                    self.multiplicateur_defense = item.multiplicateur_stats[stat]
                    self.defense = round(self.defense * item.multiplicateur_stats[stat])
                elif stat == 'vit':
                    self.multiplicateur_speed = item.multiplicateur_stats[stat]
                    self.speed = round(self.speed * item.multiplicateur_stats[stat])

        if not item.bonus_lv == 0:
            self.level_up(item.bonus_lv)

    def give_item(self, item):
        self.objet_tenu = item

        self.bonus_attaque_type = self.objet_tenu.type
        self.multiplicateur_bonus_attaque = self.objet_tenu.multiplicateur_attaque_dmg

        if self.objet_tenu.stat == 'pv':
            self.pv += self.objet_tenu.bonus_stat
            self.health += self.objet_tenu.bonus_stat
            self.bonus_pvmax += self.objet_tenu.bonus_stat
        elif self.objet_tenu.stat == 'atk':
            self.attack += self.objet_tenu.bonus_stat
            self.bonus_attack += self.objet_tenu.bonus_stat
        elif self.objet_tenu.stat == 'def':
            self.defense += self.objet_tenu.bonus_stat
            self.bonus_defense += self.objet_tenu.bonus_stat
        elif self.objet_tenu.stat == 'vit':
            self.speed += self.objet_tenu.bonus_stat
            self.bonus_speed += self.objet_tenu.bonus_stat

        self.item_pourcent_hp_activate = self.objet_tenu.pv_pourcent_activate

        for status in self.status:
            if self.objet_tenu.removed_status[status]:
                self.status[status] = False

        if self.objet_tenu.multiplicateur_pvmax != 1:
            diff = self.pv - self.health
            self.pv = round(self.pv * self.objet_tenu.multiplicateur_pvmax)
            self.health = self.pv - diff

        self.passive_heal = self.objet_tenu.heal_after_each_fight

        for stat in self.objet_tenu.multiplicateur_stats:
            if not self.objet_tenu.multiplicateur_stats[stat] == 1:
                if stat == 'pv':
                    diff = self.pv - self.health
                    self.bonus_pvmax += round(self.pv * self.objet_tenu.multiplicateur_stats[stat]) - self.pv
                    self.pv = round(self.pv * self.objet_tenu.multiplicateur_stats[stat])
                    self.health = self.pv - diff
                elif stat == 'atk':
                    self.bonus_attack += round(self.attack * self.objet_tenu.multiplicateur_stats[stat]) - self.attack
                    self.attack = round(self.attack * self.objet_tenu.multiplicateur_stats[stat])
                elif stat == 'def':
                    self.bonus_defense += round(self.defense * self.objet_tenu.multiplicateur_stats[stat]) - self.defense
                    self.defense = round(self.defense * self.objet_tenu.multiplicateur_stats[stat])
                elif stat == 'vit':
                    self.bonus_speed += round(self.speed * self.objet_tenu.multiplicateur_stats[stat]) - self.speed
                    self.speed = round(self.speed * self.objet_tenu.multiplicateur_stats[stat])

    def def_shiny(self, is_shiny):
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
        return int(str(random.randint(0, 255))
                   + str(random.randint(0, 255))
                   + str(random.randint(0, 255))
                   + str(random.randint(0, 255)))


if __name__ == "__main__":
    pass
