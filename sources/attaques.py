"""
Fichier gérant les attaques des pokémons.
"""

# Importation des modules
import pygame
import random

# Définition des classes


class Attaque:
    """
    Classe représentant une attaque d'un pokémon.
    Une attaque est définie par son nom et son nombre de PP (optionnel, utile uniquement si on veut charger
        une attaque qui n'a pas son nombre de PP initial au maximum).
    Les PP sont les Points de Pouvoir. Si les PP d'une attaque tombent à 0, elle ne peut plus être lancée.
    """

    def __init__(self, name, pp=None):
        self.name = name
        self.name_ = self.reformate_name()
        self.line = self.find_attaque_line()

        self.type = self.line[1]
        if pp is None:
            self.pp = int(self.line[2])
        else:
            self.pp = pp

        self.bool_special_puissance = ':' in self.line[3]  # Bool
        self.special_puissance = ''
        if self.bool_special_puissance:
            self.special_puissance = self.line[3].split(':')
            if self.special_puissance[1] == "s.lv":
                self.puissance = "level"
            elif self.special_puissance[0] == "opp.pv":
                self.puissance = float(self.special_puissance[1])
                self.special_puissance = "ennemy_pv"
                # de la forme : ('ennemy_pv', 0.5)
            elif self.special_puissance[0] == "v":
                self.puissance = self.special_puissance[1]
                self.special_puissance = "v"
            elif self.special_puissance[0] == "r":
                values = self.special_puissance[1].split("-")
                self.puissance = random.randint(int(values[0]), int(values[1]))
            elif self.special_puissance[0] == 'c':
                self.puissance = int(self.special_puissance[1])
            elif self.special_puissance[1] == 'effort':
                self.puissance = "effort"
        else:
            self.puissance = int(self.line[3])

        self.bool_special_precision = ':' in self.line[4]  # Bool
        self.special_precision = None
        if self.bool_special_precision:
            self.special_precision = self.line[4].split(":")  # du type : ['d', '100-25']
            if self.special_precision[0] == 'd':
                self.precision = int(self.special_precision[1].split("-")[0])  # Pour les precisions diminutives
        else:
            self.precision = int(self.line[4])

        self.taux_crit = float(self.line[5])
        self.priorite = int(self.line[6])

        self.special_effect = self.line[7].split(',')
        self.special_effect = [effet.split(':') for effet in self.special_effect]

    # Méthodes d'accessions

    def get_stats(self) -> tuple:
        """
        Methode qui retourne toutes les stats de l'attaque :
        - Son type, str
        - Son nombre de PP, int
        - Sa puissance, int (ou str si puissance spéciale)
        - Sa precision, int
        - Ses chances de critique, float
        - Sa priorité, int
        - Ses effets spéciaux, list

        @out: tuple
        """
        return self.type, self.pp, self.puissance, self.precision, self.taux_crit, self.priorite, self.special_effect

    def get_name(self, mode_affichage=False) -> str:
        """
        Méthode qui retourne le nom de l'attaque.
        Retourne le nom à afficher si mode_affichage est True.
        Retourne le nom en interne du jeu sinon.

        Exemple avec l'attaque Croc Fatal :
                nom en interne du jeu : "Croc_Fatal"
                nom à afficher : "Croc Fatal"

        @in: mode_affichage, bool
        @out: str
        """
        if mode_affichage:
            return self.name_
        else:
            return self.name

    # Méthodes d'actualisation de variables

    def set_pp(self, amount: int):
        """
        Methode qui permet de définir le nombre de PP de l'attaque.
        @in: amoount, int
        """
        self.pp = amount

    # Méthodes liées à l'initialisation

    def reformate_name(self) -> str:
        """
        Methode de reformatage du nom de l'attaque.
        Tranforme le nom en interne du jeu en nom à afficher pour le joueur.
        @out: name, str
        """
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
        """
        Methode qui trouve, lit et renvoie le ligne d'infos de l'attaque.
        @out: list
        """
        with open('all_attaques.txt') as file:
            for line in file.readlines():
                if line.split()[0] == self.name:
                    return line.split()
