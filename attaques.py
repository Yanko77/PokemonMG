import pygame
import random


class Attaque:

    def __init__(self, name):
        self.name = name
        self.name_ = self.reformate_name()
        self.line = self.find_attaque_line()

        self.type = self.line[1]
        self.pp = int(self.line[2])

        self.special_puissance = ':' in self.line[3]  # Bool
        if self.special_puissance:
            self.puissance = self.line[3]
        else:
            self.puissance = int(self.line[3])

        self.bool_special_precision = ':' in self.line[4]  # Bool
        self.special_precision = None
        if self.bool_special_precision:
            self.special_precision = self.line[4].split(":")
            if self.special_precision[0] == 'd':
                self.precision = int(self.special_precision[1].split("-")[0])  # Pour les precisions diminutives
        else:
            self.precision = int(self.line[4])

        self.taux_crit = float(self.line[5])
        self.priorite = int(self.line[6])

        self.special_effect = self.line[7].split(',')
        self.special_effect = [effet.split(':') for effet in self.special_effect]

    def get_stats(self):
        return self.type, self.pp, self.puissance, self.precision, self.taux_crit, self.priorite, self.special_effect

    def get_name(self, mode_affichage=False):
        if mode_affichage:
            return self.name_
        else:
            return self.name

    def reformate_name(self):
        name = ''
        for mot in self.name.split("_"):
            if mot == 'a':
                name += 'à'
            else:
                name += mot

            if not name == '':
                name += ' '

        return name

    def find_attaque_line(self) -> list:
        with open('all_attaques.txt') as file:
            for line in file.readlines():
                if line.split()[0] == self.name:
                    return line.split()


if __name__ == '__main__':
    croc = Attaque('Vive-Attaque')
    print(croc.get_stats())
