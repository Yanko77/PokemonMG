import pokemon
import game_infos


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

def bot_fight_algo(ennemy_pk, pk , att:list):
    esperence = []
    is_killing = []
    for attaque in att:
        degat = calcul_degats(pk, ennemy_pk, attaque, False)
        print(degat)
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
            print(scoretemp)
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
    return att[j]


if __name__ == '__main__':
    import game
    import attaques as att
    game = game.Game()
    dracaufeu = pokemon.Pokemon('Dracaufeu', 20, game.player)
    tortank = pokemon.Pokemon('Tortank', 20, game.player)
    tortank2 = pokemon.Pokemon('Tortank', 20, game.player)
    tortank2.health = 10

    att_list = [att.Attaque('Feu_Sacre'), att.Attaque('Lance-Flammes')]

    print(bot_fight_algo(tortank2, dracaufeu, att_list).name)