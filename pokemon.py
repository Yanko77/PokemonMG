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
        self.status = None

        self.line = self.find_pokemon_line()

        self.level = int(level)
        self.rarety = int(self.line[1])
        self.type = str(self.line[2])
        self.type2 = str(self.line[10])

        self.bonus_pvmax = 0
        self.pv = round((2 * int(self.line[3]) * self.level)/100 + self.level + 10) + self.bonus_pvmax
        self.health = self.pv + self.bonus_pvmax

        self.bonus_attack = 0
        self.attack = round((2 * int(self.line[4]) * self.level)/100 + 5) + self.bonus_attack
        self.bonus_defense = 0
        self.defense = round((2 * int(self.line[5]) * self.level)/100 + 5) + self.bonus_defense
        self.bonus_speed = 0
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

    def find_pokemon_line(self) -> list:
        with open('all_pokemons.txt') as file:
            for line in file.readlines():
                if line.split()[0] == self.name:
                    return line.split()

    def level_up(self, nb_lv=1):
        self.level += nb_lv
        diff = self.pv - self.health
        self.pv = round((2*int(self.line[3])*self.level)/100 + self.level + 10) + self.bonus_pvmax
        self.health = self.pv - diff
        self.attack = round((2 * int(self.line[4]) * self.level)/100 + 5) + self.bonus_attack
        self.defense = round((2 * int(self.line[5]) * self.level)/100 + 5) + self.bonus_defense
        self.speed = round((2 * int(self.line[6]) * self.level)/100 + 5) + self.bonus_speed

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

    def damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.is_alive = False
            self.health = 0

    def attaque(self, pokemon, attaque):
        cm = 1
        if attaque.type == self.type:
            cm *= 1.5
        cm *= game_infos.types_affinities[attaque.type][pokemon.type] * game_infos.types_affinities[attaque.type][pokemon.type2]
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
        cm = cm*random_cm/100

        degats = round((((((self.level * 0.4 + 2) * self.attack * attaque.puissance) / self.defense) / 50) + 2) * cm)
        pokemon.damage(degats)
        print(degats)

    def use_item(self, item_name):

        if item_name == 'Guerison':
            self.status = None
        elif item_name == 'Potion':
            if self.health + 30 >= self.pv:
                self.health = self.pv
            else:
                self.health += 30
        elif item_name == 'Hyper_Potion':
            if self.health + 120 >= self.pv:
                self.health = self.pv
            else:
                self.health += 120
        elif item_name == 'Potion_Max':
            self.health = self.pv
        elif item_name == 'PV_Plus':
            self.bonus_pvmax += 1 + round(self.pv * 5 / 100)
            diff = self.pv - self.health
            self.pv = round((2 * int(self.line[3]) * self.level) / 100 + self.level + 10) + self.bonus_pvmax
            self.health = self.pv - diff
            print('augmentation pv de', str(self.bonus_pvmax))
        elif item_name == 'Proteine':
            self.bonus_attack += 5
            self.attack = round((2 * int(self.line[4]) * self.level)/100 + 5) + self.bonus_attack
            print('augmentation atk de', str(self.bonus_attack))
        elif item_name == 'Fer':
            self.bonus_defense += 5
            self.defense = round((2 * int(self.line[5]) * self.level) / 100 + 5) + self.bonus_defense
            print('augmentation def de', str(self.bonus_defense))
        elif item_name == 'Carbone':
            self.bonus_speed += 5
            self.speed = round((2 * int(self.line[6]) * self.level) / 100 + 5) + self.bonus_speed
            print('augmentation vit de', str(self.bonus_speed))
        elif item_name == 'Super_Bonbon':
            self.level_up(1)
        elif item_name == 'Eau_Fraiche':
            if self.health + 50 >= self.pv:
                self.health = self.pv
            else:
                self.health += 50
        else:
            print('ERREUR ITEM USE')

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


def get_all_diff_pokemons(pokemon_type, difficulte=2):
    weak_types_list = _get_difficulte_types(pokemon_type,difficulte)
    if weak_types_list is None:
        return None
    weak_pokemons_list = []
    with open('all_pokemons.txt', 'r') as file:
        for line in file.readlines():
            if not line.split()[0] == '#':
                if line.split()[2] in weak_types_list:
                    weak_pokemons_list.append(line.split()[0])

    return weak_pokemons_list

def _get_difficulte_types(pokemon_type, difficult=2):
    weak_types_list = []
    for type in game_infos.types_affinities[pokemon_type]:
        if game_infos.types_affinities[pokemon_type][type] == difficult:
            weak_types_list.append(type)
    if weak_types_list is []:
        return None

    return weak_types_list


if __name__ == "__main__":
    print(get_all_diff_pokemons('plante'))
    print(get_all_diff_pokemons('normal', 1))
