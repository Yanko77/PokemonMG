import player_name
from objet import Objet


class Player:

    def __init__(self):
        self.level = 0
        self.name = "Nom"
        self.name_edited = False
        self.name_editing_mode = False

        self.actions = 3
        self.max_actions = 3

        self.team = [None,
                     None,
                     None,
                     None,
                     None,
                     None]
        self.sac_page1 = [Objet('Poke_Ball', 3),
                          Objet('Super_Bonbon', 3),
                          Objet('PV_Plus', 2),
                          Objet('Collier_Agathe', 2),
                          Objet('Potion', 2),
                          Objet('Hyper_Potion', 2),
                          Objet('Potion_Max', 2),
                          Objet('PV_Plus', 2),
                          Objet('Proteine', 2),
                          Objet('Fer', 2),
                          Objet('Carbone', 2),
                          Objet('Eau_Fraiche', 2)]
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

    def evol_pk(self, i=0):
        if self.team[i] is not None:
            self.team[i] = self.team[i].evolution()

    def use_action(self, amount=1):
        self.actions -= amount

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

if __name__ == "__main__":
    player = Player()
    player.evol_pk()
