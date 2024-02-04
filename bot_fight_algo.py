
def attaque(pk, ennemy_pk, attaque):
    cm = 1
    # Calcul avec stab ( attaque de type maternel )
    if attaque.type in [pk.type, pk.type2]:
        cm *= 1.5

    # Calcul avec affinités des types
    cm *= game_infos.get_mutiliplicateur(attaque.type, ennemy_pk.type) * game_infos.get_mutiliplicateur(attaque.type, ennemy_pk.type2)
    # Calcul avec taux de crit
    t = round(int(pk.line[6]) / 2) * attaque.taux_crit
    ncrit = random.randint(0, 256)
    if ncrit < t:
        crit = True
    else:
        crit = False

    if crit:
        cm *= (2 * pk.level + 5) / (pk.level + 5)

    if "augmentation_degats" in ennemy_pk.objet.classes:
        cm *= ennemy_pk.objet.multiplicateur_degats()
    random_cm = random.randint(85, 100)
    cm = cm * random_cm / 100
    degats = round((((((pk.level * 0.4 + 2) * pk.attack * attaque.puissance) / pk.defense) / 50) + 2) * cm)
    ennemy_pk.damage(degats)
    print(degats)

def bot_fight_algo(ennemy_pk:ennemy_pk, pk:ennemy_pk , att:list):
    esperence = []
    for attaque in att:





