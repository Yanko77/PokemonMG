import pygame
import random
import objet
import game_infos
import attaques

class Pokemon:

    def __init__(self, name, level, is_shiny=None, objet_tenu=objet.Objet("Nothing")):
        self.name = name[0].upper() + name[1:].lower()
        self.is_shiny = self.def_shiny(is_shiny)

        self.objet_tenu = objet_tenu

        self.line = self.find_pokemon_line()

        self.level = int(level)
        self.rarety = int(self.line[1])
        self.type = str(self.line[2])
        self.type2 = str(self.line[10])

        self.pv = round((2 * int(self.line[3]) * self.level)/100 + self.level + 10)
        self.health = self.pv
        self.attack = round((2 * int(self.line[4]) * self.level)/100 + 5)

        self.defense = round((2 * int(self.line[5]) * self.level)/100 + 5)
        self.speed = round((2 * int(self.line[6]) * self.level)/100 + 5)

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
        self.pv = round((2*int(self.line[3])*self.level)/100 + self.level + 10)
        self.health = self.pv - diff
        self.attack = round((2 * int(self.line[4]) * self.level)/100 + 5)
        self.defense = round((2 * int(self.line[5]) * self.level)/100 + 5)
        self.speed = round((2 * int(self.line[6]) * self.level)/100 + 5)

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
    pokemon_A = Pokemon('Reptincel', 24)
    print(pokemon_A.get_stats())
    pokemon_A = pokemon_A.evolution()
    print(pokemon_A.get_stats())
