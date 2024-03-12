import pygame
import random
import objet
import game_infos
import attaques


class Pokemon:

    def __init__(self, name, level, game, is_shiny=None, objet_tenu=None):
        self.game = game

        self.name = name[0].upper() + name[1:].lower()
        self.is_shiny = self.def_shiny(is_shiny)
        self.id = self.game.get_init_pokemon_id()

        self.objet_tenu = objet_tenu
        self.status = {
            'Sommeil': False,
            'Brulure': False,
            'Confusion': False,
            'Gel': False,
            'Poison': False,
            'Paralysie': False
            }

        self.line = self.find_pokemon_line()

        self.level = int(level)
        self.rarity = int(self.line[1])
        self.type = str(self.line[2])
        self.type2 = str(self.line[10])

        self.bonus_pvmax = 0
        self.multiplicateur_pvmax = 1
        self.pv = round((2 * int(self.line[3]) * self.level)/100 + self.level + 10) + self.bonus_pvmax  # PV MAX
        self.health = self.pv + self.bonus_pvmax  # PV ACTUELS

        self.bonus_attack = 0
        self.multiplicateur_attack = 1
        self.base_attack = round((2 * int(self.line[4]) * self.level)/100 + 5) + self.bonus_attack
        self.attack = self.base_attack

        self.bonus_defense = 0
        self.multiplicateur_defense = 1
        self.base_defense = round((2 * int(self.line[5]) * self.level)/100 + 5) + self.bonus_defense
        self.defense = self.base_defense

        self.bonus_speed = 0
        self.multiplicateur_speed = 1
        self.base_speed = round((2 * int(self.line[6]) * self.level)/100 + 5) + self.bonus_speed
        self.speed = self.base_speed

        self.evolution_level = int(self.line[7])
        self.evolution_name = str(self.line[8])
        self.min_p_lv = int(self.line[9])

        self.is_alive = True
        self.is_vulnerable = True

        if self.is_shiny:
            print(self.name, 'est shiny !!')
            self.icon_image = pygame.image.load(f'assets/game/pokemons_icons/{self.name}_.png')
        else:
            self.icon_image = pygame.image.load(f'assets/game/pokemons_icons/{self.name}.png')

        self.bonus_attaque_type = None
        self.multiplicateur_bonus_attaque = 1

        self.item_pourcent_hp_activate = None
        self.passive_heal = 0

        self.attaque_pool_line = self.find_attaque_pool_line()
        print(self.attaque_pool_line)
        self.attaque_pool = self.init_attaque_pool()

        self.random_seed = self.generate_random_seed_number()

    def find_pokemon_line(self) -> list:
        with open('all_pokemons.txt') as file:
            for line in file.readlines():
                if line.split()[0] == self.name:
                    return line.split()

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
                print(attaque_name)
                attaque_pool[i] = (attaques.Attaque(attaque_name))
                i += 1

        else:
            attaque_name_list = random.sample(self.attaque_pool_line, 4)
            i = 0
            for attaque_name in attaque_name_list:
                print(attaque_name)
                attaque_pool[i] = (attaques.Attaque(attaque_name))
                i += 1

        return attaque_pool

    def level_up(self, nb_lv=1):
        self.level += nb_lv
        diff = self.pv - self.health
        self.pv = round((round((2*int(self.line[3])*self.level)/100 + self.level + 10) + self.bonus_pvmax) * self.multiplicateur_pvmax)
        self.health = self.pv - diff
        self.base_attack = round((round((2 * int(self.line[4]) * self.level)/100 + 5) + self.bonus_attack) * self.multiplicateur_attack)
        self.base_defense = round((round((2 * int(self.line[5]) * self.level)/100 + 5) + self.bonus_defense) * self.multiplicateur_defense)
        self.base_speed = round((round((2 * int(self.line[6]) * self.level)/100 + 5) + self.bonus_speed) * self.multiplicateur_speed)

    def evolution(self):
        if self.evolution_name == '0':
            print("Ce pokémon n'a pas d'évolution(s)")
            return self
        else:
            if self.level >= self.evolution_level:
                return Pokemon(self.evolution_name, self.level, self.game, self.is_shiny)
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

    def attaque(self, pokemon, attaque):
        """
        Attaque le pokémon renseigné en parametre avec l'attaque prise en entrée.
        Renvoie True si l'attaque a abouti, False sinon
        """

        precision_value = random.randint(0, 100)
        if precision_value < attaque.precision and pokemon.is_vulnerable:

            if attaque.puissance != 0:

                cm = 1
                # Calcul avec stab ( attaque de type maternel )
                if attaque.type in [self.type, self.type2]:
                    cm *= 1.5

                # Calcul avec affinités des types
                cm *= game_infos.get_mutiliplicateur(attaque.type, pokemon.type)

                if not pokemon.type2 == 'NoType':
                    cm *= game_infos.get_mutiliplicateur(attaque.type, pokemon.type2)

                # Calcul avec taux de crit
                t = round(int(self.line[6]) / 2) * attaque.taux_crit
                ncrit = random.randint(0, 256)
                if ncrit < t:
                    crit = True
                else:
                    crit = False

                if crit:
                    cm *= (2 * self.level + 5) / (self.level + 5)

                if not self.objet_tenu is None:
                    cm *= self.objet_tenu.multiplicateur_attaque_dmg
                random_cm = random.randint(85, 100)
                cm = cm * random_cm / 100

                if attaque.puissance == "level":
                    puissance = self.level
                elif attaque.puissance == "ennemy_pv":
                    puissance = 1000000
                elif attaque.puissance == "pv*0.5":
                    puissance = pokemon.health // 2
                elif attaque.special_puissance == 'v':
                    if self.speed <= pokemon.speed:
                        puissance = int(attaque.puissance.split("-")[0])
                    else:
                        puissance = int(attaque.puissance.split("-")[1])
                else:
                    puissance = attaque.puissance

                if attaque.special_puissance == 'c':
                    degats = attaque.puissance
                elif attaque.puissance == "effort":
                    degats = pokemon.pv - self.health
                else:
                    degats = round((((((self.level * 0.4 + 2) * self.attack * puissance) / self.defense) / 50) + 2) * cm)

                pokemon.damage(degats)

            for effet in attaque.special_effect:
                if not effet[0] == 'None':
                    if effet[0] == 'taken_dmg':
                        value = int(effet[1])
                        self.is_vulnerable = False
                        self.health -= value

            if attaque.special_effect[0][0] == "status":
                pokemon.status[attaque.special_effect[0][1]] = True
                print(attaque.special_effect[0][1], 'appliqué sur', pokemon.name)

            return True
        else:
            print(f'{attaque.name_} ratée')
            return False

    def reset_status(self):
        self.status = {
            'Sommeil': False,
            'Brulure': False,
            'Confusion': False,
            'Gel': False,
            'Poison': False,
            'Paralysie': False
            }

    def reset_turn_effects(self):
        self.is_vulnerable = True

    def reset_stats(self):
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.speed = self.base_speed

    def use_item(self, item):

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

        self.heal(self.objet_tenu.heal_value)
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
