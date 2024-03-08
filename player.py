import objet
import player_name
import pokemon
from objet import Objet


class Player:

    def __init__(self, game):
        self.game = game

        self.level = 0
        self.name = "Nom"
        self.name_edited = False
        self.name_editing_mode = False

        self.actions = 3
        self.max_actions = 3

        self.always_shiny_on = False

        self.team = [None,
                     None,
                     None,
                     None,
                     None,
                     None]
        self.sac_page1 = [objet.Objet('Super_Bonbon', 100),
                          objet.Objet('Potion_Max', 100),
                          objet.Objet('Baie_Oran', 100),
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None]
        self.sac_page2 = [None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None]

        self.money = 1000

    def edit_name(self, mode='add', letter=''):
        if mode == 'add':
            if player_name.get_pixels(self.name) < player_name.MAX_PLAYER_NAME_LENGTH:
                self.name += letter
        elif mode == 'suppr':
            self.name = self.name[:-1]
        elif mode == 'change':
            self.name = letter
        elif mode == 'delete':
            self.name = ''

    def enable_name_editing_mode(self):
        self.name_editing_mode = True
        self.name = ''
        self.name_edited = True

    def reset_name(self):
        self.name = "Nom"
        self.name_edited = False
        self.name_editing_mode = False

    def reset_actions(self):
        self.actions = self.max_actions

    def evol_pk(self, i=0):
        if self.team[i] is not None:
            self.team[i] = self.team[i].evolution()

    def use_action(self, amount=1):
        self.actions -= amount

        if amount > 1:
            text = f'{amount} actions utilisées'
        else:
            text = f'{amount} action utilisée'

        self.game.notif(text=text, color=(225, 0, 0))

    def level_up(self, nb_lv=1):
        self.level += nb_lv

    def rise_max_actions_value(self):
        self.max_actions += 1
        self.actions += 1

    def get_nb_team_members(self):
        nb_team_members = 0
        for member in self.team:
            if member is not None:
                nb_team_members += 1

        return nb_team_members

    def is_team_empty(self):
        if self.get_nb_team_members() == 0:
            return True
        return False

    def is_sac_page_full(self, page_num):
        sac_page = self.sac_page1
        if page_num == 1:
            sac_page = self.sac_page1
        elif page_num == 2:
            sac_page = self.sac_page2

        for objet in sac_page:
            if objet is None:
                return False

        return True

    def get_sac_empty_emp(self, page_num):
        sac_page = self.sac_page1
        if page_num == 1:
            sac_page = self.sac_page1
        elif page_num == 2:
            sac_page = self.sac_page2

        empty_emp_i = 0
        for emp in sac_page:
            if emp is None:
                return empty_emp_i

            empty_emp_i += 1

    def get_moyenne_team(self):
        levels_list = []
        for pk in self.team:
            if pk is not None:
                levels_list.append(pk.get_level())

        if not levels_list:
            return 0
        else:
            return sum(levels_list) // len(levels_list)

    def get_level(self):
        return self.level


if __name__ == "__main__":
    player = Player()
