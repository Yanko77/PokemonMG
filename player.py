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

        self.sac = [objet.Objet('Rappel', 1),
                    objet.Objet('Bandeau_Muscle', 1),
                    objet.Objet('Aimant', 1),
                    objet.Objet('Cuillere_Tordue', 1),
                    objet.Objet('Croc_Dragon', 1),
                    objet.Objet('Baie_Oran', 1),
                    objet.Objet('Baie_Sitrus', 1),
                    objet.Objet('Potion', 1),
                    objet.Objet('Super_Bonbon', 1),
                    objet.Objet('Graine_Miracle', 1),
                    objet.Objet('Charbon', 1),
                    objet.Objet('Rune_Sort', 1),
                    objet.Objet('Lunettes_Noires', 1),
                    objet.Objet('Bec_Pointu', 1),
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

    def swap_sac_items(self, i1, i2):
        """
        Fonction qui echange la place de 2 items dans le sac
        """
        if not i1 == i2:
            self.sac[i1 - 1], self.sac[i2 - 1] = self.sac[i2 - 1], self.sac[i1 - 1]

    def find_sac_item(self, item):
        """
        Methode qui renvoie l'index de l'item recherché dans le sac.
        Renvoie None s'il n'est pas présent
        """

        for i in range(len(self.sac)):
            sac_item = self.sac[i]

            if sac_item is not None:
                if sac_item.name == item.name:
                    return i

    def add_sac_item(self, item):
        """
        Fonction qui ajoute au sac un objet et qui le stack si possible
        """

        item_place = self.find_sac_item(item)

        if item_place is None:  # Si l'item n'est pas déjà présent dans le sac
            i = 0
            while self.sac[i] is not None:
                i += 1
            self.sac[i] = item

        else:
            self.sac[item_place].quantite += item.quantite

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
