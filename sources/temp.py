import math

import pygame
pygame.font.init()

from math import cos, sin, tan, radians, degrees

upgrade_name_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 35)


class Upgrade:

    def __init__(self, name, next_list=None, cost=0):  # classe generale pour toutes les upgrades
        self.name = name

        self.pos = (0, 0)
        self.angle = 0

        if next_list is None:
            self.next = []
        else:
            self.next = []
            for upgrade in next_list:
                self.next.append(upgrade)

        self.cost = cost
        self.is_unlock = False

    def display(self, surface):
        angle_cos = cos(self.angle)
        angle_sin = sin(self.angle)

        center = (self.pos[0] + 50*angle_cos, self.pos[1] + 50*angle_sin)
        draw_forme('circle')(surface, center)

        surface.blit(upgrade_name_font.render(self.name, False, (255, 0, 0)), (center[0] - 10, center[1] - 25))

        if len(self.next) != 0:

            pos_deb = (self.pos[0] + 100*angle_cos, self.pos[1] + 100*angle_sin)

            i = 0
            for upgrade in self.next:
                angle = radians(120/len(self.next)*i) - radians(60) + radians(120/(len(self.next)+2)) + self.angle

                pos_fin = (pos_deb[0] + 100*cos(angle), pos_deb[1] + 100*sin(angle))

                draw_forme('line')(surface, pos_deb, pos_fin)

                upgrade.set_pos(pos_fin, angle)
                upgrade.display(surface)

                i += 1

    def unlock(self):
        """
        Méthode qui débloque l'upgrade
        """
        self.is_unlock = True

    def add_next(self, upgrade):
        self.next.append(upgrade)

    def add_previous(self, upgrade):
        self.previous.append(upgrade)

    def set_pos(self, pos, angle):
        self.pos = pos
        self.angle = angle

    def set_next(self, dict):
        for upgrade in dict:
            upgrade.set_next(dict[upgrade])
            self.next.append(upgrade)


class Graphe:

    def __init__(self, dict=None):
        self.root = Upgrade('Root')
        if dict is not None:
            self.init_graph(dict)

    def display(self, surface: pygame.Surface):
        self.root.set_pos((surface.get_width() // 2, surface.get_height() // 2), 0)

        i = 0
        nb_upgrades = len(self.root.next)
        for upgrade in self.root.next:
            angle = radians(360/nb_upgrades * i)

            pos = (self.root.pos[0] + 100*cos(angle), self.root.pos[1] + 100*sin(angle))
            upgrade.set_pos(pos, angle)
            draw_forme('line')(surface, self.root.pos, pos)
            upgrade.display(surface)

            i += 1

    def init_graph(self, dict):
        for upgrade in dict:
            upgrade.set_next(dict[upgrade])
            self.root.next.append(upgrade)



def draw_forme(forme: str):
    def line(surface, pos1, pos2):
        pygame.draw.line(surface, (255, 255, 255), pos1, pos2, width=10)

    def circle(surface, center, color=(255, 255, 255), radius=50, width=10):
        pygame.draw.circle(surface, center=center, color=color, radius=radius, width=width)

    formes_functions = {
        'line': line,
        'circle': circle,
    }

    return formes_functions[forme]




#draw_forme("line")(pos1, pos2)

def main():
    screen = pygame.display.set_mode((1280, 720))

    # Définition des fonctions

    running = True
    posSouris = (0, 0)

    g = Graphe({
        Upgrade('1'): {Upgrade('2'):  {},
                       Upgrade('3'):  {Upgrade('4'): {}}},
        Upgrade('5'): {Upgrade('6'):  {}}
    })




    # Boucle du jeu
    while running:
        posSouris = list(pygame.mouse.get_pos())

        g.display(screen)

        for event in pygame.event.get():  # Detection actions du joueur
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()  # Update de la fenetre

    pygame.quit()


if __name__ == '__main__':
    main()