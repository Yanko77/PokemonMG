# importation des module
import pokemon
import game_infos

# declaration des constante
SPEED_HEAL = 333 #valeur entre 0 et 1000

#declaration des fonction
def calcul_degats(pk, ennemy_pk, attaque, crit=False):
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

    degats = round((((((pk.level * 0.4 + 2) * pk.attack * attaque.puissance) / pk.defense) / 50) + 2) * cm)
    return degats


def get_npc_action(pk, ennemy_pk , att:list):
    esperence = []
    is_killing = []
    for attaque in att:
        degat = calcul_degats(pk, ennemy_pk, attaque, False)
        # print(degat)
        if degat > ennemy_pk.health:
            is_killing.append(attaque)
    if is_killing == []:
        for attaque in att:
            
            degat = calcul_degats(pk, ennemy_pk, attaque, False)
            degat_crit = calcul_degats(pk, ennemy_pk, attaque, True)
            delta_degat = degat_crit - degat
            t = round(int(pk.line[6]) / 2) * attaque.taux_crit
            scoretemp = degat + delta_degat * t
            taux = attaque.precision/100

            # Calcul des bonus spéciaux des attaques ( altération de status, double attaque, invnlnérabilités,
            if attaque.special_effect[0][0] == 'status' and ennemy_pk.status[str(attaque.special_effect[0][1])] is not True:
                scoretemp *= (1 + int(attaque.special_effect[0][2])/100)

            scoretemp *= taux
            if attaque.special_effect[0][0] == 'heal_on_maxpv' or attaque.special_effect[0] == 'long_time_heal_par_tour_of_maxpv':
                scoretemp = (pk.pv/pk.health) * SPEED_HEAL
            if attaque.special_effect[0][0] == 'heal_on_atk':
                taux_heal_on_atk, _ = attaque.special_effect[0][1].split("*")
                #scoretemp = scoretemp * (1 + (SPEED_HEAL/400) * float(taux_heal_on_atk))
                scoretemp = scoretemp * (1 + (SPEED_HEAL/400) * float(taux_heal_on_atk) * (-2*(pk.health/pk.pv)+2))
                
                
            print(attaque.name, scoretemp)
            esperence.append(scoretemp)

    else:
        for attaque in att:
            esperence.append(attaque.precision)

    max = esperence[0]
    j = 0
    for i in range(len(esperence)):
        if esperence[i] > max:
            max = esperence[i]
            j = i
    print(att[j].name)
    return att[j]

# programe principal (test)
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
