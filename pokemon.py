import pygame
import random
import objet
import game_infos
import attaques


class Pokemon:

    def __init__(self, name, level, is_shiny=None, objet_tenu=None):
        self.name = name[0].upper() + name[1:].lower()
        self.is_shiny = self.def_shiny(is_shiny)

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
        self.rarety = int(self.line[1])
        self.type = str(self.line[2])
        self.type2 = str(self.line[10])

        self.bonus_pvmax = 0
        self.multiplicateur_pvmax = 1
        self.pv = round((2 * int(self.line[3]) * self.level)/100 + self.level + 10) + self.bonus_pvmax
        self.health = self.pv + self.bonus_pvmax

        self.bonus_attack = 0
        self.multiplicateur_attack = 1
        self.attack = round((2 * int(self.line[4]) * self.level)/100 + 5) + self.bonus_attack

        self.bonus_defense = 0
        self.multiplicateur_defense = 1
        self.defense = round((2 * int(self.line[5]) * self.level)/100 + 5) + self.bonus_defense

        self.bonus_speed = 0
        self.multiplicateur_speed = 1
        self.speed = round((2 * int(self.line[6]) * self.level)/100 + 5) + self.bonus_speed

        self.evolution_level = int(self.line[7])
        self.evolution_name = str(self.line[8])
        self.min_p_lv = int(self.line[9])

        self.is_alive = True

        if self.is_shiny:
            print(self.name, 'est shiny !!')
            self.icon_image = pygame.image.load(f'assets/game/pokemons_icons/{self.name}_.png')
        else:
            self.icon_image = pygame.image.load(f'assets/game/pokemons_icons/{self.name}.png')

        self.bonus_attaque_type = None
        self.multiplicateur_bonus_attaque = 1

        self.item_pourcent_hp_activate = None
        self.passive_heal = 0

    def find_pokemon_line(self) -> list:
        with open('all_pokemons.txt') as file:
            for line in file.readlines():
                if line.split()[0] == self.name:
                    return line.split()

    def level_up(self, nb_lv=1):
        self.level += nb_lv
        diff = self.pv - self.health
        self.pv = round((round((2*int(self.line[3])*self.level)/100 + self.level + 10) + self.bonus_pvmax) * self.multiplicateur_pvmax)
        self.health = self.pv - diff
        self.attack = round((round((2 * int(self.line[4]) * self.level)/100 + 5) + self.bonus_attack) * self.multiplicateur_attack)
        self.defense = round((round((2 * int(self.line[5]) * self.level)/100 + 5) + self.bonus_defense) * self.multiplicateur_defense)
        self.speed = round((round((2 * int(self.line[6]) * self.level)/100 + 5) + self.bonus_speed) * self.multiplicateur_speed)

    def evolution(self):
        if self.evolution_name == '0':
            print("Ce pokémon n'a pas d'évolution(s)")
            return self
        else:
            if self.level >= self.evolution_level:
                return Pokemon(self.evolution_name, self.level, self.is_shiny)
            else:
                return Pokemon(self.name, self.level, self.is_shiny)

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

    def heal(self, value):
        self.health += value
        if self.health > self.pv:
            self.health = self.pv

    def damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.is_alive = False
            self.health = 0

    def attaque(self, pokemon, attaque):
        cm = 1
        # Calcul avec stab ( attaque de type maternel )
        if attaque.type in [self.type, self.type2]:
            cm *= 1.5

        # Calcul avec affinités des types
        cm *= game_infos.get_mutiliplicateur(attaque.type, pokemon.type) * game_infos.get_mutiliplicateur(attaque.type, pokemon.type2)

        # Calcul avec taux de crit
        t = round(int(self.line[6]) / 2) * attaque.taux_crit
        ncrit = random.randint(0, 256)
        if ncrit < t:
            crit = True
        else:
            crit = False

        if crit:
            cm *= (2*self.level+5)/(self.level+5)

        if "augmentation_degats" in pokemon.objet.classes:
            cm *= pokemon.objet.multiplicateur_degats()

        random_cm = random.randint(85, 100)
        cm = cm * random_cm/100

        degats = round((((((self.level * 0.4 + 2) * self.attack * attaque.puissance) / self.defense) / 50) + 2) * cm)
        pokemon.damage(degats)
        print(degats)

    def reset_status(self):
        self.status = {
            'Sommeil': False,
            'Brulure': False,
            'Confusion': False,
            'Gel': False,
            'Poison': False,
            'Paralysie': False
            }

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
        if is_shiny is None:
            n = random.randint(1, 256)
            if n == 137:
                return True
            else:
                return False
        elif is_shiny:
            return True
        else:
            return False


if __name__ == "__main__":
    print(get_all_diff_pokemons('elec', 'hard'))
