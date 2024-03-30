# Documentation technique | PokémonMG

## TOUS LES MODULES

-  **[accueil.py](#accueilpy)** : *Gestion de l'écran d'accueil*
- **[all_attaques.txt](#all_attaquestxt)** : *Stockage des informations de toutes les attaques | Database*
- **[all_objets.txt](#all_objetstxt)** : *Stockage des informations de tous les objets | Database*
- **[all_pokemons.csv](#all_pokemonscsv)** : *Stockage des informations de tous les Pokémons | Database*
- **[attaques.py](#attaquespy)** : *Gestion des attaques des Pokémons*
- **[dresseur.py](#dresseurpy)** : *Gestion des dresseurs*
- **[evolutions.py](#evolutionspy)** : *Gestion de l'action "Evolution"*
- **[fight.py](#fightpy)** : *Gestion des combats*
- **[game.py](#gamepy)** : *Gestion du jeu*
- **[game_infos.py](#game_infospy)** : *Gestion des infos du jeu*
- **[game_panel.py](#game_panelpy)** : *Gestion du panel principal de jeu*
- **[game_round.py](#game_roundpy)** : *Gestion des tours de jeu*
- **[ingame_windows.py](#ingame_windowspy)** : *Gestion de la fenêtre ingame*
- **[items.py](#itemspy)** : *Gestion de l'action "Items"*
- **[main.py](#mainpy)** : *Programme principal*
- **[notif.py](#notifpy)** : *Gestion des notifications ingame*
- **[objet.py](#objetpy)** : *Gestion des objets*
- **[player.py](#playerpy)** : *Gestion du joueur*
- **[pokemon.py](#pokemonpy)** : *Gestion des Pokémons*
- **[pokemon_attaque_pooltxt](#pokemon_attaque_pool.txt)** : *Stockage des attaques possédées par les Pokémons. | Database*
- **[sac.py](#sacpy)** : *Gestion de l'inventaire du joueur*
- **[sound.py](#soundpy)** : *Gestion des effets sonores du jeu*
- **[spawn.py](#spawnpy)** : *Gestion de l'action "Spawn"*
- **[special_pokemon.py](#special_pokemonpy)** : *Gestion des Pokémons spéciaux des dresseurs*
- **[special_pokemon_attaque_pooltxt](#special_pokemon_attaque_pool.txt)** : *Stockage des attaques possédées par les Pokémons spéciaux | Database*
- **[starters.py](#starterspy)** : *Gestion de l'action "Spawn"*
- **[train.py](#trainpy)** : *Gestion de l'action "Train"*




## *```accueil.py ```*


### ```class  accueil.Accueil([game])```
> Classe représentant l'écran d'accueil du jeu.

### ```.update(surface, possouris)```
> Méthode d'actualisation de l'affichage.  
 >
>	@in : surface, pygame.Surface → fenêtre du jeu  
>	@in : possouris, list → coordonnées du pointeur de souris


### ```.update_intro(surface)```

> Methode qui gère l'affichage de l'intro du lancement du jeu.
>
> @in : surface, pygame.Surface → fenêtre du jeu

### ```.update_home_screen(surface, possouris)```

> Methode d'actualisation de l'affichage de l'écran d'accueil.      
> 
> @in : surface, pygame.Surface → fenêtre du jeu
> @in : possouris, list → coordonnées du pointeur de souris

### ```.clic(button_name)```

> Méthode d'éxécution de l'action de clic du joueur
> 
> @in : button_name, str → nom associé au bouton

### ```.left_clic_interactions(possouris)```

> Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.
> 
> @in : possouris, list → coordonnées du pointeur de souris

### ```.is_hovering_buttons(possouris)```

> Méthode qui détecte si le joueur pointe le curseur de la souris sur un bouton de l'écran d'accueil.
> Retourne un booléen : True si le curseur est sur un bouton, False sinon
> 
> @in : possouris, list → coordonnées du pointeur de souris
> @out : bool

### ```.img_load(path)```

> Methode de chargement d'image dépendant du chemin d'accès (self.PATH, une constante).
> Retourne une surface pygame.
> 
> @in : path, str → chemin d'accès du fichier depuis self.PATH

## *```all_attaques.txt ```*

### Fichier qui contient toutes les informations sur les attaques des Pokémons.

> **Format :** ```Name	type	pp	puissance	precision	taux_crit	priorite	spécialités```

## *```all_objets.txt ```*

### Fichier qui contient toutes les informations sur les objets des Pokémons.

> **Format :** ```Name spawning_infos catégorie fonctionnement achat vente description```

## *```all_pokemons.csv ```*

### Fichier qui contient toutes les informations sur les stats des Pokémons.

> **Format :** ```Name, rareté, type, pv, attack, defense, speed, evolution_level, evolution_name, player_lv_to_spawn, type2, min_lv_at_spawn, max_lv_at_spawn```


## *```attaques.py ```*


### ```class  attaques.Attaque([name], [pp]=None)```
> Classe représentant une attaque de pokémon.

### ```.get_stats()```

> Methode qui retourne toutes les stats de l'attaque :
> 
> - Son type, str
> - Son nombre de PP, int
> - Sa puissance, int (ou str si puissance spéciale)
> - Sa precision, int
> - Ses chances de critique, float
> - Sa priorité, int
> - Ses effets spéciaux, list
> 
> @out: tuple

### ```.get_name(surface)```

> Méthode qui retourne le nom de l'attaque.   
> Retourne le nom à afficher si mode_affichage est True.   
> Retourne le nom en interne du jeu sinon.
> 
> - Exemple avec l'attaque Croc Fatal :   
> - - nom en interne du jeu : "Croc_Fatal"   
> - -  nom à afficher : "Croc Fatal"
> 
>@in: mode_affichage, bool   
>@out: str

### ```.set_pp(amount)```

> Methode qui permet de définir le nombre de PP de l'attaque.  
> 
> @in: amount, int

### ```.reformate_name()```

> Methode de reformatage du nom de l'attaque.
> Tranforme le nom en interne du jeu en nom à afficher pour le joueur.
> 
> @out: name, str

### ```.find_attaque_line()```

> Methode qui trouve, lit et renvoie le ligne d'infos de l'attaque.  
> 
> @out: list




## *```dresseur.py ```*


### ```class  dresseur.Dresseur([name], [pp], [type], [power], [pk_lists]=None, [pk]=None)```

> Super-Classe représentant un dresseur (PNJ).  
Un dresseur est défini par:  
>
> - Son nom, str
> - La game dans laquelle il intervient, game.Game
> - Sa classe, str
> - Sa puissance, int
> - La liste de pokémons qu'il peut posséder, list
> - Le pokémon qu'il possède s'il est déjà déterminé, pokemon.Pokemon

### ```.init_pk()```

> Methode qui initialise et/ou détermine le pokémon du dresseur.


### ```.init_inventory()```

> Methode qui initialise l'inventaire du dresseur et détermine son contenu.


### ```.get_pk_level()```

> Methode qui calcul le niveau du pokémon du dresseur.
> 
> 
> Ce niveau est calculé de manière aléatoire dans un intervalle de 2
> valeurs entières.
> 
> 
> @out: int → niveau du pokémon.



### ```.get_infos()```

> Methode qui retourne les infos du dresseur:  
> - Son nom, str  
> - Sa classe, str  
> - Sa puissance, int  
> - Son inventaire, list      
>
>@out: tuple


### ```class  dresseur.Sauvage([game], [pk]) // Super-class : dresseur.Dresseur```

> Classe représentant le maitre des pokémons sauvages du jeu.

### ```class  dresseur.Alizee([game], [pk]) // Super-class : dresseur.Dresseur```

> Classe représentant le dresseur du nom de Alizee.

### ```class  dresseur.Red([game], [pk]) // Super-class : dresseur.Dresseur```

> Classe représentant le dresseur du nom de Red.

### ```class  dresseur.Blue([game], [pk]) // Super-class : dresseur.Dresseur```

> Classe représentant le dresseur du nom de Blue.

### ```class  dresseur.Pierre([game], [pk]) // Super-class : dresseur.Dresseur```

> Classe représentant le dresseur du nom de Pierre.


### ```class  dresseur.Ondine([game], [pk]) // Super-class : dresseur.Dresseur```

> Classe représentant le dresseur du nom de Ondine.


### ```class  dresseur.Olea([game], [pk]) // Super-class : dresseur.Dresseur```

> Classe représentant le dresseur du nom de Olea.


### ```class  dresseur.Iris([game], [pk]) // Super-class : dresseur.Dresseur```

> Classe représentant le dresseur du nom de Iris.


### ```dresseur.get_dresseur_by_name(name) ```

> Fonction qui retourne la classe du dresseur à partir de son nom (prise en compte des accents !).  
> 
> @in: name, str
> @out: dresseur_class issu de la super-classe Dresseur.


## *```evolutions.py ```*

### ```class evolutions.EvolPanel([game])``` 

> Classe représentant le panel de l'action Evolution.   
> Le joueur peut faire évoluer un Pokémon.

  
### ```.update(surface, possouris, window_pos)```

> Méthode d'actualisation de l'affichage du panel.      
> 
> @in : surface,pygame.Surface → fenêtre du jeu   
> @in : possouris, list → coordonnées du pointeur de souris   
> @in : window_pos, list → coordonnées de la fenêtre ingame

  
### ```.update_evol_pk(surface, possouris)```

> Methode d'actualisation de l'affichage du pokémon à évoluer.      
> 
> @in : surface, pygame.Surface → fenêtre du jeu   
> @in : possouris, list →coordonnées du pointeur de souris

  
### ```.update_pk_emp(surface, possouris)```

> Methode d'actualisation de l'affichage de l'emplacement pokémon à évoluer.     
> 
> @in : surface, pygame.Surface → fenêtre du jeu   
> @in : possouris, list → coordonnées du pointeur de souris

  
### ```.update_evol_button(surface, possouris)```

> Méthode d'actualisation de l'affichage du bouton pour évoluer.     
> 
> @in : surface, pygame.Surface → fenêtre du jeu   
> @in : possouris, list → coordonnées du pointeur de souris

  
### ```.update_evolving_pk()```

> Methode permettant de changer le pokémon à évoluer du joueur

  
### ```.update_rects(window_pos)```

> Methode d'actualisation des positions des rects du panel en fonction de la position de la fenetre ingame.    
>   
> @in : window_pos, list → coordonnées de la fenêtre ingame

  
### ```.add_pk_to_team(team_i) ```

> Methode qui ajoute un pokémon à l'équipe (redondance avec une méthode de l'objet Player)      
> 
> @in : team_i, int → indice du pokémon dans l'équipe.

  
### ```.reset()```

> Méthode de réinitialisation du panel.  
>  Utilisée lors de l'initialisation d'un nouveau tour de jeu.
  
 ### ```.close()```  

> Méthode classique qui éxécute tout ce qu'il faut faire lorsque le panel est fermé.
> 

  
 ### ```.left_clic_interactions(possouris)```

> Méthode gérant les intéractions de l'utilisateur avec le clic gauche  de la souris.
> 
> @in : possouris, list → coordonnées du pointeur de souris

  
 ### ```.is_hovering_buttons(possouris)```

> Méthode qui retourne True si la souris est positionnée sur un bouton du panel.  
> 
> @in : possouris, list → coordonnées du pointeur de souris  
> @out : bool

## *```fight.py```*
  
  
###  ```class fight.Fight([game], [player_pk], [dresseur]=None, [difficult]='easy, [fight_type]='Classic')```:  

> Classe représentant un combat entre le pokémon du joueur, et un dresseur (PNJ)      
> Classe définie par:  
> - La game, game.Game  
> - Le pokémon du joueur, pokemon.Pokemon  
> - Le dresseur  
> - La difficulté du combat, str  
> - Le type de combat, str →  ('Classic' ou 'Boss')

  
###  ```.update(surface, possouris)```
  
> Methode d'actualisation de l'affichage du combat.      
> 
> @in : surface, pygame.Surface → fenêtre du jeu   
> @in : possouris, list → coordonnées du pointeur de souris

  
###  ```.update_end_panel(surface)```

> Methode d'actualisation de l'affichage du panel de fin de combat.    
>  
> @in : surface, pygame.Surface → fenêtre du jeu

  
###  ```.update_current_action(possouris)```

> Methode permettant de modifier l'action en cours du joueur.    
>   
> @in : possouris, list → coordonnées du pointeur de souris

  
###  ```.update_turn_exec_info(surface)```

> Methode d'actualisation de l'affichage des infos d'execution du tour du combat.  
>     
> @in : surface, pygame.Surface → fenêtre du jeu

  
###  ```.update_fight_buttons(surface, possouris)```

> Methode d'actualisation de l'affichage des boutons du combat.      
> 
> @in : surface, pygame.Surface → fenêtre du jeu   
> @in : possouris, list → coordonnées du pointeur de souris

  
###  ```.update_pokemons(surface)```

> Methode d'actualisation de l'affichage des pokémons (Celui du joueur et celui du dresseur).
> 
> @in : surface, pygame.Surface → fenêtre du jeu

  
###  ```.animate_player_pk_damage(surface)```

> Methode d'actualisation de l'affichage de l'animation de la barre rouge de dégats subis par le pokémon du joueur.      
> 
> @in : surface, pygame.Surface → fenêtre du jeu

  
###  ```.animate_dresseur_pk_damage(surface)```

> Methode d'actualisation de l'affichage de l'animation de la barre rouge de dégats subis par le pokémon du dresseur.
> 
> @in : surface, pygame.Surface → fenêtre du jeu

  
###  ```.sac_item_update(surface, possouris, item, i)```


> Methode d'actualisation de l'affichage de l'emplacement d'objet dans l'action 'SAC'.
> 
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  
> @in : item, objet.Objet   
> @in : i, int → indice de l'item dans le sac

  
###  ```.sac_curseur_update(possouris)```

> Methode d'actualisation de la position du curseur et de la possibilité de le déplacer à la souris.  
>     
> @in : possouris, list → coordonnées du pointeur de souris

  
###  ```.get_action_order(player_pk_action, dresseur_pk_action)```

> Déterminer l'ordre d'agissement des 2 pokemons.   
> Renvoie le premier pokémon à attaquer.      
> 
> @in : player_pk_action & dresseur_pk_action, tuple → ('ITEM', objet.Objet(), i) ou ('ATTAQUE', attaques.Attaque()) 
> @out : str →  "player_pk" ou "dresseur_pk"

  
###  ```.turn(player_pk_action)```
  

> Methode qui réalise le tour de combat.   
> Ordre :  
> - Actualisation des effets de status des 2 pokémons  
> - Attaque du 1er pokemon  
> - Attaque du 2e pokemon (si encore vivant)  
> - Application des effets de status sur le 1er pokémon (si encore vivant)  
> - Application des effets de status sur le 2e pokémon (si encore vivant)      
>
> @in: tuple → action du joueur

  
###  ```.exec_item_action(pk, item, i)```

> Methode qui execute l'action d'un pokémon d'utiliser un item lors du tour.

  
###  ```.exec_attaque_action(pk, ennemy_pk, attaque)```

> Methode qui execute l'action du pokémon d'attaquer      
> 
> @in : pk, pokemon.Pokemon → Pokémon attaquant   
> @in : ennemy_pk, pokemon.Pokemon → Pokémon défenseur   
> @in : attaque, attaques.Attaque → attaque éxécutée

###  ```.update_fight_logs(surface)```

> Methode d'actualisation de l'affichage des logs du combat.      
> 
> @in : surface, pygame.Surface → fenêtre du jeu

  
###  ```.get_rewards()```

> Methode permettant de donner au joueur les recompenses du combat.

  
###  ```.end_fight()```

> Methode permettant de terminer le combat.

  
###  ```.apply_status_effects(pk)```

> Methode qui applique les effets de status du pokémon pris en parametre d'entrée.    
>   
> @in : pk, pokemon.Pokemon

###  ```.update_status_effects(pk)```

> Methode d'actualisation des effets de status du pokémon pris en parametre d'entrée.
> 
> @in : pk, pokemon.Pokemon

  
###  ```.update_pk_attaques(player_pk_action, dresseur_pk_action)```

> Methode d'actualisation de certain effets des attaques des pokémons d'un tour à l'autre.    
>   
> @in : player_pk_action, tuple → ('ITEM', objet.Objet) ou ('ATTAQUE', attaques.Attaque)   
> @in : dresseur_pk_action, tuple → ('ITEM', objet.Objet) ou ('ATTAQUE', attaques.Attaque)

  
###  ```.update_pk_item()```

> Methode qui actualise les effets des objets tenus par les pokemons


###  ```.left_clic_interactions(possouris)```

> Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.
> 
> @in : possouris, list → coordonnées du pointeur de souris

  
###  ```.is_hovering(possouris)```

> Méthode qui retourne True si la souris est positionnée sur un bouton du panel.
> 
> @in : possouris, list → coordonnées du pointeur de souris   
> @out : bool


###  ```fight.calcul_degats(pk, ennemy_pk, attaque, crit=False)```

> Methode de calcul des dégats simulés d'une attaque du pokémon du PNJ sur le pokémon du joueur.   
> Retourne le montant de dégats de la simulation sur le pokémon du joueur.  
>   
>   
> @in: pk, pokemon.Pokemon => Pokémon du PNJ   
> @in: ennemy_pk, pokemon.Pokemon => Pokémon du joueur 
> @in: attaque, attaque.Attaque => Attaque simulée   
> @in: crit, bool => True si l'attaque critique, False sinon   
> @out: degats, int


  
  
###  ```fight.get_npc_action(pk, ennemy_pk, att)```

> Fonction de selection de la meilleure action à réaliser pour le pokémon du PNJ. 
> Retourne l'attaque à réaliser.   
>     
> @in : pk, pokemon.Pokemon => Pokémon du PNJ
> @in : ennemy_pk, pokemon.Pokemon => Pokémon du joueur   
> @in: att, list => liste d'attaque du pokémon du PNJ   
> @out : attaque.Attaque => Meilleure attaque à réaliser pour le pokémon du PNJ

## *```game.py```*

###  ```class game.Game()```  
  

> Classe représentant le jeu.   
> Initialise tous les elements du jeu.

  
###  ```.update(screen, possouris)```

> Methode d'actualisation de l'affichage du jeu   
>    
> @in : surface, pygame.Surface → fenêtre du jeu   
> @in : possouris, list → coordonnées du pointeur de souris

  
###  ```.notif(text, color)```

> Methode permettant d'emettre une notification.      
> 
> @in: text, str  
> @in: color, tuple

  
###  ```.get_fighting_dresseur()```

> Methode permettant de determiner et de retourner le dresseur à combattre lors du combat final de fin de tour. 
>      
> @out: dresseur.Dresseur class

  
###  ```.init_new_game()```

> Methode d'initialisation d'une nouvelle partie.

  
###  ```.create_new_game()```

> Methode de création d'une nouvelle partie.

  
###  ```.start_new_game()```

> Methode de démarrage d'une nouvelle partie.

  
###  ```.load_game()```

> Methode de lancement d'une partie à charger depuis les fichiers de sauvegarde.

  
###  ```.game_over()```

> Methode permettant de relancer le jeu après qu'il se soit terminé.

  
###  ```.start_fight(player_pk, dresseur=None, difficult="easy", fight_type='Classic')```

> Methode de lancement de combat.   
> 
> @in : *voir fight.Fight*

  
###  ```.cancel_fight()```

> Methode d'annulation du combat en cours.

  
###  ```.end_fight()```

> Methode de fin du combat en cours.

  
###  ```.init_fight(player_pk , dresseur=None, difficult='easy', fight_type='Classic')```

> Methode d'initialisation d'un combat.   
> 
> @in : *voir fight.Fight*

  
###  ```.next_turn()```

> Methode permettant de passer au tour de jeu suivant.

###  ```.get_init_pokemon_id()```

> Methode permettant de récupérer l'id unique d'un pokémon.      
> @out: id, int → id unique.

  
###  ```.update_variable_item_price()```

> Methode permettant d'actualiser le prix variables des objets concernés.

  
###  ```.get_item_price(item)```

> Methode qui retourne le prix de l'item rentré en parametre      
> 
> @in : item, objet.Objet

  
###  ```.(init_items_list)```

> Methode d'initialisation de la liste de tous les items du jeu.     
> 
> @out : list

  
###  ```.get_all_items_list()```

> Methode qui retourne la liste de tous les items du jeu.      
> Retourne le dict: {  
>  'All': all_items,
>  'Use': use_items,
>  'Give': give_items,   
>  'Sell': sell_items,
>  'Enable': enable_items,  
> 'Spawnble': spawnable_items  
>  }  

>   @out: items_list, dict

###  ```.get_items_list()``` 

> Methode qui renvoie la liste des objets du jeu.

  
###  ```.init_pokemons_list()``` 

> Methode d'initialisation de dictionnaire de tous les pokémons du jeu et leurs infos.     
> 
>  @out : dict

  
###  ```.init_special_pokemons_list()```

> Methode d'initialisation de dictionnaire de tous les pokémon spéciaux du jeu et leurs infos      
> 
> @out : dict

  
###  ```.get_total_items_rarity()```

> Methode qui renvoie la somme de toutes les raretés des objets du jeu obtenable via spawn.     
>  
> @out : int

  
###  ```.update_random_seed()```  

> Methode d'actualisation de la seed aléatoire du jeu.

  
###  ```.save()```

> Méthode d'écriture de la sauvegarde du jeu.



  
###  ```.write_down_backup(file_name, listecsv)```

> Methode qui écrit la sauvegarde dans le fichier en mémoire.

  
###  ```.load()```

> Methode qui charge la sauvegarde du jeu.

  
###  ```.get_bool_save()```

> Returne True si une partie est sauvegardée,   False sinon. 
> 
> @out: bool

##  *```game_infos.py```*

###  ```game_infos.get_all_diff_pokemons(game, attacking_pokemon, level, difficulty='easy')```

> Methode qui retourne la liste de tous les pokémons d'un certain niveau pouvant apparaitre contre le pokémon du joueur selon la difficulté du combat.  
> 
> @in: game, game.Game   
> @in: attacking_pokemon, pokemon.Pokemon   
> @in: level, int => Niveau d'apparition du pokémon   
> @in: difficulty, str

###  ```game_infos.get_diff_types(pokemon_type, pokemon_type2, multiplicateur)```

> Methode retournant la liste de tous les types des pokémons pouvant apparaitre selon les types du pokémon du joueur et l'affinité de type attendue.  
> 
> @out: types_list, list

##  *```game_panel.py```*

###  ```class game_panel.GamePanel([game])``` 

> Classe qui représente le panel principal du jeu  

  
###  ```.update(surface, possouris)```
> Methode d'actualisation de l'affichage de l'ecran principal du jeu.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  
  
###  ```.update_fight_popup(surface, possouris)```

> Methode d'actualisation de l'affichage du popup FIGHT.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.update_player_infos(surface, possouris)```

>Methode d'actualisation de l'affichage des infos du joueur.  
  
>@in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.update_player_name()```

> Methode d'actualisation de l'image du nom du joueur  

  
###  ```.display_player_name( surface, possouris)```

> Methode d'actualisation de l'affichage du nom du joueur.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.update_player_lv(surface)``` 

> Methode d'actualisation de l'affichage du niveau du joueur.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  

  
###  ```.update_hover_pokemon()```

> Methode d'actualisation du pokémon sur lequel pointe le curseur de souris.  

  
###  ```.update_player_name_editing_mode(surface)```

> Methode d'actualisation de l'affichage du mode d'edition du nom du joueur.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  

  
###  ```.update_team_pokemons(surface, possouris)```

> Methode d'actualisation de l'affichage de l'equipe du joueur.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.update_pokemon(surface, possouris, i)```

> Méthode d'actualisation de l'affichage du pokémon dans l'équipe.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  
> @in : i, int → indice du pokémon dans l'équipe  

  
###  ```.update_pk_move(possouris, i)```  

> Méthode d'actualisation du déplacement du pokémon par le joueur sur le panel de jeu.  
  
> @in : possouris, list → coordonnées du pointeur de souris  
> @in : i, int → indice du pokémon dans l'équipe  

  
###  ```.update_pokemon_info(surface, possouris)```  

> Méthode d'actualisation de l'affichage des infos du pokémon dans l'équipe.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.update_cursor(possouris)```

> Méthode d'actualisation du pointeur de la souris.  
  
> @in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.update_go_fight_button(surface, possouris)```

> Méthode d'actualisation de l'affichage du bouton "Go fight".  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.start_fight()```  

> Méthode démarrage de combat  

  
###  ```.next_turn()```

> Méthode de passage au tour suivant  

  
###  ```.left_clic_interactions(possouris)```


> Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.  
  
> @in : possouris, list → coordonnées du pointeur de souris  


  
###  ```.right_clic_interactions(possouris)```

> Méthode gérant les intéractions de l'utilisateur avec le clic droit de la souris.  
  
> @in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.keydown(event_key)```  

> Méthode gérant les intéractions de l'utilisateur avec le clavier.  
  
> @in : event_key, int → valeur associée à la touche appuyée  

  
###  ```.get_interactions(possouris)```

>Méthode qui retourne True si la souris est positionnée sur un bouton.  
  
>@in : possouris, list → coordonnées du pointeur de souris  
>@out : bool  

  
###  ```.change_pk_place(i1, i2)```

> Méthode d'inversion de place de 2 pokémons dans l'équipe.  
  
> @in : i1, int → indice du pokémon 2 dans l'équipe  
> @in : i2, int → indice du pokémon 2 dans l'équipe  

###  ```.is_hovering_team_pokemon(possouris)```

> Méthode qui retourne True si la souris est positionnée sur un pokémon de l'équipe.  
  
> @in : possouris, list → coordonnées du pointeur de souris  
> @out : bool  

  
###  ```.is_hovering_pokemon_info_popup_buttons(possouris)``` 

> Méthode qui retourne True si la souris est positionnée sur un bouton du popup d'infos des pokémons.  
>  
> @in : possouris, list → coordonnées du pointeur de souris  
> @out : bool  

  
  
###  ```class game_panel.GamePanelButtons()```

> Classe gérant les boutons d'action du panel principal du jeu.  

  
###  ```.update(surface, possouris, ingame_window)```

> Méthode d'actualisation de l'affichage des boutons d'action du panel principal du jeu.  
>
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  
> @in : ingame_window, ingame_window.IngameWindow → fenêtre ingame du jeu  


##  *```game_round.py```*

###  ```class  game_round.Round([game])```

> Classe représentant le tour de jeu.  

###  ```.next()```

> Méthode permettant de passer au tour de jeu suivant.  

  
###  ```.set_new_random_seed(seed=None)```

> Méthode qui détermine la nouvelle seed aléatoire.  

  
###  ```.generate_round_random_seed()```

> Méthode de génération de seed aléatoire.  
> @out: int  

##  *```ingame_windows.py```*

###  ```class ingame_windows.IngameWindow()```
  
> Classe représentant la fenêtre ingame du jeu.  

  
###  ```.update(surface, possouris)``` 
 
> Méthode d'actualisation de l'affichage de la fenêtre ingame.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  

###  ```.update_buttons(surface, possouris)```

> Fonction qui gère l'affichage des boutons.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  

###  ```.update_window_pos(possouris)```

> Méthode d'actualisation de la position de la fenêtre lorsqu'elle est déplacée par le joueur.  
  
> @in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.rectif_window_rect()``` 
 
> Fonction qui rectifie la position de la fenetre si celle-ci n'est pas correcte.  

  
###  ```.update_all_rects()```  

> Fonction qui modifie tous les rects de la fenetre en fonction de sa position sur l'ecran  

  
###  ```.update_panel(panel_name)```

>Méthode d'actualisation du panel courant de la fenêtre.  
  
>@in : panel_name, str  

  
###  ```.open()```
  
> Méthode d'ouverture de la fenêtre ingame  

  
###  ```.close()```

> Méthode de fermeture de la fenêtre ingame  

  
###  ```.minimize()```

> Méthode de minimisation de la fenêtre ingame  

  
###  ```.maximize()```

> Méthode de maximisation de la fenêtre ingame  

  
###  ```.reset_all_panels()```

> Méthode de réinitialisation de tous les panels de la fenêtre ingame  

  
###  ```.is_hovering(possouris)```
 
> Méthode qui retourne True si la souris est positionnée sur la fenêtre.  
  
> @in : possouris, list → coordonnées du pointeur de souris  
> @out : bool  

  
###  ```.is_hovering_buttons(possouris)```

> Méthode qui retourne True si la souris est positionnée sur un bouton de la fenêtre.  
  
> @in : possouris, list → coordonnées du pointeur de souris  
> @out : bool  

  
###  ```.left_clic_interactions(possouris)```

> Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.  
  
> @in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.right_clic_interactions(possouris)```

> Méthode gérant les intéractions de l'utilisateur avec le clic droit de la souris.  
  
> @in : possouris, list → coordonnées du pointeur de souris  


##  *```items.py```*

###  ```class items.ItemsPanel()```:  
 
> Classe représentant le panel d'action "Items".  
  
> Dans ce panel, le joueur pourra :  
> - Acheter des items.  
> - Vendre des items.  

  
###  ```.update(surface, possouris, window_pos)```(self, ):  

> Méthode d'actualisation de l'affichage du panel.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  
> @in : window_pos, list → coordonnées de la fenêtre ingame  

  
###  ```.display_entrer_panel(surface)```

> Methode qui actualise l'affichage du panel pour entrer dans le magasin.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  

  
###  ```.display_choisir_panel(surface, possouris)```(self, : pygame.Surface, : list):  

> Methode qui actualise l'affichage du panel de choix de type de transaction (Payer ou Acheter).  
  
>@in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.display_buy_panel(surface, possouris)```
  
>Methode qui gère l'actualisation de l'affichage du panel d'achat d'objets.  
  
>@in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.display_sell_panel(surface, possouris)```

>Methode qui gère l'actualisation de l'affichage du panel de vente d'objets.  
  
>@in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.display_categories(surface, possouris)```
 
>Méthode d'actualisation de l'affichage des catégories.  
  
>@in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  

  

###  ```.display_buy_items_emps(surface, possouris)```

>Méthode d'actualisation de l'affichage des emplacements d'objets du panel d'achat.  
 > 
>@in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  
  
  
###  ```.display_sell_items_emps(surface, possouris)```

>Méthode d'actualisation de l'affichage des emplacements d'objets du panel de vente.  
  
>@in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.display_item_desc(surface)```

>Methode qui actualise l'affichage de la description de l'item sélectionné.  
  
>@in : surface, pygame.Surface → fenêtre du jeu  

  
###  ```.display_curseur(surface, possouris)```

>Methode d'actualisation de l'affichage du curseur.  
>  
>@in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.display_research_text(surface)```  

>Methode d'actualisation de l'affichage du texte recherché dans la barre de recherche.  
  
>@in : surface, pygame.Surface → fenêtre du jeu  

  
###  ```.rect(rect)```

>Méthode qui retourne le rect réel par rapport à la fenêtre du jeu.  
  
>@in : rect, pygame.Rect  
>@out : pygame.Rect → rect modifié  

  
###  ```.display(image, pos, surface, rect=None)``` 

>Méthode d'affichage d'une image.  
>Prend en paramètre une position relative à la fenêtre ingame.  
  
>@in : image, pygame.Surface → image à afficher  
>@in : pos, tuple ou pygame.Rect → position souhaitée relative à la fenêtre ingame  
>@in : surface, pygame.Surface → fenêtre du jeu  
>@in : rect, pygame.Rect ou None → zone de l'image à afficher  
  

  
###  ```.update_selected_item(possouris)```

>Methode d'actualisation de l'item sélectionné en fonction de la position du pointeur de souris.  
  
>@in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.update_curseur_rect()```

>Méthode d'actualisation du rect du curseur.  

  
###  ```.update_research_text(character)```

>Méthode d'actualisation de la recherche du joueur.  
>Ajoute à la recherche le character pris en entrée ou éxécute l'action liée à la touche spéciale appuyée.  
  
>@in : character, str  

  
###  ```.update_current_items_list()```
  
>Méthode d'actualisation des listes d'objets dépendant des critères de recherche actuels.  

###  ```.buy_item(item)```

>Methode qui permet d'acheter un objet.  
>
>@in : item, objet.Objet → Objet à acheter  
  
###  ```.sell_item(item)```

>Methode qui permet de vendre un objet.  
>
>@in : item, objet.Objet → Objet à vendre  

  
###  ```.tri_croisant_prix(liste_objet, mode='Buy')``` 

>Méthode de tri d'une liste d'objet par tri croissant.  
>→ Algorithme de tri par insertion.  
  
>@in : liste_objet, list  
>@in : mode, str → 'Buy' ou 'Sell'  
>@out : list  

  
###  ```.research_item(mode='Buy')```
 
>Methode de recherche d'objet dans la boutique.  
  
>@in : mode, str → 'Buy' ou 'Sell'  
>@out : list → liste des objets triés  

  
###  ```.research_categorie(liste_obj, categorie, mode='Buy')``` 

>Méthode de recherche en fonction de la catégorie sélectionnée.  
>  
>@in : liste_obj, list → liste d'objets à répertorier selon la catégorie et à trier  
>@in : categorie, str  
>@in : mode, str → 'Buy' ou 'Sell'  
>@out : list  

  
###  ```.reset_research()``` 

>Methode de reinitialisation de la recherche.  

  
###  ```.close()``` 

>Méthode classique qui éxécute tout ce qu'il faut faire lorsque le panel est fermé.  

  
###  ```.left_clic_interactions(possouris)``` 

>Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.  
>  
>@in : possouris, list → coordonnées du pointeur de souris  

  
###  ```.keydown(event_key)```  

>Methode qui gère les interactions de l'utilisateur avec les touches du clavier.  
>  
>@in : event_key, int → valeur associée à la touche appuyée  

  
###  ```.mouse_wheel(possouris, value)```(self, possouris: list, value: int):  

>Methode qui gère les interactions utilisateurs avec la molette haut/bas de la souris  
>@in : possouris, list → coordonnées du pointeur de souris  
>@in : value, int → puissance de l'action molette. Ex : 1 = haut de 1  
>-2 = bas de 2  

  
###  ```.is_hovering_buttons(possouris)```

> Méthode qui retourne True si la souris est positionnée sur un bouton du panel.  
>   
> @in : possouris, list → coordonnées du pointeur de souris  
> @out : bool  

 ##  *```main.py```*
 Fichier contenant le programme principal du jeu.

###  ```main()```

> Fonction de lancement du programme du jeu


##  *```notif.py```*

###  ```class notif.Notif()```:  

> Classe représentant les notifications en jeu.  

  
###  ```.update(surface)``` 

>Méthode d'actualisation de l'affichage de la notification.  
 > 
>@in : surface, pygame.Surface → fenêtre du jeu  

  
###  ```.new_notif(text, color)```

>Méthode permettant d'émettre une nouvelle notification  
>  
> @in : text, str  
> @in : color, tuple  
  
  
###  ```.start_animation()```

> Méthode de démarrage de l'animation de la notification  

##  *```objet.py```*

###  ```class objet.Objet([name], [game], [quantite]=1)```:  

> Classe représentant un objet du jeu.  
>  
>Un objet est défini par :  
>- son nom, str  
>- la game dans laquelle il intervient, game.Game  
>- sa quantité, int  

  
###  ```.set_special_effects()``` 

> Méthode d'initialisation des effets spéciaux de l'objet.  


###  ```.reformate_name(name)```
 
> Méthode de reformatage du nom.  
> Permet de convertir le nom interne au jeu en nom affichable pour le joueur.  
>  
> @in : name, str → nom de l'objet  
> @out : reformated_name, str  

  
###  ```.reformate_desc(desc)```

>Méthode de reformatage de la description de l'objet pour l'affichage dans le sac et la boutique d'objets.  
>
>@in : desc, str  
>@out: list  

  
###  ```.set_quantite_at_spawn()```

> Méthode qui détermine la quantité au spawn de l'objet.  

  
###  ```.find_item_line()``` 

>Méthode qui renvoie la ligne du fichier contenant en brut les informations concernant l'objet.  
 > 
>@out: list  

  
###  ```.enable_item()```

> Méthode d'activation de l'objet, s'il est activable.  


  
###  ```.set_sell_price()```  

>Méthode d'actualisation du prix de vente.  
>Utile notamment pour les gérer le principe de prix variables du marché  

##  *```player.py```*

###  ```class player.Player([game])```:  
  
> Classe représentant le joueur.  

  
###  ```.edit_name(key)```

> Méthode d'édition du nom du joueur.  
> 
> @in : key, int → valeur associée à la touche appuyée. Voir pygame.key.  

  
###  ```.reset_name()```

> Méthode de réinitialisation du nom du joueur.  

  
###  ```.reset_actions()```

> Méthode de réinitialisation du nombre d'actions.  

  
###  ```.swap_sac_items( i1, i2)```

> Fonction qui echange la place de 2 items dans le sac.  
 >  
> @in : i1, int → indice de l'objet 1 dans le sac  
> @in : i2, int → indice de l'objet 2 dans le sac  

  
###  ```.find_sac_itemitem()``` 

> Methode qui renvoie l'index de l'item recherché dans le sac.  
> Renvoie None s'il n'est pas présent.  
  
> @in : item, objet.Objet  
> @out: i, int ; None  

  
###  ```.find_sac_item_by_str(item_name)```

> Methode qui renvoie l'index de l'item recherché dans le sac à partir de son nom.  
> Renvoie None s'il n'est pas présent;  
  
> @in : item, objet.Objet  
> @out: i, int ; None  

  
###  ```.add_sac_item(item)```
 
>Fonction qui ajoute au sac un objet et qui le stack si possible.  
>  
>@in : item, objet.Objet  

  
###  ```.remove_item_sac(index)```

> Retire un objet du sac.  
> Ne tient pas compte de la quantité de l'objet.  
>  
> @in : index, int → indice de l'objet dans le sac.  

  
###  ```.add_team_pk(pk, i=0)``` 

> Méthode qui ajoute un pokémon à l'équipe.  
>   
> Essaye de le placer à l'indice voulu.  
> Si c'est impossible, le place à la suite.  
> Si c'est impossible, ne fait rien.  
>   
> @in : pk, pokemon.Pokemon  
>@in: i, int → indice voulu  
  
###  ```.use_action(amount=1)```

> Méthode d'utilisation de points d'actions.  
> Le nombre de points d'actions est pris en parametre d'entrée.  
>  
> @in : amount, int  

  
###  ```.payer(price)```

> Methode qui permet au joueur de payer la somme rentrée en paramètre d'entrée.  
> Renvoie True s'il a payé, False sinon.  
> 
> @in : price, int  

###  ```.level_up(nb_lv=1)```

>Méthode d'augmentation du niveau du joueur.  
 > 
>@in : nb_lv, int → Nombre de niveau d'augmentation du joueur voulu.  

  
###  ```.add_money(amount)```

>Méthode d'ajout d'argent au porte-monnaie du joueur.  
>
>@in : amount, int → Valeur ajoutée  
 
  
###  ```.rise_max_actions_value()```  

> Méthode d'augmentation du nombre d'actions maximum réalisables par tour.  

  
###  ```.get_nb_team_members()```  
 
>Méthode qui retourne le nombre de pokémon présent dans l'équipe.  

  
###  ```.is_team_empty()```
  
> Retourne True si l'équipe est vide, False sinon.  
> 
>@out : bool  

  
###  ```.next_turn()```

> Methode qui éxécute toutes les modifications dues au changement de tour de jeu  

##  *```pokemon.py```*
###  ```class pokemon.Pokemon([name], [level], [game], [is_shiny]=None, [objet_tenu]=None)```:  

>Classe représentant un Pokémon du jeu.  
>  
>Un Pokémon est défini par :  
>- son nom, str  
>- son niveau, int  
>- la game dans laquelle il intervient, game.Game  
>- s'il est shiny ou non, bool  
>- l'objet qu'il porte, objet.Objet / None  


  
###  ```.get_infos()```

>Retourne toutes les infos concernant le pokémon  

  
###  ```.find_attaque_pool_line()```
  
> Retourne le nom des attaques du pool d'attaque du pokémon (issu de pokemon_attaque_pool.txt)  

  
###  ```.init_attaque_pool()``` 
> Méthode d'initialisation du pool d'attaque du pokémon.  
>   
> @out : attaque_pool, list  

  
###  ```.level_up(nb_lv=1)```
  
> Méthode d'augmentation du niveau du pokémon.  
  
> @in : nb_lv, int → nombre de niveaux d'augmentation.  

  
###  ```.set_bonus_stats(bonus_stats)```

> Methode qui applique les bonus stats prise en paramètre d'entrée, de la forme:  
> (pvmax_bonus,  
> atk_bonus,  
> def_bonus,  
> speed_bonus,  
> pvmax_multiplicateur,  
> atk_multiplicateur,  
> def_multiplicateur,  
> speed_multiplicateur)  
  
> @in : bonus_stats, tuple  

  
###  ```.evolution()```  

> Méthode permettant de faire évoluer le pokémon.  
> Renvoie un pokémon : son évolution s'il peut évoluer, lui sinon.  
  
> @out: pokemon.Pokemon  

  
###  ```.full_heal()```
  
> Méthode de régénération des pv actuels du pokémon.  

  
###  ```.get_save_infos(delimiter= ',')```

> Méthode qui renvoie la ligne à écrire dans le fichier de sauvegarde pour stocker l'ensemble des infos qui le définissent.  
  
> @in : delimiter, str → délimiteur choisi pour l'écriture des infos. Varie selon le fichier.  
  
> Exemple :  
> Format : Name, level, id, objet, is_shiny, health, all_bonus_stats, is_alive, attaque_pool  
  
> "Pikachu,10,5,None,False,18,0/0/0/0/1/1/1/1,True,Griffe:25/Vive-Attaque:15/None/None"  

  
###  ```.get_bonus_stats_backup()```

>Retourne l'expression à écrire dans le fichier de sauvegarde pour stocker les valeurs des stats bonus du pokémon.  
  
>@out: str  

  
###  ```.get_attaque_pool_backup()```

> Retourne l'expression à écrire dans le fichier de sauvegarde pour stocker le pool d'attaque du pokémon.  
  
> @out : str  

  
###  ```.load_save_infos(save_infos)``` 

>Methode qui charge les informations sauvegardées du pokémon.  
  
>@in : save_infos, list  

  
###  ```.heal(value)```

>Méthode de régénération des pv actuels du pokémon.  
  
>@in : value, int → nombre de pv à régénérer  

  
###  ```.damage(amount)```

>Méthode faisant subir au pokémon des dégats  
  
>@in : amount, int → nombre de points de pv en dégats subis  

  
###  ```.attaque(pokemon, attaque)``` 

> Attaque le pokémon renseigné en parametre avec l'attaque prise en entrée.  
  
> Renvoie une liste contenant :  
> - True si l'attaque a abouti, False sinon  
> - None si l'attaque n'a pas appliqué d'effet à personne, (<nom_effet>, <self ou pokemon>) sinon  
  
> @in : pokemon, pokemon.Pokemon → pokémon défenseur qui subira l'attaque  
> @in : attaque, attaques.Attaque → attaque lancée  
> @out : list  

###  ```.reset_status()```

> Méthode qui réinitialise les status du pokémon.  

  
###  ```.reset_attaque_fight()```

>Méthode qui reset les effets des attaques du pokémon en combat.  

  
###  ```.reset_turn_effects()```
> Reset les effets de combat du pokémon ne durant qu'un tour.  

  
###  ```.apply_turn_effects()```
 
> Methode qui applique les effets de tour de fight.  

  
###  ```.update_item_turn_effects()```
 
> Methode qui actualise les effets des objets à la fin d'un tour de combat.  

  
###  ```.reset_stats()```
 
> Méthode qui reset les stats modifiées en combat.  

  
###  ```.use_item(item)```

> Méthode d'utilisation d'un objet sur le pokémon.  
  
> @in : item, objet.Objet  

  
###  ```.give_item(item)```

>Méthode d'attachement d'un objet au pokémon.  
>Applique les effets bonus de l'objet.  
  
>@in : item, objet.Objet  

  
###  ```.def_shiny(is_shiny)```

> Méthode qui détermine si le pokémon est shiny ou pas.  
> Retourn un booléen.  
  
> @in : is_shiny, bool  
> @out : bool  

###  ```generate_random_seed_number.()```  

> Méthode qui détermine la seed random associée au pokémon.  


## *```pokemon_attaque_pool.txt```*

> Fichier contenant le nom des attaques possédées par un Pokémon.
> Le format est le suivant :
> ```Pokemon_name Attaque_pool1 Attaque_pool2```
> 
> Chaque pokémon peut posséder 2 listes d'attaques : la première, la plus commune ( 90% ) et l'autre, une liste secrète d'attaques plus puissantes. Si la 2ème liste est vide, la première sera systématiquement celle choisie.

> Le format des Attaque_pool 1 et 2 sont :
> ```attaque_name1,attaque_name2,attaque_name3,attaque_name4 ...```

> Si un pool d'attaques est composé de plus de 4 attaques, alors le jeu choisira aléatoirement parmi la liste 4 attaques à donner au pokémon.

## *```sac.py```*


### ```class sac.SacIngamePanel([game])```:  
 
>Classe qui représente le panel de sac du joueur.  
>Dans ce panel, le joueur peut accéder à son sac, modifier l'emplacement des objets, les utiliser sur un pokémon, les donner à un pokémon...  

  
### ```.update(surface, possouris, window_pos)``` 

> Méthode d'actualisation de l'affichage du panel.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  
> @in : window_pos, list → coordonnées de la fenêtre ingame  

  
### ```.update_emp( surface, possouris, i)```  

> Méthode d'actualisation de l'affichage de l'emplacement d'un objet.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  
> @in : i, int → indice de l'emplacement (de 1 à 12)  

  
### ```.update_rect_pos(window_pos)```

>Méthode d'actualisation des rects du panel par rapport à la position de la fenêtre ingame.  
  
>@in : window_pos, list → coordonnées de la fenêtre ingame  

  
### ```.change_page(num)``` 

> Méthode de changement de page du sac.  
  
> @in : num, int → numéro de la nouvelle page (1 ou 2)  


  
### ```.left_clic_interactions(possouris)```
  
> Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.  
  
> @in : possouris, list → coordonnées du pointeur de souris  

  
### ```.is_hovering_buttons(possouris)```

>Méthode qui retourne True si la souris est positionnée sur un bouton du panel.  
  
>@in : possouris, list → coordonnées du pointeur de souris  
>@out : bool  

## *```sound.py```*

> Fichier gérant les effets sonores du jeu.

### ```sound.get_sound(sound_name)```

> Fonction qui retourne un objet *pygame.mixer.Sound* chargé depuis le dossier *assets/sounds/*.
> 
> @in : sound_name, str → le nom du fichier son en .wav

### ```sound.play_sound(sound, repetition=0, fadein=0, volume=1.0)```

> Joue le son dont le nom du fichier est rentré en paramètre.
>
> @in : sound, str → le nom du fichier son en .wav
> @in : repetition, int → le nombre de fois où le son sera joué
> @in : fadein, int → temps de fondu audio en ms
> @in : volume, float → puissance sonore, de 0 à 1.0

## *```spawn.py```*

### ```class spawn.SpawnPanel([game])```:  

> Classe représentant le panel d'action "Spawn".  
  
> Dans ce panel, le joueur pourra :  
> - Faire apparaître un pokémon en utilisant 1 action.  
> - Capturer un pokémon apparu en utilisant une Pokéball de son sac.  


  
### ```.update(surface, possouris, window_pos)```
  
> Méthode d'actualisation de l'affichage du panel Spawn.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  
> @in : window_pos, list → coordonnées de la fenêtre ingame  

  
### ```.update_rect_pos(window_pos)```

> Méthode d'actualisation de la position sur l'écran des rects par rapport à la position de la fenêtre ingame.  
  
> @in : window_pos, list → coordonnées de la fenêtre ingame  

  
### ```.spawn_pk()```

> Méthode qui permet de faire apparaître un pokémon.  

  
### ```.catch_pk()```
 
> Méthode qui permet d'attraper un pokémon.  
 
  
### ```.update_spawning_pk_level()```
  
> Méthode d'actualisation du niveau minimal et maximal du pokémon lorsqu'il apparait.  

  
### ```.get_valable_pokemons(player_level, spawning_pk_level)```

> Méthode qui renvoie la liste des noms des pokémons pouvant potentiellement apparaitre en fonction du niveau du joueur et du niveau prédéfini d'apparition du pokémon.  
  
> @in : player_level, int  
> @in : spawning_pk_level, int  
> @out : valable_pks, list  

  
### ```.get_pk_rarity(pokemon_name)```

> Méthode qui retourne la valeur de rareté du pokémon utilisée dans l'algorithme permettant de déterminer le pokémon qui apparaitra.  
  
> @in : pokemon_name, str → Nom du pokémon  
> @out : pokemon_rarity, int → Valeur de rareté  

  
### ```.get_total_spawn_chances(valable_pks)```  

> Méthode qui retourne la somme des valeurs de toutes les raretés cumulées des pokémons dont le nom figure dans la liste des pokémon pouvant potentiellement apparaitre.  
  
> @in : valables_pks, list  
> @out : total_rarity, int  

  
### ```.get_spawning_pokemon(player_level, spawning_pk_lv)```  
  
> Méthode qui retourne le pokémon qui apparait.  
> Il est déterminé à partir du niveau du joueur et du niveau d'apparition du pokémon.  
  
> @in : player_level, int  
> @in : spawning_pk_lv, int  
>@out : pokemon, str → nom du pokémon qui apparait.  
  
### ```.spawning_pk_in_team(team_i)```

>Méthode d'ajout du pokémon spawn dans l'équipe.  
>  
>@in : team_i, int → indice de l'emplacement dans l'équipe  

  
### ```.img_load(file_name)```

> Méthode de chargement d'une image.  
  > 
> @in : file_name, str  
> @out : pygame.Surface  
  
  
### ```.reset()```
 
> Méthode de réinitialisation du panel.  
> Utilisée lors de l'initialisation d'un nouveau tour de jeu.  
 
  
### ```.left_clic_interactions(possouris)```

> Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.  
  
> @in : possouris, list → coordonnées du pointeur de souris  

  
### ```.right_clic_interactions(posssouris)```

>Méthode gérant les intéractions de l'utilisateur avec le clic droit de la souris.  
>  
>@in : possouris, list → coordonnées du pointeur de souris  

  
### ```.is_hovering_buttons(possouris)```  

>Méthode qui retourne True si la souris est positionnée sur un bouton du panel.  
 > 
>@in : possouris, list → coordonnées du pointeur de souris  

## *```special_pokemon.py```*

> Fichier gérant les pokémons spéciaux du jeu.
> Contient la classe ```Pokemon```, fonctionnant de la même manière que *```pokemon.Pokemon```*.

> Se référer à **[```pokemon.py```](#pokemon.py)** pour la documentation.

> Contient également la liste des pokémons spéciaux du jeu, à compléter dès qu'un nouveau pokémon spécial est ajouté au jeu.

## *```special_pokemon_attaque.txt```*

> Fonctionne de la même manière que [**```pokemon_attaque_pool.txt```**](#pokemon_attaque_pooltxt).
> Attention cependant, le format est différent : 
> ```Name|attaque_pool1 attaque_pool2```

## *```special_pokemons.csv```*

> Fichier contenant les informations de tous les pokémons spéciaux du jeu.
> Le format est exactement le même que celui de [**```all_pokemons.csv```**](#all_pokemonscsv).

## *```starters.py```*

### ```class starters.StarterPanel([game])```:  

> Classe représentant le panel de sélection du pokémon starter du joueur.  

  
### ```.update(surface, possouris)```

> Méthode d'actualisation de l'affichage du panel.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  
> @in : window_pos, list → coordonnées de la fenêtre ingame  

  
### ```.update_animations()```
 
> Méthode d'actualisation de l'animation des éléments au cours du temps.  

  
### ```.update_pk_emps(surface, possouris)``` 

> Méthode d'actualisation de l'affchage des emplacements de pokémons.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  

  
### ```.update_pokemon(surface, possouris, i)```

> Méthode d'actualisation de l'affichage des pokémons starters.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  
>@in : i, int → indice du pokémon  

  
### ```.update_drop_pk_emp(surface, possouris)```

> Méthode d'actualisation de l'affichage de l'emplacement pour drop le pokémon.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  

  
### ```.update_aide_button(surface, possouris)```

>Méthode d'actualisation de l'affichage du botuon aide.  
  
>@in : surface, pygame.Surface → fenêtre du jeu  
>@in : possouris, list → coordonnées du pointeur de souris  

  
### ```.update_text_box(surface)``` 

>Méthode d'actualisation de l'affichage de la zone de texte.  
  
>@in : surface, pygame.Surface → fenêtre du jeu  

  
### ```.update_dresseur(surface)```

> Méthode d'actualisation de l'affichage du dresseur.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  

  
### ```.update_intro_skip_button(surface, possouris)```
  
> Méthode d'actualisation du bouton "skip l'intro".  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  
 
  
### ```.skip_intro()``` 
> Méthode qui permet de skip l'intro.   
  
### ```.is_hovering_buttons(possouris)```

> Méthode qui retourne True si la souris est positionnée sur un bouton du panel.  
>   
> @in : possouris, list → coordonnées du pointeur de souris  
> @out : bool  

  
### ```.left_clic_interactions(possouris)```

> Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.  
  
> @in : possouris, list → coordonnées du pointeur de souris  

## *```train.py```*

### ```class train.TrainPanel([game])```:  
  
> Classe représentant le panel de l'action "Train".  
> Dans ce panel, le joueur pourra affronter entrainer ses pokémon en lançant un combat dont il pourra choisir la difficulté.  

  
### ```.update(surface, possouris, window_pos)```

> Méthode d'actualisation de l'affichage du panel.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  
 >@in : window_pos, list → coordonnées de la fenêtre ingame  

  
### ```.update_training_pk_emp(surface, possouris)``` 

> Methode d'actualisation de l'affichage de l'emplacement du pokémon à entrainer du joueur.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  

  
### ```.update_ennemy_preview(surface, possouris)```

> Methode d'actualisation de l'affichage de la preview du pokemon ennemi.  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
 >@in : possouris, list → coordonnées du pointeur de souris  

  
### ```.update_settings_popup(surface, possouris)```

> Méthode d'actualisation de l'affichage du popup "settings".  
  
> @in : surface, pygame.Surface → fenêtre du jeu  
> @in : possouris, list → coordonnées du pointeur de souris  

  
### ```.update_training_pk()```

> Methode permettant de changer le pokémon à entrainer du joueur.  

  
### ```.update_all_rects(window_pos)```

>Méthode d'actualisation des rects en fonction de la position de la fenêtre ingame.  
  
>@in : window_pos, list → coordonnées de la fenêtre ingame  

  
### ```.start_fight()``` 

> Méthode de lancement de combat.  

  
### ```.open_settings_popup()```

> Méthode d'ouverture du popup "settings".  

  
### ```.close_settings_popup()```  

> Méthode de fermeture du popup "settings".  

  
### ```.spawn_ennemy_pk(diff)```

> Methode qui génére et renvoie le pokémon ennemi en fonction de la difficulté.  
> Si aucun pokémon ne peut apparaitre, la méthode renvoie None.  
  
> @in : diff, str → difficulté du combat  

  
### ```.set_difficult(diff='easy')```  

> Méthode de modification de la difficulté.  
  
> @in : diff, str → la nouvelle difficulté sélectionnée  

  
### ```.set_ennemy_pks()```
  
> Methode d'actualisation des pokémons ennemis en fonction du pokémon à entrainer du joueur.  
 
  
### ```.load_ennemy_pk()```

> Methode qui charge les images liées au pokémon ennemi pour limiter les chargements répétés  

  
### ```.get_ennemy_pk_name(diff, ennemy_pk_lv)```  

>Methode qui détermine le nom du pokémon ennemi en fonction de la difficulté  
 
  
### ```.get_ennemy_pk_level(diff)```

> Methode qui determine le level du pokémon ennemi à affronter selon la difficulté choisie.  
  
> @in : diff, str → difficulté du combat.  

  
### ```.add_pk_to_team(team_i)```

> Méthode permettant d'ajouter un pokémon à l'équipe du joueur.  
  
> @in : team_i, int → indice du pokémon dans l'équipe  

  
### ```.reset()```

> Méthode de réinitialisation du panel.  
> Utilisée lors de l'initialisation d'un nouveau tour de jeu.  
 
  
### ```.close()```

> Méthode classique qui éxécute tout ce qu'il faut faire lorsque le panel est fermé.  

  
### ```.left_clic_interactions(possouris)```

> Méthode gérant les intéractions de l'utilisateur avec le clic gauche de la souris.  
  
> @in : possouris, list → coordonnées du pointeur de souris  

  
### ```.right_clic_interactions(posssouris)```

>Méthode gérant les intéractions de l'utilisateur avec le clic droit de la souris.  
>  
>@in : possouris, list → coordonnées du pointeur de souris  

  
### ```.is_hovering_settings_popup_buttons(possouris)```

> Méthode qui retourne True si la souris est positionnée sur un bouton du popup "settings".  
  
> @in : possouris, list → coordonnées du pointeur de souris  
> @out : bool  
 
  
### ```.is_hovering_buttons(possouris)```

> Méthode qui retourne True si la souris est positionnée sur un bouton du panel.  
  
> @in : possouris, list → coordonnées du pointeur de souris  
> @out : bool  

