import pygame
from font import Font


class Player:

    def __init__(self, game):
        self.game = game

        self.level = 0
        self.name = Name(self)

        self.team = Team(self)


class Team:
    
    def __init__(self, player):
        self.player: Player = player
        
        self.members = [None for _ in range(6)]

    @property
    def nb_members(self) -> int:
        nb = 0
        for member in self.members:
            if member is not None:
                nb += 1

        return nb

    @property
    def is_empty(self) -> bool:
        return self.nb_members == 0
        
    def add(self, pokemon, index=None) -> bool:
        """
        Permet d'ajouter un pokémon à l'équipe.
        
        Si aucun indice n'est indiqué, essaye d'ajouter à la suite. Si l'équipe est pleine, ne fait rien.
        Sinon essaye de l'ajouter à l'indice indiqué. Si celui-ci est occupé, ne fait rien.
        
        Renvoie True si le pokémon a été ajouté, False sinon.
        """
        if index is None:
            i = 0
            while i < len(self.members):
                if self.members[i] is None:
                    self.members[i] = pokemon
                    return True
        else:
            if self.members[index] is None:
                self.members[index] = pokemon
                return True
        
        return False

    def __getitem__(self, index):
        return self.members[index]


class Name(str):

    def __init__(self, player):
        self.player = player

        self.text = "Nom"

        self.loaded_renders = {}

    def __repr__(self):
        return self.get()

    def get(self) -> str:
        return self.text

    def set(self, name):
        self.text = name

    def add(self, letter):
        self.text += letter

    def truncate(self):
        self.text = self.text[:-1]

    def render(self, font: Font, color: tuple):
        """
        Retourne une image du nom du joueur écrit avec la police font
        puis l'ajoute à la liste des renders pour la re-charger plus vite par la suite.
        """
        if (font.id, color) in self.loaded_renders:
            return self.loaded_renders[(font.id, color)]
        else:
            render = font.render(self.text, color)
            self.loaded_renders[(font.id, color)] = render

            return render


if __name__ == '__main__':
    p = Player('a')
    print(p.team[0])
