
types_affinities = {
    'normal': {'normal': 1,
               'plante': 1,
               'feu': 1,
               'eau': 1,
               'elec': 1,
               'glace': 1,
               'combat': 1,
               'poison': 1,
               'sol': 1,
               'vol': 1,
               'psy': 1,
               'insect': 1,
               'roche': 0.5,
               'spectre': 0,
               'dragon': 1,
               'dark': 1,
               'acier': 0.5,
               'fee': 1
               },
    'plante': {
               'normal': 1,
               'plante': 0.5,
               'feu': 0.5,
               'eau': 2,
               'elec': 1,
               'glace': 1,
               'combat': 1,
               'poison': 0.5,
               'sol': 2,
               'vol': 0.5,
               'psy': 1,
               'insect': 0.5,
               'roche': 2,
               'spectre': 1,
               'dragon': 1,
               'dark': 1,
               'acier': 1,
               'fee': 1
    },

    'feu': {'normal': 1,
            'plante': 2,
            'feu': 0.5,
            'eau': 0.5,
            'elec': 1,
            'glace': 2,
            'combat': 1,
            'poison': 1,
            'sol': 1,
            'vol': 1,
            'psy': 1,
            'insect': 2,
            'roche': 0.5,
            'spectre': 1,
            'dragon': 0.5,
            'dark': 1,
            'acier': 2,
            'fee': 1},
    'eau': {'normal': 1,
            'plante': 0.5,
            'feu': 2,
            'eau': 0.5,
            'elec': 1,
            'glace': 1,
            'combat': 1,
            'poison': 1,
            'sol': 2,
            'vol': 1,
            'psy': 1,
            'insect': 1,
            'roche': 2,
            'spectre': 1,
            'dragon': 0.5,
            'dark': 1,
            'acier': 1,
            'fee': 1},
    'elec': {'normal': 1,
             'plante': 0.5,
             'feu': 1,
             'eau': 2,
             'elec': 0.5,
             'glace': 1,
             'combat': 1,
             'poison': 1,
             'sol': 0,
             'vol': 2,
             'psy': 1,
             'insect': 1,
             'roche': 1,
             'spectre': 1,
             'dragon': 0.5,
             'dark': 1,
             'acier': 1,
             'fee': 1},
    'glace': {'normal': 1,
              'plante': 2,
              'feu': 0.5,
              'eau': 0.5,
              'elec': 1,
              'glace': 0.5,
              'combat': 1,
              'poison': 1,
              'sol': 2,
              'vol': 2,
              'psy': 1,
              'insect': 1,
              'roche': 1,
              'spectre': 1,
              'dragon': 2,
              'dark': 1,
              'acier': 0.5,
              'fee': 1},
    'combat': {'normal': 2,
               'plante': 1,
               'feu': 1,
               'eau': 1,
               'elec': 1,
               'glace': 2,
               'combat': 1,
               'poison': 0.5,
               'sol': 1,
               'vol': 0.5,
               'psy': 0.5,
               'insect': 0.5,
               'roche': 2,
               'spectre': 0,
               'dragon': 1,
               'dark': 2,
               'acier': 2,
               'fee': 0.5},
    'poison': {'normal': 1,
               'plante': 2,
               'feu': 1,
               'eau': 1,
               'elec': 1,
               'glace': 1,
               'combat': 1,
               'poison': 0.5,
               'sol': 0.5,
               'vol': 1,
               'psy': 1,
               'insect': 1,
               'roche': 0.5,
               'spectre': 0.5,
               'dragon': 1,
               'dark': 2,
               'acier': 2,
               'fee': 0.5},
    'sol': {'normal': 1,
            'plante': 0.5,
            'feu': 2,
            'eau': 1,
            'elec': 2,
            'glace': 1,
            'combat': 1,
            'poison': 2,
            'sol': 1,
            'vol': 0,
            'psy': 1,
            'insect': 0.5,
            'roche': 2,
            'spectre': 1,
            'dragon': 1,
            'dark': 1,
            'acier': 2,
            'fee': 1},
    'vol': {'normal': 1,
            'plante': 2,
            'feu': 1,
            'eau': 1,
            'elec': 0.5,
            'glace': 1,
            'combat': 2,
            'poison': 1,
            'sol': 1,
            'vol': 1,
            'psy': 1,
            'insect': 2,
            'roche': 0.5,
            'spectre': 1,
            'dragon': 1,
            'dark': 1,
            'acier': 0.5,
            'fee': 1},
    'psy': {'normal': 1,
            'plante': 1,
            'feu': 1,
            'eau': 1,
            'elec': 1,
            'glace': 1,
            'combat': 2,
            'poison': 2,
            'sol': 1,
            'vol': 1,
            'psy': 0.5,
            'insect': 1,
            'roche': 1,
            'spectre': 1,
            'dragon': 1,
            'dark': 0,
            'acier': 0.5,
            'fee': 1},
    'insect': {'normal': 1,
               'plante': 2,
               'feu': 0.5,
               'eau': 1,
               'elec': 1,
               'glace': 1,
               'combat': 0.5,
               'poison': 0.5,
               'sol': 1,
               'vol': 0.5,
               'psy': 2,
               'insect': 1,
               'roche': 1,
               'spectre': 0.5,
               'dragon': 1,
               'dark': 2,
               'acier': 0.5,
               'fee': 0.5},
    'roche': {'normal': 1,
              'plante': 1,
              'feu': 1,
              'eau': 1,
              'elec': 1,
              'glace': 2,
              'combat': 0.5,
              'poison': 1,
              'sol': 0.5,
              'vol': 2,
              'psy': 1,
              'insect': 2,
              'roche': 1,
              'spectre': 1,
              'dragon': 1,
              'dark': 1,
              'acier': 0.5,
              'fee': 1},
    'spectre': {'normal': 0,
                'plante': 1,
                'feu': 1,
                'eau': 1,
                'elec': 1,
                'glace': 1,
                'combat': 1,
                'poison': 1,
                'sol': 1,
                'vol': 1,
                'psy': 2,
                'insect': 1,
                'roche': 1,
                'spectre': 2,
                'dragon': 1,
                'dark': 0.5,
                'acier': 1,
                'fee': 1},
    'dragon': {'normal': 1,
               'plante': 1,
               'feu': 1,
               'eau': 1,
               'elec': 1,
               'glace': 1,
               'combat': 1,
               'poison': 1,
               'sol': 1,
               'vol': 1,
               'psy': 1,
               'insect': 1,
               'roche': 1,
               'spectre': 1,
               'dragon': 2,
               'dark': 1,
               'acier': 0.5,
               'fee': 0},
    'dark': {'normal': 1,
             'plante': 1,
             'feu': 1,
             'eau': 1,
             'elec': 1,
             'glace': 1,
             'combat': 0.5,
             'poison': 1,
             'sol': 1,
             'vol': 1,
             'psy': 2,
             'insect': 1,
             'roche': 1,
             'spectre': 2,
             'dragon': 1,
             'dark': 0.5,
             'acier': 1,
             'fee': 0.5},
    'acier': {'normal': 1,
              'plante': 0.5,
              'feu': 0.5,
              'eau': 1,
              'elec': 0.5,
              'glace': 2,
              'combat': 1,
              'poison': 1,
              'sol': 1,
              'vol': 1,
              'psy': 1,
              'insect': 1,
              'roche': 2,
              'spectre': 1,
              'dragon': 1,
              'dark': 1,
              'acier': 0.5,
              'fee': 2},
    'fee': {'normal': 1,
            'plante': 0.5,
            'feu': 1,
            'eau': 1,
            'elec': 1,
            'glace': 1,
            'combat': 2,
            'poison': 0.5,
            'sol': 1,
            'vol': 1,
            'psy': 1,
            'insect': 1,
            'roche': 1,
            'spectre': 0,
            'dragon': 2,
            'dark': 2,
            'acier': 0.5,
            'fee': 1},

    'NoType': {'normal': 1,
               'plante': 1,
               'feu': 1,
               'eau': 1,
               'elec': 1,
               'glace': 1,
               'combat': 1,
               'poison': 1,
               'sol': 1,
               'vol': 1,
               'psy': 1,
               'insect': 1,
               'roche': 1,
               'spectre': 1,
               'dragon': 1,
               'dark': 1,
               'acier': 1,
               'fee': 1
               }

}

