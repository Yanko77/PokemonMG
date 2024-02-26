if self.game.player.team[i] is not None:
    if not self.ingame_window.starters_panel.pk_move_mode and not self.ingame_window.sac_panel.emp_move_mode and not self.ingame_window.spawn_panel.spawning_pk_move_mode:
        if not self.pk_move_mode and not self.ingame_window.is_hovering(possouris) and not self.ingame_window.moving:
            if self.game.mouse_pressed[1] and self.pk_rects[i].collidepoint(possouris):
                self.pk_move_mode = True
                self.moving_pk[i] = True
                self.rel_possouris_pk_move_mode = [0, 0]
                self.saved_possouris = possouris

        if self.pk_move_mode and self.moving_pk[i]:
            if not self.logo_pk_suppr_rect.collidepoint(possouris):
                surface.blit(self.logo_pk_suppr, (0, 0))

            if not self.game.mouse_pressed[1]:
                if self.PK_RECTS[0].collidepoint(possouris):
                    self.change_pk_place(i, 0)
                elif self.PK_RECTS[1].collidepoint(possouris):
                    self.change_pk_place(i, 1)
                elif self.PK_RECTS[2].collidepoint(possouris):
                    self.change_pk_place(i, 2)
                elif self.PK_RECTS[3].collidepoint(possouris):
                    self.change_pk_place(i, 3)
                elif self.PK_RECTS[4].collidepoint(possouris):
                    self.change_pk_place(i, 4)
                elif self.PK_RECTS[5].collidepoint(possouris):
                    self.change_pk_place(i, 5)
                elif self.logo_pk_suppr_rect.collidepoint(possouris):
                    if not self.game.player.get_nb_team_members() <= 1:
                        self.game.player.team[i] = None

                self.pk_move_mode = False
                self.moving_pk[i] = False
                self.pk_rects = [pygame.Rect(900, 275, 369, 69), pygame.Rect(900, 348, 369, 69),
                                 pygame.Rect(900, 421, 369, 69), pygame.Rect(900, 494, 369, 69),
                                 pygame.Rect(900, 567, 369, 69), pygame.Rect(900, 640, 369, 69)]
            else:
                self.rel_possouris_pk_move_mode = (possouris[0] - self.saved_possouris[0],
                                                   possouris[1] - self.saved_possouris[1])
                self.pk_rects[i].x = self.PK_RECTS[i].x + self.rel_possouris_pk_move_mode[0]
                self.pk_rects[i].y = self.PK_RECTS[i].y + self.rel_possouris_pk_move_mode[1]

                if self.logo_pk_suppr_rect.collidepoint(possouris):
                    surface.blit(self.logo_pk_suppr_hover, (0, 0))

    if self.game.player.team[i] is not None:
        surface.blit(self.game.player.team[i].icon_image, (self.pk_rects[i].x, self.pk_rects[i].y - 5),
                     (0, 0, 64, 64))
        surface.blit(self.pokemon_name_font.render(self.game.player.team[i].name, False, (0, 0, 0)),
                     (self.pk_rects[i].x + 70, self.pk_rects[i].y + 13))
        level = self.pokemon_level_font.render('Lv.' + str(self.game.player.team[i].level), False, (0, 0, 0))
        surface.blit(level, (self.pk_rects[i].x + 60, self.pk_rects[i].y + 42))

        type_color = game_infos.get_type_color(self.game.player.team[i].get_type())
        type_name_to_print = game_infos.get_type_name_to_print(self.game.player.team[i].get_type())
        type1_render = self.font_pokemon_type.render(type_name_to_print, False, type_color)
        surface.blit(type1_render, ((self.pk_rects[i].x + level.get_width() + 65, self.pk_rects[i].y + 42)))

        type2 = self.game.player.team[i].get_type2()
        if not type2 == 'NoType':
            type2_color = game_infos.get_type_color(type2)
            type2_name_to_print = game_infos.get_type_name_to_print(type2)
            surface.blit(self.font_pokemon_type.render(type2_name_to_print, False, type2_color),
                         ((self.pk_rects[i].x + level.get_width() + type1_render.get_width() + 68,
                           self.pk_rects[i].y + 42)))

        pygame.draw.rect(surface, (35, 35, 35),
                         pygame.Rect(self.pk_rects[i].x + 205, self.pk_rects[i].y + 26, 150, 17))
        pygame.draw.rect(surface, (42, 214, 0), pygame.Rect(self.pk_rects[i].x + 205,
                                                            self.pk_rects[i].y + 26,
                                                            self.game.player.team[i].health / self.game.player.team[
                                                                i].pv * 150,
                                                            17))
        surface.blit(
            self.pokemon_hp_font.render(str(self.game.player.team[i].health) + "/" + str(self.game.player.team[i].pv),
                                        False, (0, 0, 0)), (self.pk_rects[i].x + 205, self.pk_rects[i].y + 40))

        if self.game.player.team[i].objet_tenu is not None:
            surface.blit(self.font_pokemon_type.render('ITEM', False, (30, 30, 30)),
                         (self.pk_rects[i].x + 327, self.pk_rects[i].y + 6))

if i in (0, 2, 4):
    color = (255, 255, 255)
else:
    color = (163, 171, 255)

if self.pk_rects[i].collidepoint(possouris):
    surface.blit(self.create_rect_alpha((369, 69), color), (self.pk_rects[i].x, self.pk_rects[i].y))
    if not self.ingame_window.is_hovering(possouris):
        self.current_hover_pokemon_register[i] = True

        if self.ingame_window.sac_panel.emp_move_mode:
            if self.game.player.team[i] is not None:
                if self.ingame_window.sac_panel.selected_item.target_pokemon == 'All' or \
                        self.game.player.team[i].name == self.ingame_window.sac_panel.selected_item.target_pokemon:

                    if 'Use' in self.ingame_window.sac_panel.selected_item.fonctionnement:
                        surface.blit(self.item_pk_hover_use, (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
                    elif 'Give' in self.ingame_window.sac_panel.selected_item.fonctionnement:
                        if self.game.player.team[i].objet_tenu is None:
                            surface.blit(self.item_pk_hover_give, (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
                        else:
                            surface.blit(self.item_pk_hover_give_error,
                                         (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
                    else:
                        surface.blit(self.item_pk_hover_error, (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
                else:
                    surface.blit(self.item_pk_hover_error, (self.PK_RECTS[i].x - 3, self.PK_RECTS[i].y - 2))
else:
    self.current_hover_pokemon_register[i] = False