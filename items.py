import pygame
import random


class ItemsPanel:

    def __init__(self, game):
        self.game = game
        self.PATH = 'assets/game/ingame_windows/Items/'

        self.bool_entrer = False
        self.bool_sell = False
        self.bool_buy = False

        # FONTS
        self.entrer_price_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 50)
        self.item_price_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 30)
        self.player_money_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 40)
        self.categorie_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 25)
        self.research_text_font = pygame.font.Font('assets/fonts/Oswald-Regular.ttf', 30)
        self.item_name_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 50)
        self.item_desc_font = pygame.font.Font('assets/fonts/Cheesecake.ttf', 25)
        # IMAGES
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

        self.categorie_hover = self.img_load('categorie_hover')

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
        # VARIABLES
        self.entrer_price = 100

        self.research_text = ""
        self.categorie_selected = None
        self.item_selected = None

        self.current_buy_item_list = self.research_item('Buy')
        self.current_sell_item_list = self.research_item('Sell')

        self.page = 0
        if len(self.current_buy_item_list) % 10 == 0:
            self.max_page = len(self.current_buy_item_list) // 10
        else:
            self.max_page = len(self.current_buy_item_list) // 10 + 1

        #
        self.curseur_move_mode = False
        self.research_mode = False

        self.research_curseur_compteur = 0

        self.window_pos = (0, 0)

    def update(self, surface, possouris, window_pos):
        self.window_pos = window_pos

        if not self.bool_entrer:
            self.display_entrer_panel(surface, possouris)
        elif not self.bool_buy and not self.bool_sell:
            self.display_choisir_panel(surface, possouris)
        elif self.bool_sell:
            self.display_sell_panel(surface, possouris)
        elif self.bool_buy:
            self.display_buy_panel(surface, possouris)

    def display_entrer_panel(self, surface, possouris):
        """
        Methode qui actualise l'affichage du panel pour entrer dans le magasin
        """

        # Background
        self.display(self.background, (0, 0), surface)
        # Affichage du prix
        text = self.entrer_price_font.render(str(self.entrer_price), False, (0, 0, 0))
        co = (354 - text.get_width() // 2, 8)
        self.display(text,
                     co,
                     surface)

    def display_choisir_panel(self, surface, possouris):
        """
        Methode qui actualise l'affichage du panel de choix de type de transaction (Payer ou Acheter)
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

    def display_buy_panel(self, surface, possouris):
        """
        Methode qui gère l'actualisation de l'affichage du panel d'achat d'objet
        """

        # Fenetre d'achat
        self.display(self.buy_panel, self.buy_panel_rect, surface)

        # Texte recherché
        self.display_research_text(surface, possouris)

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

    def display_sell_panel(self, surface, possouris):
        """
        Methode qui gère l'actualisation de l'affichage du panel de vente d'objet
        """
        pass

    def display_categories(self, surface, possouris):

        color = (59, 33, 0)  # Buy color

        for i in range(6):
            if self.rect(self.categories_rects[i]).collidepoint(possouris) or self.categorie_selected == \
                    self.categories_names_[i]:
                self.display(self.categorie_hover,
                             self.categories_rects[i],
                             surface)

            self.display(self.categorie_font.render(self.categories_names[i], False, color),
                         (self.categories_rects[i].x + 10,
                          self.categories_rects[i].y),
                         surface)

    def display_buy_items_emps(self, surface, possouris):
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
                    if item.can_be_buy:
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

                if item.can_be_buy:
                    item_price_text = self.item_price_font.render(str(item.buy_price), False, (0, 0, 0))
                    self.display(item_price_text, (item_rect.x + 53 - item_price_text.get_width() // 2,
                                                   item_rect.y + 89),
                                 surface)

            i += 1

    def display_item_desc(self, surface):
        """
        Methode qui actualise l'affichage de la description de l'item sélectionné
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

    def display_curseur(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage du curseur
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

    def display_research_text(self, surface, possouris):
        """
        Methode d'actualisation de l'affichage du texte recherché dans la barre de recherche
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

            '''curseur = self.create_rect_alpha((2, self.player_name_text.get_height() - 16), (0, 0, 0), 200)
            self.display(curseur, 
                         (67 + research_text.get_width(), 16),
                         surface)'''

    def rect(self, rect):
        return pygame.Rect(rect.x + self.window_pos[0] + 19,
                           rect.y + self.window_pos[1] + 39,
                           rect.w,
                           rect.h)

    def display(self, image, pos, surface, rect=None):
        if rect is None:
            surface.blit(image, (pos[0] + self.window_pos[0] + 19,
                                 pos[1] + self.window_pos[1] + 39))
        else:
            surface.blit(image, (pos[0] + self.window_pos[0] + 19,
                                 pos[1] + self.window_pos[1] + 39),
                         rect)

    def update_selected_item(self, possouris):
        """
        Methode d'actualisation de l'item sélectionné
        """
        i = 0
        for item_rect in self.emp_rects:
            if i + self.page * 10 < len(self.current_buy_item_list):
                if self.rect(item_rect).collidepoint(possouris):
                    self.item_selected = self.current_buy_item_list[i + self.page * 10]
                elif self.item_selected == self.current_buy_item_list[i + self.page * 10]:
                    self.item_selected = None

            i += 1

    def update_curseur_rect(self):
        if self.page == self.max_page - 1 and self.max_page != 1:
            self.curseur_rect = pygame.Rect(842, 272, 17, 45)
        else:
            self.curseur_rect = pygame.Rect(842, self.curseur_bar_rect.y + self.curseur_bar_rect.h // self.max_page * self.page, 17, 45)

    def update_research_text(self, character: str):
        if character in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLKMNOPQRSTUVWXYZ':
            self.research_text += character
        elif character == 'backspace':
            self.research_text = self.research_text[:-1]
        elif character == 'space':
            self.research_text += " "

        self.update_current_items_list()

    def update_current_items_list(self):
        self.current_buy_item_list = self.research_item('Buy')
        self.current_sell_item_list = self.research_item('Sell')

        self.page = 0
        if len(self.current_buy_item_list) % 10 == 0:
            self.max_page = len(self.current_buy_item_list) // 10
        else:
            self.max_page = len(self.current_buy_item_list) // 10 + 1

    def buy_item(self, objet):
        """
        Methode qui permet d'acheter des objets
        @input : objet

        Exemple :
            buy_item(Poke_Ball) --> Ajoute à sac Poke_Ball
                                --> Retire prix de Poke_Ball à l'argent du joueur
        """
        if objet.can_be_buy:
            if self.game.player.payer(objet.buy_price):  # Le joueur paye s'il peut
                self.game.player.add_sac_item(item=objet)
                self.game.notif(f"Objet ajouté au sac !", (0, 0, 0))

    def sell_item(self, objet):
        """
        Methode qui permet d'acheter des objets
        @input : objet

        Exemple :
            sell_item(Poke_Ball) --> Retire à sac Poke_Ball
                                 --> Ajoute prix de Poke_Ball à l'argent du joueur
        """
        if objet.can_be_sell:
            self.game.player.money += objet.sell_price
            objet.quantite -= 1

    def tri_croisant_prix(self, liste_objet: list, mode='Buy') -> list:
        if mode == 'Buy':
            tri = True
            while tri:
                tri = False
                for objet_index in range(1, len(liste_objet)):
                    if liste_objet[objet_index].buy_price < liste_objet[objet_index - 1].buy_price:
                        liste_objet[objet_index], liste_objet[objet_index - 1] = liste_objet[objet_index - 1], \
                            liste_objet[objet_index]
                        tri = True
            return liste_objet

    def research_item(self, mode='Buy') -> list:
        """
        Methode de recherche d'objet dans la boutique
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

    def research_categorie(self, liste_obj, categorie, mode='Buy'):
        liste_obj_r = []
        for obj in liste_obj:
            if obj.categorie == categorie:
                liste_obj_r.append(obj)
        return self.tri_croisant_prix(liste_obj_r, mode)

    def reset_research(self):
        """
        Methode de reinitialisation de la recherche
        """
        self.research_text = ""
        self.research_mode = False
        self.update_current_items_list()
        self.update_curseur_rect()

    def reset(self):
        pass

    def close(self):
        self.bool_entrer = False
        self.bool_buy = False
        self.bool_sell = False
        self.reset_research()

    def left_clic_interactions(self, possouris):
        if not self.bool_entrer:
            if not self.game.classic_panel.ingame_window.window_bar_rect.collidepoint(possouris):
                if self.game.player.payer(self.entrer_price):
                    self.bool_entrer = True
        elif self.bool_sell:
            pass
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
            elif self.rect(self.buy_mode_button_rect).collidepoint(possouris):
                self.bool_buy = True

    def right_clic_interactions(self, posssouris):
        pass

    def keydown(self, event_key):
        """
        Methode qui gère les interactions de l'utilisateur avec les touches du clavier
        """
        if self.research_mode:
            if event_key == pygame.K_RETURN:
                self.research_mode = False
            else:
                if self.game.pressed[pygame.K_LSHIFT]:
                    self.update_research_text(pygame.key.name(event_key).upper())
                else:
                    self.update_research_text(pygame.key.name(event_key))

    def mouse_wheel(self, possouris, value):
        """
        Methode qui gère les interactions utilisateurs avec la molette haut/bas de la souris
        @in : int, puissance de l'action molette. Ex : 1 = haut de 1
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

    def is_hovering_buttons(self, possouris):
        if not self.bool_entrer:
            if not self.game.classic_panel.ingame_window.window_bar_rect.collidepoint(possouris):
                return True
        elif self.bool_sell:
            pass
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

    def img_load(self, file_name):
        return pygame.image.load(f'{self.PATH}{file_name}.png')