type_colors = {
    'normal': (168, 167, 122),
    'plante': (122, 199, 76),
    'feu': (238, 129, 48),
    'eau': (99, 144, 240),
    'elec': (247, 208, 44),
    'glace': (150, 217, 214),
    'combat': (194, 46, 40),
    'poison': (163, 62, 161),
    'sol': (226, 191, 101),
    'vol': (169, 143, 243),
    'psy': (249, 85, 135),
    'insect': (166, 185, 26),
    'roche': (182, 161, 54),
    'spectre': (115, 87, 151),
    'dragon': (111, 53, 252),
    'dark': (112, 87, 70),
    'acier': (183, 183, 206),
    'fee': (214, 133, 173)
}

type_names_to_print = {
    'normal': 'NORMAL',
    'plante': 'PLANTE',
    'feu': 'FEU',
    'eau': 'EAU',
    'elec': 'ELEK',
    'glace': 'GLACE',
    'combat': 'COMBAT',
    'poison': 'POISON',
    'sol': 'SOL',
    'vol': 'VOL',
    'psy': 'PSY',
    'insect': 'INSECT',
    'roche': 'ROCHE',
    'spectre': 'SPECTR',
    'dragon': 'DRAGON',
    'dark': 'DARK',
    'acier': 'ACIER',
    'fee': 'FEE'

}


