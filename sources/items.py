"""
Fichier gérant le panel de l'action Items
"""

# Importation des modules
import pygame
import random

import objet


class ItemsPanel:
    """
    Classe représentant le panel d'action "Items".

    Dans ce panel, le joueur pourra :
    - Acheter des items.
    - Vendre des items.
    """

    def __init__(self, game):
        self.game = game
        self.PATH = 'assets/game/ingame_windows/Items/'

        # Variables de panel
        self.bool_entrer = False
        self.bool_sell = False
        self.bool_buy = False

        # Chargement des fonts
        self.entrer_price_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 50)
        self.item_price_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 30)
        self.item_quantite_font = pygame.font.Font('assets/fonts/impact.ttf', 30)
        self.player_money_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 40)
        self.categorie_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 25)
        self.research_text_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 30)
        self.item_name_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 50)
        self.item_desc_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 25)

        # Chargement des images
        self.background = self.img_load('background')
        self.background2 = self.img_load('background2')

        self.buy_mode_button = self.img_load('acheter_button')
        self.buy_mode_button_rect = pygame.Rect(71, 118, 250, 300)
        self.sell_mode_button = self.img_load('vendre_button')
        self.sell_mode_button_rect = pygame.Rect(531, 118, 250, 300)

        self.buy_panel = self.img_load('buy_panel')
        self.buy_panel_rect = pygame.Rect(1, 0, 873, 490)

        self.buy_panel_x_button = self.img_load('buy_panel_x_button')
        self.buy_panel_x_button_rect = pygame.Rect(818, 11, 44, 44)

        self.buy_emp_hover = self.img_load('buy_emp_hover3')
        self.buyable_emp_hover = self.img_load('buy_emp_hover')
        self.unbuyable_emp_hover = self.img_load('buy_emp_hover2')

        self.sell_panel = self.img_load('sell_panel')
        self.sell_panel_rect = pygame.Rect(1, 0, 873, 490)

        self.sell_emp_hover = self.img_load('sell_emp_hover')

        self.sell_panel_x_button = self.img_load('sell_panel_x_button')
        self.sell_panel_x_button_rect = pygame.Rect(818, 11, 44, 44)

        self.categorie_hover = self.img_load('categorie_hover')
        self.sell_categorie_hover = self.img_load('sell_categorie_hover')

        self.curseur = self.img_load('curseur')
        self.curseur_rect = pygame.Rect(842, 96, 17, 45)
        # RECTS
        self.emp_rects = [
            pygame.Rect(193, 91, 105, 105),
            pygame.Rect(320, 91, 105, 105),
            pygame.Rect(446, 91, 105, 105),
            pygame.Rect(573, 91, 105, 105),
            pygame.Rect(699, 91, 105, 105),
            pygame.Rect(193, 217, 105, 105),
            pygame.Rect(320, 217, 105, 105),
            pygame.Rect(446, 217, 105, 105),
            pygame.Rect(573, 217, 105, 105),
            pygame.Rect(699, 217, 105, 105)
        ]
        self.categories_rects = [
            pygame.Rect(0, 128, 173, 30),
            pygame.Rect(0, 161, 173, 30),
            pygame.Rect(0, 194, 173, 30),
            pygame.Rect(0, 227, 173, 30),
            pygame.Rect(0, 260, 173, 30),
            pygame.Rect(0, 293, 173, 30),
        ]
        self.categories_names = [
            "Médecine",
            "Baies",
            "Objets",
            "Marchandises",
            "Objets rares",
            "Balls"
        ]
        self.categories_names_ = [
            "Medecine",
            "Baies",
            "Objets",
            "Marchandises",
            "Objets_rares",
            "Balls"
        ]

        self.search_bar_rect = pygame.Rect(9, 11, 771, 47)
        self.items_space_rect = pygame.Rect(160, 76, 691, 294)
        self.curseur_bar_rect = pygame.Rect(842, 96, 17, 220)

        # Variables
        self.entrer_price = 100

        self.research_text = ""
        self.categorie_selected = None
        self.item_selected = None

        self.current_buy_item_list = self.research_item('Buy')
        self.current_sell_item_list = self.research_item('Sell')

        self.page = 0
        if len(self.current_buy_item_list) % 10 == 0:
            self.max_page = len(self.current_buy_item_list) // 10
            if self.max_page < 1:
                self.max_page = 1

        else:
            self.max_page = len(self.current_buy_item_list) // 10 + 1

        #
        self.curseur_move_mode = False
        self.research_mode = False

        self.research_curseur_compteur = 0

        # Position sauvegardée de la fenêtre ingame
        self.window_pos = (0, 0)

    # Méthodes liées à l'affichage

    def update(self, surface: pygame.Surface, possouris: list, window: list):
        """
        Méthode d'actualisation de l'affichage du panel.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        @in : window_pos, list → coordonnées de la fenêtre ingame
        """

        window_pos = window.basic_window_pos
        self.window_pos = window_pos

        if not self.bool_entrer:
            self.display_entrer_panel(surface)
        elif not self.bool_buy and not self.bool_sell:
            self.display_choisir_panel(surface, possouris)
        elif self.bool_sell:
            self.display_sell_panel(surface, possouris)
        elif self.bool_buy:
            self.display_buy_panel(surface, possouris)

    def display_entrer_panel(self, surface: pygame.Surface):
        """
        Methode qui actualise l'affichage du panel pour entrer dans le magasin.

        @in : surface, pygame.Surface → fenêtre du jeu
        """

        # Background
        self.display(self.background, (0, 0), surface)
        # Affichage du prix
        text = self.entrer_price_font.render(str(self.entrer_price), False, (0, 0, 0))
        co = (354 - text.get_width() // 2, 8)
        self.display(text,
                     co,
                     surface)

    def display_choisir_panel(self, surface: pygame.Surface, possouris: list):
        """
        Methode qui actualise l'affichage du panel de choix de type de transaction (Payer ou Acheter).

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        self.display(self.background2, (0, 0), surface)

        if self.rect(self.buy_mode_button_rect).collidepoint(possouris):
            self.display(self.buy_mode_button, self.buy_mode_button_rect, surface, (250, 0, 250, 300))
        else:
            self.display(self.buy_mode_button, self.buy_mode_button_rect, surface, (0, 0, 250, 300))

        if self.rect(self.sell_mode_button_rect).collidepoint(possouris):
            self.display(self.sell_mode_button, self.sell_mode_button_rect, surface, (250, 0, 250, 300))
        else:
            self.display(self.sell_mode_button, self.sell_mode_button_rect, surface, (0, 0, 250, 300))

    def display_buy_panel(self, surface: pygame.Surface, possouris: list):
        """
        Methode qui gère l'actualisation de l'affichage du panel d'achat d'objets.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """

        # Fenetre d'achat
        self.display(self.buy_panel, self.buy_panel_rect, surface)

        # Texte recherché
        self.display_research_text(surface)

        # X Button
        if self.rect(self.buy_panel_x_button_rect).collidepoint(possouris):
            self.display(self.buy_panel_x_button, self.buy_panel_x_button_rect, surface, (44, 0, 44, 44))
        else:
            self.display(self.buy_panel_x_button, self.buy_panel_x_button_rect, surface, (0, 0, 44, 44))

        # Curseur
        self.display_curseur(surface, possouris)

        # Page
        page_ind_text = self.item_price_font.render(f'{self.page + 1}/{self.max_page}', False, (0, 0, 0))
        self.display(page_ind_text,
                     (769 + 35 - page_ind_text.get_width() // 2, 338),
                     surface)

        # Items emps
        self.display_buy_items_emps(surface, possouris)

        # Item selectionné
        self.update_selected_item(possouris)

        # Catégories
        self.display_categories(surface, possouris)

        # Items descriptions
        self.display_item_desc(surface)

        # Solde
        solde_text = self.player_money_font.render(str(self.game.player.money), False, (0, 0, 0))
        self.display(solde_text,
                     (86 - solde_text.get_width() // 2, 463 - solde_text.get_height() // 2),
                     surface)

    def display_sell_panel(self, surface: pygame.Surface, possouris: list):
        """
        Methode qui gère l'actualisation de l'affichage du panel de vente d'objets.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        # Fenetre d'achat
        self.display(self.sell_panel, self.sell_panel_rect, surface)

        # Texte recherché
        self.display_research_text(surface)

        # X Button
        if self.rect(self.sell_panel_x_button_rect).collidepoint(possouris):
            self.display(self.sell_panel_x_button, self.sell_panel_x_button_rect, surface, (44, 0, 44, 44))
        else:
            self.display(self.sell_panel_x_button, self.sell_panel_x_button_rect, surface, (0, 0, 44, 44))

        # Curseur
        self.display_curseur(surface, possouris)

        # Page
        page_ind_text = self.item_price_font.render(f'{self.page + 1}/{self.max_page}', False, (0, 0, 0))
        self.display(page_ind_text,
                     (769 + 35 - page_ind_text.get_width() // 2, 338),
                     surface)

        # Items emps
        self.display_sell_items_emps(surface, possouris)

        # Item selectionné
        self.update_selected_item(possouris)

        # Catégories
        self.display_categories(surface, possouris)

        # Items descriptions
        self.display_item_desc(surface)

        # Solde
        solde_text = self.player_money_font.render(str(self.game.player.money), False, (0, 0, 0))
        self.display(solde_text,
                     (86 - solde_text.get_width() // 2, 463 - solde_text.get_height() // 2),
                     surface)

    def display_categories(self, surface: pygame.Surface, possouris: list):
        """
        Méthode d'actualisation de l'affichage des catégories.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """

        if self.bool_buy:
            color = (59, 33, 0)  # Buy color
        elif self.bool_sell:
            color = (0, 34, 3)  # Sell color

        for i in range(6):
            if self.rect(self.categories_rects[i]).collidepoint(possouris) or self.categorie_selected == \
                    self.categories_names_[i]:
                if self.bool_sell:
                    self.display(self.sell_categorie_hover,
                                 self.categories_rects[i],
                                 surface)
                elif self.bool_buy:
                    self.display(self.categorie_hover,
                                 self.categories_rects[i],
                                 surface)

            self.display(self.categorie_font.render(self.categories_names[i], False, color),
                         (self.categories_rects[i].x + 10,
                          self.categories_rects[i].y),
                         surface)

    def display_buy_items_emps(self, surface: pygame.Surface, possouris: list):
        """
        Méthode d'actualisation de l'affichage des emplacements d'objets du panel d'achat.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """

        i = 0
        for item_rect in self.emp_rects:

            if i + self.page * 10 >= len(self.current_buy_item_list):
                item = None
            else:
                item = self.current_buy_item_list[i + self.page * 10]

            if item is not None:
                self.display(pygame.transform.scale(item.icon_image, (80, 80)),
                             (item_rect.x + 13,
                              item_rect.y + 12), surface)

                if self.rect(item_rect).collidepoint(possouris):
                    if item.boolBuy:
                        if self.game.player.money >= item.buy_price:
                            self.display(self.buy_emp_hover, (item_rect.x + 2,
                                                              item_rect.y + 4,
                                                              item_rect.w,
                                                              item_rect.h),
                                         surface)
                        else:
                            self.display(self.buyable_emp_hover, (item_rect.x + 2,
                                                                  item_rect.y + 4,
                                                                  item_rect.w,
                                                                  item_rect.h),
                                         surface)
                    else:
                        self.display(self.unbuyable_emp_hover, (item_rect.x + 2,
                                                                item_rect.y + 4,
                                                                item_rect.w,
                                                                item_rect.h),
                                     surface)

                if item.boolBuy:
                    item_price_text = self.item_price_font.render(str(item.buy_price), False, (0, 0, 0))
                    self.display(item_price_text, (item_rect.x + 53 - item_price_text.get_width() // 2,
                                                   item_rect.y + 89),
                                 surface)

            i += 1

    def display_sell_items_emps(self, surface: pygame.Surface, possouris: list):
        """
        Méthode d'actualisation de l'affichage des emplacements d'objets du panel de vente.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """
        i = 0
        for item_rect in self.emp_rects:

            if i + self.page * 10 >= len(self.current_sell_item_list):
                item = None
            else:
                item = self.current_sell_item_list[i + self.page * 10]

            if item is not None:
                self.display(pygame.transform.scale(item.icon_image, (80, 80)),
                             (item_rect.x + 13,
                              item_rect.y + 12), surface)

                if self.rect(item_rect).collidepoint(possouris):
                    if item.boolSell:
                        self.display(self.sell_emp_hover, (item_rect.x + 5,
                                                           item_rect.y + 4,
                                                           item_rect.w,
                                                           item_rect.h),
                                     surface)
                    else:
                        self.display(self.unbuyable_emp_hover, (item_rect.x + 2,
                                                                item_rect.y + 4,
                                                                item_rect.w,
                                                                item_rect.h),
                                     surface)

                if item.boolSell:
                    item_price_text = self.item_price_font.render(str(item.sell_price), False, (0, 0, 0))
                    self.display(item_price_text, (item_rect.x + 53 - item_price_text.get_width() // 2,
                                                   item_rect.y + 89),
                                 surface)

                # Affichage de la quantite
                item_quantite_text = self.item_quantite_font.render(str(item.quantite), False, (255, 255, 255))
                self.display(item_quantite_text, (item_rect.x + 90 - item_quantite_text.get_width() // 2,
                                                  item_rect.y + 70),
                             surface)
            i += 1

    def display_item_desc(self, surface: pygame.Surface):
        """
        Methode qui actualise l'affichage de la description de l'item sélectionné.

        @in : surface, pygame.Surface → fenêtre du jeu
        """
        item = self.item_selected
        if item is not None:
            self.display(self.item_name_font.render(item.name_, False, (0, 0, 0)),
                         (183, 350),
                         surface)

            y = 400
            for line in item.description:
                self.display(self.item_desc_font.render(line, False, (0, 0, 0)),
                             (183, y),
                             surface)
                y += 28

    def display_curseur(self, surface: pygame.Surface, possouris: list):
        """
        Methode d'actualisation de l'affichage du curseur.

        @in : surface, pygame.Surface → fenêtre du jeu
        @in : possouris, list → coordonnées du pointeur de souris
        """

        if self.rect(self.curseur_rect).collidepoint(possouris) or self.curseur_move_mode:
            self.display(self.curseur, self.curseur_rect, surface, (17, 0, 17, 45))
        else:
            self.display(self.curseur, self.curseur_rect, surface, (0, 0, 17, 45))

        if not self.curseur_move_mode:
            if self.game.mouse_pressed[1] and self.rect(self.curseur_rect).collidepoint(possouris):
                self.curseur_move_mode = True
        else:
            if not self.game.mouse_pressed[1]:
                self.curseur_move_mode = False

            for n in range(self.max_page):
                if possouris[1] > self.rect(self.curseur_bar_rect).y + self.curseur_bar_rect.h // self.max_page * n:
                    self.page = n

                    self.update_curseur_rect()

    def display_research_text(self, surface: pygame.Surface):
        """
        Methode d'actualisation de l'affichage du texte recherché dans la barre de recherche.

        @in : surface, pygame.Surface → fenêtre du jeu
        """
        research_text = self.research_text_font.render(self.research_text, False, (0, 0, 0))
        self.display(research_text,
                     (62, 13),
                     surface)
        if self.research_mode:
            if self.research_curseur_compteur > 20:
                pygame.draw.rect(surface, (0, 0, 0), self.rect(
                    pygame.Rect(67 + research_text.get_width(), 21, 2, research_text.get_height() - 16)))

            self.research_curseur_compteur += 1
            if self.research_curseur_compteur > 41:
                self.research_curseur_compteur = 0

    def rect(self, rect: pygame.Rect):
        """
        Méthode qui retourne le rect réel par rapport à la fenêtre du jeu.

        @in : rect, pygame.Rect
        @out : pygame.Rect → rect modifié
        """
        return pygame.Rect(rect.x + self.window_pos[0] + 19,
                           rect.y + self.window_pos[1] + 39,
                           rect.w,
                           rect.h)

    def display(self,
                image: pygame.Surface,
                pos,
                surface: pygame.Surface,
                rect=None):
        """
        Méthode d'affichage d'une image.
        Prend en paramètre une position relative à la fenêtre ingame.

        @in : image, pygame.Surface → image à afficher
        @in : pos, tuple ou pygame.Rect → position souhaitée relative à la fenêtre ingame
        @in : surface, pygame.Surface → fenêtre du jeu
        @in : rect, pygame.Rect ou None → zone de l'image à afficher

        """
        if rect is None:
            surface.blit(image, (pos[0] + self.window_pos[0] + 19,
                                 pos[1] + self.window_pos[1] + 39))
        else:
            surface.blit(image, (pos[0] + self.window_pos[0] + 19,
                                 pos[1] + self.window_pos[1] + 39),
                         rect)

    # Méthode d'actualisation des variables

    def update_selected_item(self, possouris: list):
        """
        Methode d'actualisation de l'item sélectionné en fonction de la position du pointeur de souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if self.bool_sell:
            i = 0
            for item_rect in self.emp_rects:
                if i + self.page * 10 < len(self.current_sell_item_list) and self.current_sell_item_list[
                    i + self.page * 10] is not None:
                    if self.rect(item_rect).collidepoint(possouris):
                        self.item_selected = self.current_sell_item_list[i + self.page * 10]
                    elif self.item_selected == self.current_sell_item_list[i + self.page * 10]:
                        self.item_selected = None

                i += 1

        elif self.bool_buy:

            i = 0
            for item_rect in self.emp_rects:
                if i + self.page * 10 < len(self.current_buy_item_list):
                    if self.rect(item_rect).collidepoint(possouris):
                        self.item_selected = self.current_buy_item_list[i + self.page * 10]
                    elif self.item_selected == self.current_buy_item_list[i + self.page * 10]:
                        self.item_selected = None

                i += 1

    def update_curseur_rect(self):
        """
        Méthode d'actualisation du rect du curseur.
        """
        if self.page == self.max_page - 1 and self.max_page != 1:
            self.curseur_rect = pygame.Rect(842, 272, 17, 45)
        else:
            self.curseur_rect = pygame.Rect(842,
                                            self.curseur_bar_rect.y + self.curseur_bar_rect.h // self.max_page * self.page,
                                            17, 45)

    def update_research_text(self, character: str):
        """
        Méthode d'actualisation de la recherche du joueur.
        Ajoute à la recherche le character pris en entrée ou éxécute l'action liée à la touche spéciale appuyée.

        @in : character, str
        """
        if character in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLKMNOPQRSTUVWXYZ':
            self.research_text += character
        elif character == 'backspace':
            self.research_text = self.research_text[:-1]
        elif character == 'space':
            self.research_text += " "

        self.update_current_items_list()

    def update_current_items_list(self):
        """
        Méthode d'actualisation des listes d'objets dépendant des critères de recherche actuels.
        """
        self.current_buy_item_list = self.research_item('Buy')
        self.current_sell_item_list = self.research_item('Sell')
        if self.bool_sell:
            self.page = 0
            if len(self.current_sell_item_list) % 10 == 0:
                self.max_page = len(self.current_sell_item_list) // 10
                if self.max_page < 1:
                    self.max_page = 1
            else:
                self.max_page = len(self.current_sell_item_list) // 10 + 1
        elif self.bool_buy:
            self.page = 0
            if len(self.current_buy_item_list) % 10 == 0:
                self.max_page = len(self.current_buy_item_list) // 10
                if self.max_page < 1:
                    self.max_page = 1
            else:
                self.max_page = len(self.current_buy_item_list) // 10 + 1

    # Méthodes essentielles
    def buy_item(self, item: objet.Objet):
        """
        Methode qui permet d'acheter un objet.

        @in : item, objet.Objet → Objet à acheter
        """
        if item.boolBuy:
            if self.game.player.payer(item.buy_price):  # Le joueur paye s'il peut
                if item.categorie == 'Objets_rares':
                    item.boolBuy = False

                self.game.player.add_sac_item(item=item)
                self.game.notif(f"Objet ajouté au sac !", (0, 0, 0))

    def sell_item(self, item):
        """
        Methode qui permet de vendre un objet.
        @in : item, objet.Objet → Objet à vendre
        """
        if item.boolSell:
            self.game.player.money += item.sell_price
            item.quantite -= 1
            self.game.notif(f"Objet vendu !", (0, 0, 0))

    # Méthodes annexes

    def tri_croisant_prix(self, liste_objet: list, mode='Buy') -> list:
        """
        Méthode de tri d'une liste d'objet par tri croissant.
        → Algorithme de tri par insertion.

        @in : liste_objet, list
        @in : mode, str → 'Buy' ou 'Sell'
        @out : list
        """
        if mode == 'Buy':
            tri = True
            while tri:
                tri = False
                for objet_index in range(1, len(liste_objet)):
                    if not liste_objet[objet_index - 1].boolBuy:
                        if liste_objet[objet_index].boolBuy:
                            liste_objet[objet_index], liste_objet[objet_index - 1] = liste_objet[objet_index - 1], \
                                liste_objet[objet_index]
                            tri = True

                    elif liste_objet[objet_index].boolBuy:
                        if liste_objet[objet_index].buy_price < liste_objet[objet_index - 1].buy_price:
                            liste_objet[objet_index], liste_objet[objet_index - 1] = liste_objet[objet_index - 1], \
                                liste_objet[objet_index]
                            tri = True
            return liste_objet

        elif mode == 'Sell':
            tri = True
            while tri:
                tri = False
                for objet_index in range(1, len(liste_objet)):
                    if not liste_objet[objet_index - 1].boolSell:
                        if liste_objet[objet_index].boolSell:
                            liste_objet[objet_index], liste_objet[objet_index - 1] = liste_objet[objet_index - 1], \
                                liste_objet[objet_index]
                            tri = True
                    elif liste_objet[objet_index].boolSell:
                        if liste_objet[objet_index].sell_price < liste_objet[objet_index - 1].sell_price:
                            liste_objet[objet_index], liste_objet[objet_index - 1] = liste_objet[objet_index - 1], \
                                liste_objet[objet_index]
                            tri = True
            return liste_objet

    def research_item(self, mode='Buy') -> list:
        """
        Methode de recherche d'objet dans la boutique.

        @in : mode, str → 'Buy' ou 'Sell'
        @out : list → liste des objets triés
        """
        text = self.research_text
        if mode == 'Buy':
            liste = self.game.items_list['All'].copy()
            liste_r = []
            for objet in liste:
                if text in objet.name_ or text.lower() in objet.name_ or text[0].upper() + text[
                                                                                           1:].lower() in objet.name_:
                    if objet.categorie == self.categorie_selected or self.categorie_selected is None:
                        liste_r.append(objet)

            liste_r = self.tri_croisant_prix(liste_r, mode)
            return liste_r

        elif mode == 'Sell':
            liste = self.game.player.sac.copy()
            liste_r = []
            for objet in liste:
                if objet is not None:
                    if text in objet.name_ or text.lower() in objet.name_ or text[0].upper() + text[
                                                                                               1:].lower() in objet.name_:
                        if objet.categorie == self.categorie_selected or self.categorie_selected is None:
                            liste_r.append(objet)

            liste_r = self.tri_croisant_prix(liste_r, mode)
            return liste_r

    def research_categorie(self, liste_obj, categorie, mode='Buy') -> list:
        """
        Méthode de recherche en fonction de la catégorie sélectionnée.

        @in : liste_obj, list → liste d'objets à répertorier selon la catégorie et à trier
        @in : categorie, str
        @in : mode, str → 'Buy' ou 'Sell'
        @out : list
        """
        liste_obj_r = []
        for obj in liste_obj:
            if obj.categorie == categorie:
                liste_obj_r.append(obj)
        return self.tri_croisant_prix(liste_obj_r, mode)

    def reset_research(self):
        """
        Methode de reinitialisation de la recherche.
        """
        self.research_text = ""
        self.research_mode = False
        self.update_current_items_list()
        self.update_curseur_rect()

    def img_load(self, file_name):
        return pygame.image.load(f'{self.PATH}{file_name}.png')

    # Méthodes basiques

    def reset(self):
        """
        Méthode de réinitialisation du panel.
        Utilisée lors de l'initialisation d'un nouveau tour de jeu.
        """
        pass

    def close(self):
        """
        Méthode classique qui éxécute tout ce qu'il faut faire lorsque le panel est fermé.
        """
        self.bool_entrer = False
        self.bool_buy = False
        self.bool_sell = False
        self.reset_research()

    # Méthodes de gestion d'intéractions

    def left_clic_interactions(self, possouris: list):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        if not self.bool_entrer:
            if not self.game.classic_panel.ingame_window.window_bar_rect.collidepoint(possouris):
                if self.game.player.payer(self.entrer_price):
                    self.bool_entrer = True
                else:
                    self.game.notif("Argent insuffisant", (255, 0, 0))
        elif self.bool_sell:
            if self.rect(self.sell_panel_x_button_rect).collidepoint(possouris):
                self.reset_research()
                self.categorie_selected = None
                self.bool_sell = False
            elif self.rect(self.search_bar_rect).collidepoint(possouris):
                self.research_mode = True
            else:
                if self.research_mode and not self.rect(self.search_bar_rect).collidepoint(possouris):
                    self.research_mode = False

                i_categorie = 0
                for categorie_rect in self.categories_rects:
                    if self.rect(categorie_rect).collidepoint(possouris):
                        if not self.categorie_selected == self.categories_names_[i_categorie]:
                            self.categorie_selected = self.categories_names_[i_categorie]
                        else:
                            self.categorie_selected = None
                        self.update_current_items_list()
                        self.update_curseur_rect()
                    i_categorie += 1

                i_item = 0
                for item_rect in self.emp_rects:
                    if self.rect(item_rect).collidepoint(possouris):
                        if i_item + self.page * 10 < len(self.current_sell_item_list) and self.current_sell_item_list[
                            i_item + self.page * 10] is not None:
                            item = self.current_sell_item_list[i_item + self.page * 10]
                            if item.boolSell:
                                player_item_i = self.game.player.find_sac_item(item)
                                player_item = self.game.player.sac[player_item_i]
                                self.sell_item(player_item)
                                if player_item.quantite <= 0:
                                    self.game.player.sac[player_item_i] = None
                                self.update_current_items_list()
                                self.update_curseur_rect()
                    i_item += 1
        elif self.bool_buy:
            if self.rect(self.buy_panel_x_button_rect).collidepoint(possouris):
                self.reset_research()
                self.categorie_selected = None
                self.bool_buy = False
            elif self.rect(self.search_bar_rect).collidepoint(possouris):
                self.research_mode = True
            else:
                if self.research_mode and not self.rect(self.search_bar_rect).collidepoint(possouris):
                    self.research_mode = False

                i_categorie = 0
                for categorie_rect in self.categories_rects:
                    if self.rect(categorie_rect).collidepoint(possouris):
                        if not self.categorie_selected == self.categories_names_[i_categorie]:
                            self.categorie_selected = self.categories_names_[i_categorie]
                        else:
                            self.categorie_selected = None
                        self.update_current_items_list()
                        self.update_curseur_rect()
                    i_categorie += 1

                i_item = 0
                for item_rect in self.emp_rects:
                    if self.rect(item_rect).collidepoint(possouris):
                        if i_item + self.page * 10 < len(self.current_buy_item_list):
                            item = self.current_buy_item_list[i_item + self.page * 10]
                            self.buy_item(item)
                    i_item += 1
        else:
            if self.rect(self.sell_mode_button_rect).collidepoint(possouris):
                self.bool_sell = True
                self.update_current_items_list()
            elif self.rect(self.buy_mode_button_rect).collidepoint(possouris):
                self.bool_buy = True
                self.update_current_items_list()

    def right_clic_interactions(self, posssouris: list):
        """
        Méthode gérant les intéractions de l'utilisateur avec le clic droit de la souris.

        @in : possouris, list → coordonnées du pointeur de souris
        """
        pass

    def keydown(self, event_key: int):
        """
        Methode qui gère les interactions de l'utilisateur avec les touches du clavier.

        @in : event_key, int → valeur associée à la touche appuyée
        """
        if self.research_mode:
            if event_key == pygame.K_RETURN:
                self.research_mode = False
            else:
                if self.game.pressed[pygame.K_LSHIFT]:
                    self.update_research_text(pygame.key.name(event_key).upper())
                else:
                    self.update_research_text(pygame.key.name(event_key))

    def mouse_wheel(self, possouris: list, value: int):
        """
        Methode qui gère les interactions utilisateurs avec la molette haut/bas de la souris
        @in : possouris, list → coordonnées du pointeur de souris
        @in : value, int → puissance de l'action molette. Ex : 1 = haut de 1
                                                              -2 = bas de 2
        """
        if self.rect(self.items_space_rect).collidepoint(possouris):
            if self.page - value > self.max_page - 1:
                self.page = self.max_page - 1
            elif self.page - value < 0:
                self.page = 0
            else:
                self.page -= value

            self.update_curseur_rect()

    def is_hovering_buttons(self, possouris) -> bool:
        """
        Méthode qui retourne True si la souris est positionnée sur un bouton du panel.

        @in : possouris, list → coordonnées du pointeur de souris
        @out : bool
        """
        if not self.bool_entrer:
            if not self.game.classic_panel.ingame_window.window_bar_rect.collidepoint(possouris):
                return True
        elif self.bool_sell:
            if self.curseur_move_mode:
                return True
            elif self.rect(self.sell_panel_x_button_rect).collidepoint(possouris):
                return True
            elif self.rect(self.curseur_rect).collidepoint(possouris):
                return True
            else:
                for categorie_rect in self.categories_rects:
                    if self.rect(categorie_rect).collidepoint(possouris):
                        return True

                for item_rect in self.emp_rects:
                    if self.rect(item_rect).collidepoint(possouris):
                        return True
        elif self.bool_buy:
            if self.curseur_move_mode:
                return True
            elif self.rect(self.buy_panel_x_button_rect).collidepoint(possouris):
                return True
            elif self.rect(self.curseur_rect).collidepoint(possouris):
                return True
            else:
                for categorie_rect in self.categories_rects:
                    if self.rect(categorie_rect).collidepoint(possouris):
                        return True

                for item_rect in self.emp_rects:
                    if self.rect(item_rect).collidepoint(possouris):
                        return True
        else:
            if self.rect(self.sell_mode_button_rect).collidepoint(possouris):
                return True
            elif self.rect(self.buy_mode_button_rect).collidepoint(possouris):
                return True
