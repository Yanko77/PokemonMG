import pygame
import random


def find_pokemon_line(name) -> list:
    with open('all_pokemons.txt') as file:
        for line in file.readlines():
            if line.split()[0] == name:
                return line.split()


def get_valable_pokemons(player_level):
    valable_pks = []
    with open('all_pokemons.txt', 'r') as file:
        for line in file.readlines():
            line = line.split()
            if not (line[0] == "#" or line[0] == "name"):
                if int(line[13]) <= player_level:
                    valable_pks.append(line[0])
    return valable_pks


def get_pk_rarity(pokemon):
    pokemon_rarety = int(find_pokemon_line(pokemon)[1])
    pokemon_rarety = 100 - pokemon_rarety
    return pokemon_rarety


def get_total_spawn_chances(valable_pks):
    total_rarety = 0
    for pokemon in valable_pks:
        pokemon_rarety = get_pk_rarity(pokemon)
        total_rarety += pokemon_rarety
    return total_rarety


def get_spawning_pokemon(player_level):
    generated_number = random.randint(0, get_total_spawn_chances(get_valable_pokemons(player_level)))
    max_spawn_value = 0
    for pokemon in get_valable_pokemons(player_level):
        max_spawn_value += get_pk_rarity(pokemon)
        if max_spawn_value < generated_number:
            pass
        else:
            return pokemon


if __name__ == "__main__":
    print(get_spawning_pokemon(0))
