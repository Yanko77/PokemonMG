import pygame


class Attaque:

    def __init__(self, name):
        self.name = name[0].upper() + name[1:].lower()
        self.line = self.find_attaque_line()

        self.type = self.line[1]
        self.pp = int(self.line[2])
        self.puissance = int(self.line[3])
        self.precision = int(self.line[4])
        self.taux_crit = int(self.line[5])
        self.priorite = int(self.line[6])

    def find_attaque_line(self) -> list:
        with open('all_attaques.txt') as file:
            for line in file.readlines():
                if line.split()[0] == self.name:
                    return line.split()