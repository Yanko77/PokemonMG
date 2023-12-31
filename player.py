import player_name
import pokemon
from objet import Objet


class Player:

    def __init__(self):
        self.level = 0
        self.name = "Nom"
        self.name_edited = False
        self.name_editing_mode = False

        self.actions = 3
        self.max_actions = 3

        self.team = [pokemon.Pokemon('Giratina', 100),
                     pokemon.Pokemon('Brasegali', 100),
                     None,
                     None,
                     None,
                     None]
        self.sac_page1 = [Objet('Velo', 3),
                          Objet('Pokeflute', 3),
                          Objet('Guerison', 2),
                          Objet('Baie_Oran', 2),
                          Objet('Baie_Sitrus', 2),
                          Objet('Mouchoir_Soie', 2),
                          Objet('Bec_Pointu', 2),
                          Objet('Pic_Venin', 2),
                          Objet('Glace_Eternelle', 2),
                          Objet('Croc_Dragon', 2),
                          Objet('Graine_Miracle', 2),
                          Objet('Charbon', 2)]
        self.sac_page2 = [Objet('Rune_Sort', 3),
                          Objet('Lunettes_Noires', 3),
                          Objet('Cuillere_Tordue', 2),
                          Objet('Aimant', 2),
                          Objet('Vive_Griffe', 2),
                          Objet('Bandeau_Muscle', 2),
                          Objet('Poussiere_Etoile', 2),
                          Objet('Poussiere_Bleute', 2),
                          Objet('Poussiere_Jaunete', 2),
                          Objet('Poudre_Verdatre', 2),
                          Objet('Charme_Chroma', 2),
                          Objet('Caillou', 2)]

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
    player.team[0], player.team[1] = pokemon.Pokemon('Dracaufeu', 10), pokemon.Pokemon('Dracaufeu', 15)
    print(player.get_moyenne_team())
