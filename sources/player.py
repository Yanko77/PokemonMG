import pygame


class Player:

    def __init__(self, game):
        self.game = game

        self.level = 0
        self.name = "Nom"

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


if __name__ == '__main__':
    p = Player('a')
    print(p.team[0])
