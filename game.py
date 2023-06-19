import accueil


class Game:
    def __init__(self):
        self.is_playing = False
        self.is_accueil = True

        self.accueil = accueil.Accueil()

    def update(self, screen):

        if self.is_playing:
            ...
        else:
            if self.is_accueil:
                self.accueil.update(screen)

