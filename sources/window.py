from panel import Component


class Window(Component):

    def __init__(self, panel):
        super().__init__(panel=panel,
                         prio=5)

        self.panels = {
            'spawn': None,
            'train': None,
            'grind': None,
            'items': None,
            'evol': None,
        }