def get_mutiliplicateur(type_atk_pk, type_def_pk2):
    return types_affinities[type_atk_pk][type_def_pk2]


def get_all_diff_pokemons(game, attacking_pokemon, level: int, difficulty='easy'):
    multiplicateur_diff = {
        'easy': (16, 8, 4, 2,),
        'normal': (1,),
        'hard': (0.5, 0.25, 0.125, 0.0625, 0)
    }

    pokemon_type = attacking_pokemon.get_type()
    pokemon_type2 = attacking_pokemon.get_type2()

    multiplicateur = multiplicateur_diff[difficulty]

    if pokemon_type == 'normal' and pokemon_type2 == 'NoType' and difficulty == 'easy':
        multiplicateur = (1,)

    types_list = get_diff_types(pokemon_type, pokemon_type2, multiplicateur)  # Marche pour les tuples
    type_list2 = get_diff_types(pokemon_type, pokemon_type2, multiplicateur + (1,))
    type_list2.append('NoType')

    pokemons_list = []

    for pokemon_infos in game.pokemons_list.values():
        if pokemon_infos[9] <= game.player.get_level() and pokemon_infos[11] < level < pokemon_infos[12]:
            if pokemon_infos[2] in types_list:
                if pokemon_infos[10] in type_list2:
                    pokemons_list.append(pokemon_infos[0])
            elif pokemon_infos[10] in types_list:
                if pokemon_infos[2] in type_list2:
                    pokemons_list.append(pokemon_infos[0])

    if pokemons_list == []:
        assert difficulty != 'easy', "Pas de pokémon facile pour le training pk choisi"

        if difficulty == 'hard':
            diff = 'normal'
        elif difficulty == 'normal':
            diff = 'easy'

        pokemons_list = get_all_diff_pokemons(game, attacking_pokemon, level, diff)

    return pokemons_list


def get_diff_types(pokemon_type, pokemon_type2, multiplicateur):
    types_list = []

    for pk_type in types_affinities[pokemon_type]:
        if pokemon_type2 != 'NoType':
            if types_affinities[pokemon_type][pk_type]*types_affinities[pokemon_type2][pk_type] in multiplicateur:
                types_list.append(pk_type)
        else:
            if types_affinities[pokemon_type][pk_type] in multiplicateur:
                types_list.append(pk_type)

    return types_list


def get_type_name_to_print(type):
    return type_names_to_print[type]


def get_type_color(type):
    return type_colors[type]


if __name__ == '__main__':
    # Facile
    '''print(get_diff_types('normal', 'vol', (16, 8, 4, 2)))
    print(get_diff_types('normal', 'vol', (16, 8, 4, 2, 1)))'''
    # Normal
    '''print(get_diff_types('normal', 'vol', (1,)))
    print(get_diff_types('normal', 'vol', (1,)))'''
    # Difficile
    print(get_diff_types('normal', 'vol', (0.5, 0.25, 0.125, 0.0625,)))
    print(get_diff_types('normal', 'vol', (0.5, 0.25, 0.125, 0.0625, 1)))
