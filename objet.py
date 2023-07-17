import pygame
pygame.font.init()


class Objet:

    def __init__(self, name, quantite=1):
        self.name = name[0].upper() + name[1:]
        self.name_to_blit = self.reformate_name(self.name)
        self.icon_image = pygame.image.load(f'assets/items/{self.name}.png')
        self.quantite = int(quantite)

        self.line = self.find_item_line()

        self.d_spawn_infos = self.line[1].split(':')
        self.can_spawn_vs_d = int(self.d_spawn_infos[0])
        self.rarety_vs_d = int(self.d_spawn_infos[1])
        self.q_spawning_range = [int(self.d_spawn_infos[2].split('-')[0]),
                                 int(self.d_spawn_infos[2].split('-')[1])]

        self.categorie = self.line[2]
        self.fonctionnement = self.line[3].split('/')

        self.can_be_buy = int(self.line[4].split(':')[0])
        if self.can_be_buy:
            self.buy_price = int(self.line[4].split(':')[1])

        self.can_be_sell = int(self.line[5].split(':')[0])
        if self.can_be_sell:
            if self.line[5].split(':')[1] == 'v':
                self.variable_sell_price = True
                self.sell_price = [int(self.line[5].split(':')[2].split('-')[0]), int(self.line[5].split(':')[2].split('-')[1])]
            else:
                self.variable_sell_price = False
                self.sell_price = int(self.line[5].split(':')[1])

        self.desc_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 17)
        self.description = self.line[6][:-1]
        self.description = self.reformate_desc(self.description)

    def find_item_line(self):
        with open('all_objets.txt') as file:
            for line in file.readlines():
                if str(line.split()[0]) == str(self.name):
                    return line.split(maxsplit=6)

    def reformate_name(self, name):
        reformated_name = ''

        if name not in ['Collier_agathe']:
            for c in name:
                if c == '_':
                    reformated_name += ' '
                else:
                    reformated_name += c

        else:
            if name == 'Collier_agathe':
                reformated_name = "Collier d'Agathe"

        return reformated_name

    def reformate_desc(self, desc):
        l1 = desc
        l2 = ''
        l3 = ''

        while self.desc_font.render(l1, False, (0, 0, 0)).get_rect().w > 400:
            l2 = l1.split()[-1] + ' ' + l2
            l1 = l1[:-(len(l1.split()[-1])+1)]
        while self.desc_font.render(l2, False, (0, 0, 0)).get_rect().w > 400:
            l3 = l2.split()[-1] + ' ' + l3
            l2 = l2[:-(len(l2.split()[-1])+1)]

        return l1, l2, l3
