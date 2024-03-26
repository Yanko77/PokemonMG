"""
Fichier contenant les fonctions de calcul du selection de l'action à réaliser par les PNJ (Personnage Non-Joueur) durant un combat.
"""

# importation des modules
import pokemon
import game_infos

# declaration des constantes
SPEED_HEAL = 333  # valeur entre 0 et 1000


# declaration des fonctions
def calcul_degats(pk, ennemy_pk, attaque, crit=False) -> int:
    """
    Methode de calcul des dégats simulés d'une attaque du pokémon du PNJ sur le pokémon du joueur.
    Retourne le montant de dégats de la simulation sur le pokémon du joueur.
    
    @in: pk, pokemon.Pokemon => Pokémon du PNJ
    @in: ennemy_pk, pokemon.Pokemon => Pokémon du joueur
    @in: attaque, attaque.Attaque => Attaque simulée
    @in: crit, bool => True si l'attaque critique, False sinon
    @out: degats, int
    """
    if attaque.puissance != 0 and ennemy_pk.is_vulnerable:
        cm = 1
        # Calcul avec stab ( attaque de type maternel )
        if attaque.type in [pk.type, pk.type2]:
            cm *= 1.5
    
        # Calcul avec affinités des types
        cm *= game_infos.get_mutiliplicateur(attaque.type, ennemy_pk.type)
    
        if not ennemy_pk.type2 == 'NoType':
            cm *= game_infos.get_mutiliplicateur(attaque.type, ennemy_pk.type2)
    
        if crit:
            cm *= (2 * pk.level + 5) / (pk.level + 5)
    
        if attaque.puissance == "level":
            puissance = pk.level
        elif attaque.puissance == "ennemy_pv":
            puissance = 1000000
        elif attaque.puissance == "pv*0.5":
            puissance = ennemy_pk.health // 2
        elif attaque.special_puissance == 'v':
            if pk.speed <= ennemy_pk.speed:
                puissance = int(attaque.puissance.split("-")[0])
            else:
                puissance = int(attaque.puissance.split("-")[1])
        else:
            puissance = attaque.puissance
    
        if attaque.special_puissance == 'c':
            degats = attaque.puissance
        elif attaque.puissance == "effort":
            degats = ennemy_pk.pv - pk.health
        else:
            degats = round((((((pk.level * 0.4 + 2) * pk.attack * puissance) / pk.defense) / 50) + 2) * cm)


    else:
        degats = 0

    return degats


def get_npc_action(pk, ennemy_pk, att: list) -> attaque.Attaque:
    """
    Methode de selection de la meilleure action à réaliser pour le pokémon du PNJ.
    Retourne l'attaque à réaliser.

    @in: pk, pokemon.Pokemon => Pokémon du PNJ
    @in: ennemy_pk, pokemon.Pokemon => Pokémon du joueur
    @in: att, list => liste d'attaque du pokémon du PNJ
    @out: attaque.Attaque => Meilleure attaque à réaliser pour le pokémon du PNJ
    """
    score = []
    is_killing = []
    for attaque in att:
        if attaque is not None:
            degat = calcul_degats(pk, ennemy_pk, attaque, False)
            if degat > ennemy_pk.health:
                is_killing.append(attaque)

    if is_killing == []:
        for attaque in att:
            if attaque is not None:
                degat = calcul_degats(pk, ennemy_pk, attaque, False)
                degat_crit = calcul_degats(pk, ennemy_pk, attaque, True)
                delta_degat = degat_crit - degat
                t = round(int(pk.infos[6]) / 2) * attaque.taux_crit
                scoretemp = degat + delta_degat * t
                taux = attaque.precision/100

                # Calcul des bonus spéciaux des attaques ( altération de status, double attaque, invnlnérabilités,
                if attaque.special_effect[0][0] == 'status' and ennemy_pk.status[str(attaque.special_effect[0][1])] is not True:
                    scoretemp *= (1 + int(attaque.special_effect[0][2])/100)

                scoretemp *= taux
                if attaque.special_effect[0][0] == 'heal_on_maxpv' or attaque.special_effect[0] == 'long_time_heal_par_tour_of_maxpv':
                    scoretemp += (pk.pv/pk.health - 1) * round((pk.level*0.4 * pk.attack) / pk.defense) * 150
                if attaque.special_effect[0][0] == 'heal_on_atk':
                    taux_heal_on_atk, _ = attaque.special_effect[0][1].split("*")
                    #scoretemp = scoretemp * (1 + (SPEED_HEAL/400) * float(taux_heal_on_atk))
                    scoretemp = scoretemp * (1 + (SPEED_HEAL/400) * float(taux_heal_on_atk) * (-2*(pk.health/pk.pv)+2))

                # print(attaque.name, scoretemp)

                score.append(scoretemp)

        max = score[0]
        j = 0
        for i in range(len(score)):
            if score[i] > max:
                max = score[i]
                j = i

        return att[j]

    else:
        for attaque in is_killing:
            score.append(attaque.precision)

        max = score[0]
        j = 0
        for i in range(len(score)):
            if score[i] > max:
                max = score[i]
                j = i
        return is_killing[j]



# programme principal (test)
if __name__ == '__main__':
    import game
    import attaques as att
    game = game.Game()
    dracaufeu = pokemon.Pokemon('Dracaufeu', 20, game.player)
    tortank = pokemon.Pokemon('Tortank', 20, game.player)
    tortank2 = pokemon.Pokemon('Tortank', 20, game.player)
    print(tortank.pv)

    att_list = [att.Attaque('Griffe_Acier'), att.Attaque('Vampibaiser')]
    
    print(get_npc_action(tortank, tortank2, att_list).name)
