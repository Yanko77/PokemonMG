import pygame
import random


class Attaque:

    def __init__(self, name):
        self.name = name
        self.line = self.find_attaque_line()

        self.type = self.line[1]
        self.pp = int(self.line[2])

        self.special_puissance = ':' in self.line[3]  # Bool
        if self.special_puissance:
            self.puissance = self.line[3]
        else:
            self.puissance = int(self.line[3])

        self.special_precision = ':' in self.line[4]  # Bool
        if self.special_precision:
            self.precision = self.line[4]
        else:
            self.precision = int(self.line[4])

        self.taux_crit = int(self.line[5])
        self.priorite = int(self.line[6])

        self.special_effect = self.line[7].split(',')
        tem = []
        for effet in self.special_effect:
            tem.append(tuple(effet.split(":")))
        self.special_effect = tuple(tem)


    def get_stats(self):
        return self.type, self.pp, self.puissance, self.precision, self.taux_crit, self.priorite, self.special_effect

    def find_attaque_line(self) -> list:
        with open('all_attaques.txt') as file:
            for line in file.readlines():
                if line.split()[0] == self.name:
                    return line.split()


if __name__ == '__main__':
    croc = Attaque('Detection')
    print(croc.get_stats())