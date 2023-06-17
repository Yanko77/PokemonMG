import pygame


class Pokemon:

    def __init__(self, name, level):
        self.name = name[0].upper() + name[1:].lower()
        self.line = self.find_pokemon_line()

        # self.game =
        # self.player = game.player


        self.attaque_percent = {'light': 0.7,
                                'normal': 1,
                                'heavy': 1.4}  # Peut varier avec les patch d'equilibrage

        self.stam = int(self.line[14])*10
        self.stam_needed = {'light': 6,
                            'normal': 10,
                            'heavy': 16}

        self.level = int(level)
        self.rarety = int(self.line[1])
        self.e_type = str(self.line[2])

        self.xp_pv = int(self.line[7]) / 100
        self.xp_attack = int(self.line[8]) / 100
        self.xp_defense = int(self.line[9]) / 100
        self.xp_speed = int(self.line[10]) / 100

        self.pv = round(int(self.line[3]) + self.level * self.xp_pv)
        self.attack = round(int(self.line[4]) + self.level * self.xp_attack)
        self.defense = round(int(self.line[5]) + self.level * self.xp_defense)
        self.speed = round(int(self.line[6]) + self.level * self.xp_speed)

        self.evolution_level = int(self.line[11])
        self.evolution_name = str(self.line[12])
        self.min_p_lv = int(self.line[13])

        # self.image = pygame.image.load(f'assets/{name}.png')

    def find_pokemon_line(self) -> list:
        with open('all_pokemons.txt') as file:
            for line in file.readlines():
                if line.split()[0] == self.name:
                    return line.split()

    def level_up(self, nb_lv=1):
        self.level += nb_lv
        self.pv = round(int(self.line[3]) + self.level * self.xp_pv)
        self.health = self.pv - diff
        self.attack = round(int(self.line[4]) + self.level * self.xp_attack)
        self.defense = round(int(self.line[5]) + self.level * self.xp_defense)
        self.speed = round(int(self.line[6]) + self.level * self.xp_speed)

    def evolution(self):
        if self.level >= self.evolution_level:
            return Pokemon(self.evolution_name, self.level)

    def get_stats(self):
        return self.pv, self.attack, self.defense, self.speed

    def damage(self, amount):
        self.health -= amount

    def attaque(self, pokemon, att_type):
        if self.stam - self.stam_needed[att_type] >= 0:
            pokemon.damage(round(self.attack*self.attaque_percent[att_type]))
            self.stam -= self.stam_needed[att_type]




if __name__ == "__main__":
    pokemon_A = Pokemon('Reptincel', 24)
    print(pokemon_A.get_stats())
    pokemon_A = pokemon_A.evolution()
    print(pokemon_A.get_stats())
