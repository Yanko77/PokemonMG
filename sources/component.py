"""
This file contains Component class.

A Component object represents a component of a displayed panel.
It's able to contain and manage other Component objects so they can work together.
It basically passes on user events to the right component as a Panel object does.

This file also contains Button class which is a specific Component object.
"""

import pygame

import panel as p
import game as g


class Component:

    def __init__(self, owner, prio: int = 0):
        self.owner : p.Panel | Component = owner
        self.game : g.Game = self.owner.game

        self.prio = prio

        self.elements: list[Component] = []

    def update(self, possouris):
        pass

    def sort_elements_by_prio(self):
        self.elements.sort(key=lambda elem: elem.prio)

    def left_click_down(self, possouris):
        for elem in self.elements[::-1]:
            if hasattr(elem, 'is_hovering') and elem.is_hovering(possouris):
                if hasattr(elem, 'left_click_down'):
                    elem.left_click_down(possouris)
                    return True

        return False

    def left_click_up(self, possouris):
        for elem in self.elements[::-1]:
            if hasattr(elem, 'is_hovering') and elem.is_hovering(possouris):
                if hasattr(elem, 'left_click_up'):
                    elem.left_click_up(possouris)
                    return True

        return False

    def is_hovering(self, possouris):
        for elem in self.elements[::-1]:
            if hasattr(elem, 'is_hovering') and elem.is_hovering(possouris):
                return True
        return False

    def img_load(self, img_name: str):
        return self.owner.img_load(img_name)


class Button(Component):

    def __init__(self,
                 owner,
                 rect: pygame.Rect,
                 img_name: str):

        super().__init__(owner=owner,
                         prio=0)

        self.rect = rect
        self.display_pos = (rect.x, rect.y)

        self.image = self.img_load(img_name)
        self.image_hover = self.img_load(f'{img_name}_hover')

    def update(self, possouris):
        self.display(possouris)

    def display(self, possouris):
        if self.is_hovering(possouris):
            self.game.screen.blit(self.image_hover, self.display_pos)
        else:
            self.game.screen.blit(self.image, self.display_pos)

    def func(self):
        pass

    def left_click_up(self, possouris):
        self.func()

    def left_click_down(self, possouris):
        pass

    def is_hovering(self, possouris):
        return self.rect.collidepoint(possouris)