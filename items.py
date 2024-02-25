import pygame
import random


class ItemsPanel:
    
    def __init__(self, game):
        self.game = game
        
        self.background = ...
        
        self.open_sell_popup_button = ...
        self.open_buy_popup_button = ...

        self.open_sell_popup_button_rect = ...
        self.open_buy_popup_button_rect = ...
        
        self.boolBuy_popup = False
        self.boolSell_popup = False

        self.buy_popup = BuyPopup(self)
        self.sell_popup = SellPopup(self)
        
    def update(self, surface, window_pos, possouris):
        surface.blit(self.background, (window_pos.x + 20, window_pos.y + 40))

        self.buy_popup.update(surface, window_pos, possouris)

        self.sell_popup.update(surface, window_pos, possouris)

    def update_rects(self, window_pos):
        self.open_sell_popup_button_rect = ...
        self.open_buy_popup_button_rect = ...
    
    def open_buy_popup(self):
        self.boolBuy_popup = True
        self.boolSell_popup = False
        
    def open_sell_popup(self):
        self.boolSell_popup = True
        self.boolBuy_popup = False

    def buy_item(self, objet):
        if self.game.player.money >= objet.buy_price and objet.can_be_buy:
            self.game.player.money -= objet.buy_price
            objet.quantite += 1
            print('achat effectué!')  # a supr
        else:  # a supr
            print('achat non effectué')  # a supr
        # gerer le fait qu'il y en ait 0 initialement peut poser probleme

    def sell_item(self):
        if objet.can_be_sell:
            if objet.variable_sell_price:
                self.game.player.money += random.seed(game.general_seed)
            else:
                if self.game.player.money + objet.sell_price >= 0:
                    self.game.player.money += objet.sell_price
            objet.quantite -= 1

    def left_clic_interactions(self, possouris):
        pass


class BuyPopup:

    def __init__(self, items_panel):
        self.items_panel = items_panel

    def update(self, surface, window_pos, possouris):
        if self.items_panel.boolBuy_popup:
            pass


class SellPopup:

    def __init__(self, items_panel):
        self.items_panel = items_panel

    def update(self, surface, window_pos, possouris):
        if self.items_panel.boolSell_popup:
            pass


