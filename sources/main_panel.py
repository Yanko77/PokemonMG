from panel import Panel


class MainPanel(Panel):

    def __init__(self, game):
        super().__init__(game=game,
                         path='assets/game/panels/classic_panel/')

        self.background = self.img_load('background')

    def update(self, possouris):
        self.game.screen.blit(self.background, (0, 0))
