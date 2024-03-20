import random

import attaques
import dresseur
import fight
import objet
import pokemon
import starters
import csv
from player import Player
from notif import Notif

import pygame
import accueil
from game_panel import GamePanel
from fight import Fight
from game_round import Round


class Game:
    def __init__(self):
        self.is_playing = False
        self.is_accueil = True
        self.is_fighting = False

        self.is_starter_selected = False

        self.pressed = {pygame.K_LSHIFT: False}
        self.mouse_pressed = {1: False,
                              3: False}

        self.items_list = self.get_all_items_list()
        self.pokemons_list = self.init_pokemons_list()
        self.special_pokemons_list = self.init_special_pokemons_list()

        self.player = Player(self)

        self.accueil = accueil.Accueil(self)

        self.next_pk_id = 1

        self.all_starters = {'feu': ['Salameche', 'Poussifeu'],
                             'eau': ['Carapuce', 'Gobou'],
                             'plante': ['Bulbizarre', 'Arcko']}
        self.starters = [random.choice(self.all_starters['plante']),
                         random.choice(self.all_starters['feu']),
                         random.choice(self.all_starters['eau'])
                         ]

        self.starter_panel = starters.StarterPanel(self)

        self.classic_panel = GamePanel(self)
        self.round = Round(self)
        self.notifs = Notif()

        self.general_seed = self.round.get_random_seed()

        self.next_fighting_dresseur = self.get_fighting_dresseur()

        self.current_fight = None

        self.bool_game_over = False

    def update(self, screen, possouris):

        if self.is_playing:
            if self.is_starter_selected:
                if self.is_fighting:
                    self.current_fight.update(screen, possouris)
                else:
                    self.classic_panel.update(screen, possouris)
            else:
                self.starter_panel.update(screen, possouris)
        else:
            if self.is_accueil:
                self.accueil.update(screen, possouris)
            else:
                self.is_playing = True

        # Affichage des notifications
        self.notifs.update(screen)

    def notif(self, text, color):
        self.notifs.new_notif(text, color)

    def get_fighting_dresseur(self):
        r = random.Random()
        # return r.choice(fight.DRESSEUR_LIST)(self)
        return fight.Red(self)

    def init_new_game(self):
        self.is_starter_selected = False
        self.reset_save_file()

    def create_new_game(self):
        self.init_new_game()

    def start_new_game(self):
        self.is_accueil = False
        self.create_new_game()

    def game_over(self):
        self.__init__()

    def start_fight(self, player_pk, dresseur=None, difficult="easy", fight_type='Classic'):
        if fight_type == 'Classic':
            self.init_fight(player_pk, dresseur, difficult, fight_type)
            self.is_fighting = True
        elif fight_type == 'Boss':
            self.init_fight(player_pk, self.next_fighting_dresseur, difficult, fight_type)
            self.is_fighting = True

    def cancel_fight(self):
        self.current_fight = None
        self.is_fighting = False

    def end_fight(self):
        if self.current_fight.fight_type == 'Boss':
            self.next_turn()
        self.current_fight = None
        self.is_fighting = False

    def init_fight(self, player_pk, dresseur=None, difficult='easy', fight_type='Classic'):
        self.current_fight = Fight(self, player_pk, dresseur, difficult, fight_type)

    def next_turn(self):
        self.round.next()
        self.update_random_seed()
        self.player.reset_actions()
        self.player.level_up()
        self.classic_panel.next_turn()
        self.next_fighting_dresseur = self.get_fighting_dresseur()
        # add everything that have to be edited for each turn

    def get_init_pokemon_id(self):
        id = self.next_pk_id
        self.next_pk_id += 1
        return id

    def init_items_list(self):
        with open('all_objets.txt', 'r') as file:
            items_list = []
            for line in file.readlines():
                item_name = line.split()[0]
                if not item_name == '#':
                    items_list.append(objet.Objet(item_name))

            return items_list

    def get_all_items_list(self):
        """
        Retourne le dict: {
            'All': all_items
            'Use': use_items,
            'Give': give_items,
            'Sell': sell_items,
            'Enable': enable_items,
            'Spawnble': spawnable_items
             }

        :return: items_list, dict
        """

        items_list = {
            'All': [],
            'Use': [],
            'Give': [],
            'Sell': [],
            'Enable': [],
            'Spawnable': [],
        }
        for item in self.init_items_list():
            items_list['All'].append(item)
            if item.fonctionnement.split(":")[0] == 'Use':
                items_list['Use'].append(item)
            elif item.fonctionnement.split(":")[0] == 'Give':
                items_list['Give'].append(item)
            elif item.fonctionnement.split(":")[0] == 'Sell':
                items_list['Sell'].append(item)
            elif item.fonctionnement.split(":")[0] == 'Enable':
                items_list['Enable'].append(item)
            if item.boolSpawnable:
                items_list['Spawnable'].append(item)

        return items_list

    def get_items_list(self):
        return self.items_list

    def init_pokemons_list(self):
        with open('all_pokemons.csv', newline='') as file:
            pokemons_list = {}
            lines = csv.reader(file, delimiter=',', quotechar='|')
            for line in lines:
                if line[0] not in (" ", "", "NAME", "Moyennes"):

                    pokemons_list[line[0]] = (
                        line[0],  # NAME
                        int(line[1]),  # RARITY
                        line[2],  # TYPE
                        int(line[3]),  # PV
                        int(line[4]),  # ATK
                        int(line[5]),  # DEF
                        int(line[6]),  # SPEED
                        int(line[7]),  # EVOLUTION LEVEL
                        line[8],  # EVOLUTION NAME
                        int(line[9]),  # MIN PLAYER LEVEL TO SPAWN
                        line[10],  # TYPE 2
                        int(line[11]),  # MIN LEVEL ON SPAWN
                        int(line[12]),  # MAX LEVEL ON SPAWN
                    )
            print(pokemons_list)
            return pokemons_list

    def init_special_pokemons_list(self):
        with open('special_pokemons.csv', newline='') as file:
            pokemons_list = {}
            lines = csv.reader(file, delimiter=',', quotechar='|')
            for line in lines:
                if line[0] not in (" ", "", "NAME", "Moyennes"):

                    pokemons_list[line[0]] = (
                        line[0],  # NAME
                        int(line[1]),  # RARITY
                        line[2],  # TYPE
                        int(line[3]),  # PV
                        int(line[4]),  # ATK
                        int(line[5]),  # DEF
                        int(line[6]),  # SPEED
                        int(line[7]),  # EVOLUTION LEVEL
                        line[8],  # EVOLUTION NAME
                        int(line[9]),  # MIN PLAYER LEVEL TO SPAWN
                        line[10],  # TYPE 2
                        int(line[11]),  # MIN LEVEL ON SPAWN
                        int(line[12]),  # MAX LEVEL ON SPAWN
                    )
            print(pokemons_list)
            return pokemons_list

    def get_total_items_rarity(self):
        """
        Methode qui renvoie la somme de toutes les raretés des objets du jeu obtenable via spawn
        """
        total_rarity = 0
        for OBJECT in self.get_items_list()['Spawnable']:
            total_rarity += abs(OBJECT.rarity - 100)
        return total_rarity

    def update_random_seed(self):
        self.general_seed = self.round.get_random_seed()

    def save(self):
        # save team
        with open('save/team.csv', newline='') as file:
            rows = csv.reader(file, delimiter=',')
            i = 0
            listecsv = []
            for line in rows:
                if not i == 0:
                    pk = self.player.team[i-1]
                    if pk != None:
                        line[0] = pk.name
                        line[1] = str(pk.is_shiny)
                        line[2] = str(pk.get_id())
                        if pk.objet_tenu == None:
                            line[3] = "None"
                        else:
                            line[3] = pk.objet_tenu.name
                        line[4] = str(pk.get_level())
                        pk_bonus = f"{pk.health} "
                        for y in pk.get_bonus_stats():
                            pk_bonus += f'{y} '
                        line[5] = pk_bonus
                        line[6] = str(pk.is_alive)
                        pk_att_pool = ""
                        for att in pk.get_attaque_pool():
                            if att is not None:
                                pk_att_pool += f'{att.name}:{att.pp} '
                        line[7] = pk_att_pool
                    else:
                        line = ["", "", "", "", "", "", "", ""]

                listecsv.append(line)

                i += 1
            print(listecsv)
            file.close()  # Close the file

        self.write_down_backup('team.csv', listecsv)

        # save player
        with open('save/player.csv') as file:
            rows = csv.reader(file, delimiter=',')
            i = 0
            listecsv = []
            for line in rows:
                if not i == 0:
                    line[0] = self.player.name
                    line[1] = str(self.player.get_level())
                    line[2] = str(self.player.get_actions())
                    line[3] = str(self.player.get_max_actions())
                    line[4] = str(self.player.always_shiny_on)
                    line[5] = str(self.player.get_money())
                listecsv.append(line)
                i += 1
            file.close()

        self.write_down_backup('player.csv', listecsv)

        # save game
        with open('save/game.csv') as file:
            rows = csv.reader(file, delimiter=',')
            i = 0
            listecsv = []
            for line in rows:
                if not i == 0:
                    line[0] = str(self.next_pk_id)
                    line[1] = str(self.general_seed)
                    line[2] = f'{self.next_fighting_dresseur.name} {self.next_fighting_dresseur.pk.name} {self.next_fighting_dresseur.pk.get_level()} '
                    objet_tenu = self.next_fighting_dresseur.pk.objet_tenu
                    if objet_tenu != None:
                        line[2] += f'{self.next_fighting_dresseur.pk.objet_tenu.name}'
                    else:
                        line[2] += "None"

                    # line[5]
                    training_pk = self.classic_panel.ingame_window.train_panel.training_pk

                    if not training_pk == None:
                        training_pk_bonus = f"{training_pk.health} "
                        for y in training_pk.get_bonus_stats():
                            training_pk_bonus += f'{y} '
                        pk_att_pool = ""
                        for att in training_pk.get_attaque_pool():
                            if att is not None:
                                pk_att_pool += f'{att.name}:{att.pp} '

                        training_pk_item = training_pk.objet_tenu
                        if training_pk_item is None:
                            training_pk_item = 'None'
                        else:
                            training_pk_item = f'{training_pk_item.name}'

                        line[3] = f'{training_pk.name} {training_pk.is_shiny} {training_pk.get_id()} {training_pk.get_level()} {training_pk_bonus} {training_pk.is_alive} {pk_att_pool} {training_pk_item}'
                    else:
                        line[3] = 'None'


                    # line[6]
                    spawning_pk = self.classic_panel.ingame_window.spawn_panel.spawning_pk
                    if not spawning_pk == None:
                        spawning_pk_bonus = f"{spawning_pk.health} "
                        for y in spawning_pk.get_bonus_stats():
                            spawning_pk_bonus += f'{y} '
                        pk_att_pool = ""
                        for att in spawning_pk.get_attaque_pool():
                            if att is not None:
                                pk_att_pool += f'{att.name}:{att.pp} '
                        spawning_pk_item = spawning_pk.objet_tenu
                        if spawning_pk_item is None:
                            spawning_pk_item = 'None'
                        else:
                            spawning_pk_item = f'{spawning_pk_item.name}'
                        line[4] = f'{spawning_pk.name} {spawning_pk.is_shiny} {spawning_pk.get_id()} {spawning_pk.get_level()} {spawning_pk_bonus} {spawning_pk.is_alive} {pk_att_pool} {spawning_pk_item}'
                    else:
                        line[4] = 'None'


                    # line[7]
                    evolving_pk = self.classic_panel.ingame_window.evol_panel.evolving_pk
                    if not evolving_pk == None:
                        evolving_pk_bonus = f"{evolving_pk.health} "
                        for y in evolving_pk.get_bonus_stats():
                            evolving_pk_bonus += f'{y} '
                        pk_att_pool = ""
                        for att in evolving_pk.get_attaque_pool():
                            if att is not None:
                                pk_att_pool += f'{att.name}:{att.pp} '

                        evolving_pk_item = evolving_pk.objet_tenu
                        if evolving_pk_item is None:
                            evolving_pk_item = 'None'
                        else:
                            evolving_pk_item = f'{evolving_pk_item.name}'
                        line[5] = f'{evolving_pk.name} {evolving_pk.is_shiny} {evolving_pk.get_id()} {evolving_pk.get_level()} {evolving_pk_bonus} {evolving_pk.is_alive} {pk_att_pool} {evolving_pk_item}'

                    else:
                        line[5] = 'None'

                listecsv.append(line)
                i += 1
            file.close()

        self.write_down_backup('game.csv', listecsv)

        # save sac
        with open("save/sac.csv") as file:
            rows = csv.reader(file, delimiter=',')
            i = 0
            listecsv = []
            sac = self.player.sac
            for line in rows:
                if not i == 0:
                    if sac[i-1] != None:
                        line[0] = sac[i-1].name
                        line[1] = sac[i-1].quantite
                    else:
                        line = ["None", 0]
                listecsv.append(line)
                i += 1
        self.write_down_backup('sac.csv', listecsv)

    def write_down_backup(self, file_name: str, listecsv: list):
        """
        Methode qui écrit la sauvegarde dans le fichier en mémoire
        """
        with open(f'save/{file_name}', 'w', newline='') as file:
            rows = csv.writer(file)
            rows.writerows(listecsv)
            file.close()

    def reset_save_file(self):
        with open('save/team.csv', newline='') as file:
            rows = csv.reader(file, delimiter=',')
            i = 0
            listecsv = []
            for line in rows:
                if i != 0:
                    line[0] = ""
                    line[1] = ""
                    line[2] = ""
                    line[3] = ""
                    line[4] = ""
                    line[5] = ""
                    line[6] = ""
                    line[7] = ""

                listecsv.append(line)
                i += 1
            print(listecsv)
            file.close()
        with open('save/team.csv', 'w', newline='') as file:
            rows = csv.writer(file)
            rows.writerows(listecsv)
            file.close()

    def load(self):
        """
        Methode qui charge la sauvegarde
        """
        # Team
        with open('save/team.csv') as team_file:
            pk_lines = csv.reader(team_file, delimiter=',')
            i = 0
            for pk_infos in pk_lines:
                if i != 0:
                    if pk_infos[0] == '':
                        self.player.team[i-1] = None
                    else:
                        item = pk_infos[3]
                        if item == 'None':
                            item = None
                        else:
                            item = objet.Objet(item)

                        self.player.team[i-1] = pokemon.Pokemon(pk_infos[0], pk_infos[4], self, pk_infos[1] == 'True', item)
                        self.player.team[i-1].id = int(pk_infos[2])
                        bonus_stats = pk_infos[5].split(" ")
                        self.player.team[i-1].health = int(bonus_stats[0])
                        self.player.team[i-1].bonus_pvmax = int(bonus_stats[1])
                        self.player.team[i-1].bonus_attack = int(bonus_stats[2])
                        self.player.team[i-1].bonus_defense = int(bonus_stats[3])
                        self.player.team[i-1].bonus_speed = int(bonus_stats[4])
                        self.player.team[i-1].multiplicateur_pvmax = int(bonus_stats[5])
                        self.player.team[i-1].multiplicateur_attack = int(bonus_stats[6])
                        self.player.team[i-1].multiplicateur_defense = int(bonus_stats[7])
                        self.player.team[i-1].multiplicateur_speed = int(bonus_stats[8])
                        self.player.team[i-1].is_alive = pk_infos[6] == 'True'
                        attaque_pool = [None, None, None, None]
                        n = 0
                        print(pk_infos[7])
                        for att in pk_infos[7].split(" ")[:-1]:
                            print(pk_infos[7].split(" "))
                            att_name, att_pp = att.split(':')[0], att.split(':')[1]
                            attaque = attaques.Attaque(att_name)
                            attaque.set_pp(int(att_pp))

                            attaque_pool[n] = attaque
                            n += 1
                        self.player.team[i-1].attaque_pool = attaque_pool

                i += 1
            team_file.close()

        # Player
        with open('save/player.csv') as player_file:
            player_infos = list(csv.reader(player_file, delimiter=','))[1]

            self.player.name = player_infos[0]
            self.player.level = int(player_infos[1])
            self.player.actions = int(player_infos[2])
            self.player.max_actions = int(player_infos[3])
            self.player.always_shiny_on = player_infos[4] == 'True'
            self.player.money = int(player_infos[5])

            player_file.close()

        # Game
        with open('save/game.csv') as game_file:
            game_infos = list(csv.reader(game_file, delimiter=','))[1]

            self.next_pk_id = int(game_infos[0])
            self.general_seed = int(game_infos[1])

            dresseur_infos = game_infos[2].split(' ')
            next_fighting_dresseur = dresseur.get_dresseur_by_name(dresseur_infos[0])
            item = dresseur_infos[3]
            if item == 'None':
                item = None
            else:
                item = objet.Objet(item)

            dresseur_pk = pokemon.Pokemon(dresseur_infos[1], int(dresseur_infos[2]), self, objet_tenu=item)
            self.next_fighting_dresseur = next_fighting_dresseur(self, pk=dresseur_pk)

            panels_pks = (
                (self.classic_panel.ingame_window.train_panel.training_pk, 3),
                (self.classic_panel.ingame_window.spawn_panel.spawning_pk, 4),
                (self.classic_panel.ingame_window.evol_panel.evolving_pk, 5),
            )

            for pk, i in panels_pks:
                pk_infos = game_infos[i].split(' ')
                if pk_infos[0] != 'None':
                    item = pk_infos[-1]
                    if item == 'None':
                        item = None
                    else:
                        item = objet.Objet(item)

                    pk = pokemon.Pokemon(pk_infos[0], int(pk_infos[3]), self, is_shiny=pk_infos[1]=='True', objet_tenu=item)
                    pk.id = int(pk_infos[2])
                    training_pk_bonus_stats = pk_infos[4].split(' ')
                    pk.health = int(training_pk_bonus_stats[0])
                    pk.bonus_pvmax = int(training_pk_bonus_stats[1])
                    pk.bonus_attack = int(training_pk_bonus_stats[2])
                    pk.bonus_defense = int(training_pk_bonus_stats[3])
                    pk.bonus_speed = int(training_pk_bonus_stats[4])
                    pk.multiplicateur_pvmax = int(training_pk_bonus_stats[5])
                    pk.multiplicateur_attack = int(training_pk_bonus_stats[6])
                    pk.multiplicateur_defense = int(training_pk_bonus_stats[7])
                    pk.multiplicateur_speed = int(training_pk_bonus_stats[8])
                    pk.is_alive = pk_infos[5] == 'True'

                    attaque_pool = [None, None, None, None]
                    i = 0
                    for att in pk_infos[6]:
                        att_name, att_pp = att.split(':')
                        attaque = attaques.Attaque(att_name)
                        attaque.set_pp(int(att_pp))

                        attaque_pool[i] = attaque
                        i += 1
                    pk.attaque_pool = attaque_pool

            game_file.close()

        # sac
        with open('save/sac.csv') as sac_file:
            sac_infos = csv.reader(sac_file, delimiter=',')
            i = 0
            for item in sac_infos:
                if i != 0:
                    if item[0] != 'None':
                        self.player.sac[i-1] = objet.Objet(item[0], item[1])
                    else:
                        self.player.sac[i-1] = None
                    i += 1
            sac_file.close()


if __name__ == '__main__':
    game = Game()
    game.init_pokemons_list()
