import pygame
pygame.font.init()


class Objet:

    def __init__(self, name, quantite=1):
        self.name = name[0].upper() + name[1:]
        self.name_to_blit = self.reformate_name(self.name)
        self.icon_image = pygame.image.load(f'assets/items/{self.name}.png')
        self.quantite = int(quantite)

        self.line = self.find_item_line()

        self.boolSpawnable = int(self.line[1].split(':')[0])
        self.rarety = int(self.line[1].split(':')[1])
        self.quantite_at_spawn = (int(self.line[1].split(':')[2].split('-')[0]),
                                  int(self.line[1].split(':')[2].split('-')[1]))

        self.categorie = self.line[2]
        self.fonctionnement = self.line[3].split(':')[0]

        self.effect = None
        self.heal_value = 0
        self.type = None
        self.multiplicateur_attaque_dmg = 1
        self.stat = None
        self.bonus_stat = 0
        self.pv_pourcent_activate = None
        self.removed_status = {
            'Sommeil': False,
            'Brulure': False,
            'Confusion': False,
            'Gel': False,
            'Poison': False,
            'Paralysie': False}
        self.multiplicateur_pvmax = 1
        self.heal_after_each_fight = 0
        self.target_pokemon = 'All'
        self.multiplicateur_stats = {
            'pv': 1,
            'atk': 1,
            'def': 1,
            'vit': 1
        }
        self.bonus_lv = 0

        self.set_special_effects()

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

    def set_special_effects(self):
        if self.fonctionnement in ('Use', 'Give'):
            self.effect = self.line[3].split(':')[1]
            if self.effect == 'special':
                if self.name == 'Collier_Agathe':
                    self.multiplicateur_pvmax = 0.80
                    self.heal_after_each_fight = 10000
                elif self.name == 'Casquette_de_Nathan':
                    self.target_pokemon = 'Tyranocif'
                    self.multiplicateur_stats = {
                        'pv': 1.25,
                        'atk': 1.25,
                        'def': 1.25,
                        'vit': 1.25
                    }
                elif self.name == 'Caillou':
                    self.multiplicateur_stats['vit'] = 0.99
            else:
                if self.effect == 'h':
                    if self.fonctionnement == 'Give':
                        self.heal_value = int(self.line[3].split(':')[2].split('-')[0])
                        self.pv_pourcent_activate = int(self.line[3].split(':')[2].split('-')[1][:-1])
                    else:
                        self.heal_value = int(self.line[3].split(':')[2])
                elif self.effect == 'b':
                    self.stat = self.line[3].split(':')[2]
                    if self.stat == 'pv':
                        self.bonus_stat = 1
                        self.multiplicateur_stats['pv'] = 1.05
                    else:
                        self.bonus_stat = 5
                elif self.effect == 'p':
                    self.type = self.line[3].split(':')[2]
                    self.multiplicateur_attaque_dmg = 1.20
                elif self.effect == 's':
                    if self.line[3].split(':')[2] == 'All':
                        self.removed_status = {
                            'Sommeil': True,
                            'Brulure': True,
                            'Confusion': True,
                            'Gel': True,
                            'Poison': True,
                            'Paralysie': True}
                    else:
                        self.removed_status[self.line[3].split(':')[2]] = True
                else:  # self.effect == l
                    self.bonus_lv = int(self.line[3].split(':')[2])

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

if __name__ == '__main__':
    a = Objet('Baie_Oran')
    print(a.pv_pourcent_activate)