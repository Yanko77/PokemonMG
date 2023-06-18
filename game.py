import accueil


class Game:
    def __init__(self):
        self.is_playing = False
        self.accueil = accueil.Accueil()

    def update(self, screen):

        if self.is_playing:
            ...
        else:
            self.accueil.update(screen)

